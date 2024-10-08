import asyncio
import chainlit as cl
import openai
import os
from langsmith import traceable
from dotenv import load_dotenv
from datetime import datetime
import json
from prompts import ASSESSMENT_PROMPT, SYSTEM_PROMPT
from client_record import read_client_record, write_client_record, format_client_record, parse_client_record

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
    },
    "openai_gpt-4o-mini": {
        "endpoint_url": os.getenv("OPENAI_ENDPOINT"),
        "api_key": openai_api_key,
        "model": "gpt-4o-mini"
    }
}

# Choose configuration
# config_key = "openai_gpt-4"
config_key = "openai_gpt-4o-mini"
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


# Configuration setting to enable or disable the system prompt
ENABLE_SYSTEM_PROMPT = True

@traceable
def get_latest_user_message(message_history):
    # Iterate through the message history in reverse to find the last user message
    for message in reversed(message_history):
        if message['role'] == 'user':
            return message['content']
    return None

@traceable
async def assess_message(message_history):
    file_path = "client_record.md"
    markdown_content = read_client_record(file_path)
    print("----------------\n [DEBUG] Markdown content: \n\n", markdown_content, "\n----------------\n" )
    parsed_record = parse_client_record(markdown_content)

    latest_message = get_latest_user_message(message_history)

    # Remove the original prompt from the message history for assessment
    filtered_history = [msg for msg in message_history if msg['role'] != 'system']

    # Convert message history and suggestions to strings
    history_str = json.dumps(filtered_history, indent=4)
    suggestions_str = json.dumps(parsed_record.get("Suggestions", {}), indent=4)
    
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Generate the assessment prompt
    filled_prompt = ASSESSMENT_PROMPT.format(
        latest_message=latest_message,
        history=history_str,
        existing_suggestions=suggestions_str,
        current_date=current_date
    )

    print("\n\n-----------Filled prompt: \n\n", filled_prompt, "\n\n")

    response = await client.chat.completions.create(messages=[{"role": "system", "content": filled_prompt}], **gen_kwargs)

    assessment_output = response.choices[0].message.content.strip()
    print("\n\n-----------Assessment Output: \n\n", assessment_output, "\n\n")

    # Parse the assessment output
    suggestion_updates = parse_assessment_output(assessment_output)

    # Update the client record with the new suggestions
    for update in suggestion_updates:
        topic = update["topic"]
        date = update["date"]
        suggestion = update["suggestion"]
        reason = update["reason"]
        parsed_record["Suggestions"][topic] = {
            "topic": topic,
            "date": date,
            "suggestion": suggestion,
            "reason": reason
        }

    # Format the updated record and write it back to the file
    updated_content = format_client_record(
        parsed_record["Client Information"],
        parsed_record["Suggestions"]
    )
    write_client_record(file_path, updated_content)
    return suggestion_updates

@traceable
def parse_assessment_output(output):
    try:
        parsed_output = json.loads(output)
        suggestion_updates = parsed_output.get("suggestion_updates", [])
        return suggestion_updates
    except json.JSONDecodeError as e:
        print("Failed to parse assessment output:", e)
        return [], []

@traceable
@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])

    if ENABLE_SYSTEM_PROMPT and (not message_history or message_history[0].get("role") != "system"):
        message_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

    message_history.append({"role": "user", "content": message.content})

    asyncio.create_task(assess_message(message_history))
    
    response_message = cl.Message(content="")
    await response_message.send()

    if config_key == "mistral_7B":
        stream = await client.completions.create(prompt=message.content, stream=True, **gen_kwargs)
        async for part in stream:
            if token := part.choices[0].text or "":
                await response_message.stream_token(token)
    else:
        stream = await client.chat.completions.create(messages=message_history, stream=True, **gen_kwargs)
        async for part in stream:
            if token := part.choices[0].delta.content or "":
                await response_message.stream_token(token)

    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)
    await response_message.update()


if __name__ == "__main__":
    cl.main()
