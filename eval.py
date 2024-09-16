from langsmith.evaluation import evaluate
from langsmith.schemas import Run, Example
from openai import OpenAI
import json
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai

from langsmith import traceable

# Load environment variables
load_dotenv()

# Define AI system
client = wrap_openai(OpenAI())

@traceable
def client_record_accuracy_evaluator(run: Run, example: Example) -> dict:
    inputs = example.inputs["message_history"]
    model_output = example.outputs['output']
    print(f"\n\nInputs: {inputs}\n\n")
    print(f"\n\nOutputs: {model_output}\n\n")

    # Extract system prompt
    system_prompt = next((msg['content'] for msg in inputs if msg['role'] == 'system'), "")

    # Extract message history
    message_history = []
    for msg in inputs:
        if msg['role'] in ['user', 'assistant']:
            message_history.append({
                "role": msg['role'],
                "content": msg['content']
            })

    # Extract latest user message and model output
    latest_message = message_history[-1]['content'] if message_history else ""
    print(f"\n\nLatest User Message: {latest_message}\n\n")

    evaluation_prompt = f"""
    System Prompt: {system_prompt}

    Message History:
    {json.dumps(message_history, indent=2)}

    Latest User Message: {latest_message}

    Model Output: {model_output}

    Based on the above information, evaluate the model's output for compliance with the system prompt and context of the conversation. 
    Give your answer on a scale of 1 to 5, where 5 means that the model_output is an accurate client record of the alerts and readings
    that came up in the conversation in message_history and 1 means that the model_output is a completely inaccurate client record of the alerts and readings that
    came up in the conversation in message_history.

    Also provide a brief explanation for your score.

    Respond in the following JSON format:
    {{
        "score": <int>,
        "explanation": "<string>"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant tasked with evaluating the compliance of model outputs to given prompts and conversation context."},
            {"role": "user", "content": evaluation_prompt}
        ],
        temperature=0.2
    )

    try:
        result = json.loads(response.choices[0].message.content)
        print(f"\n\n\n-----Result: {result}\n\n\n")
        return {
            "key": "prompt_compliance",
            "score": (result["score"] - 1) / 4,  # normalize to 0-1 range
            "reason": result["explanation"]
        }
    except json.JSONDecodeError:
        return {
            "key": "prompt_compliance",
            "score": 0,
            "reason": "Failed to parse evaluator response"
        }


# The name or UUID of the LangSmith dataset to evaluate on.
data = "sophAI_report_output"

# A string to prefix the experiment name with.
experiment_prefix = "astrology_ai_prompt_compliance"

# List of evaluators to score the outputs of target task
evaluators = [
    client_record_accuracy_evaluator
]

# Evaluate the target task
results = evaluate(
    lambda inputs: inputs,
    data=data,
    evaluators=evaluators,
    experiment_prefix=experiment_prefix,
)

print(results)