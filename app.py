import base64
import chainlit as cl
import openai
import os
from langsmith import traceable
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

runpod_serverless_id = os.getenv("RUNPOD_SERVERLESS_ID")

runpod_api_key = os.getenv("RUNPOD_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

endpoint_url = f"https://api.runpod.ai/v2/{runpod_serverless_id}/openai/v1"



configurations = {
    "mistral_7B_instruct": {
        "endpoint_url": os.getenv("MISTRAL_7B_INSTRUCT_ENDPOINT"),
        "api_key": runpod_api_key,
        "model": "mistralai/Mistral-7B-Instruct-v0.3"
    },
    "mistral_7B": {
        "endpoint_url": os.getenv("MISTRAL_7B_ENDPOINT"),
        "api_key": runpod_api_key,
        "model": "mistralai/Mistral-7B-v0.1"
    },
    "openai_gpt-4": {
        "endpoint_url": os.getenv("OPENAI_ENDPOINT"),
        "api_key": openai_api_key,
        "model": "gpt-4"
    }
}

# Choose configuration
config_key = "openai_gpt-4"
# config_key = "mistral_7B_instruct"
# config_key = "mistral_7B"


# Get selected configuration
config = configurations[config_key]

client = openai.AsyncClient(api_key=config["api_key"], base_url=config["endpoint_url"])

gen_kwargs = {
    "model": config["model"],
    "temperature": 0.3,
    "max_tokens": 500
}

@cl.on_message
@traceable
async def on_message(message: cl.Message):
    # Maintain an array of messages in the user session
    message_history = cl.user_session.get("message_history", [])

    # Processing images exclusively
    images = [file for file in message.elements if "image" in file.mime] if message.elements else []

    if images:
        # Read the first image and encode it to base64
        with open(images[0].path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
        message_history.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": message.content if message.content else "What’s in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        })
    else:
        message_history.append({"role": "user", "content": message.content})

    response_message = cl.Message(content="")
    await response_message.send()
    
    # Pass in the full message history for each request
    stream = await client.chat.completions.create(messages=message_history, 
                                                  stream=True, **gen_kwargs)
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)

    await response_message.update()

    # Record the AI's response in the history
    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)