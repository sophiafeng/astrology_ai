from langsmith.evaluation import evaluate
from langsmith.schemas import Run, Example
from openai import OpenAI
import json
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai

from langsmith import traceable

# Load environment variables
load_dotenv()

client = wrap_openai(OpenAI())

@traceable
def prompt_compliance_evaluator(run: Run, example: Example) -> dict:
    inputs = [ {'data': {'content': example.inputs["question"]}, 'type': 'human'} ]
    outputs = {'data': {'content': example.outputs["answer"]}}

    print(f"\n\nInputs: {inputs}\n\n")
    print(f"\n\nOutputs: {outputs}\n\n")


    # Extract system prompt
    system_prompt = next((msg['data']['content'] for msg in inputs if msg['type'] == 'system'), "")

    # Extract message history
    message_history = []
    for msg in inputs:
        if msg['type'] in ['human', 'ai']:
            message_history.append({
                "role": "user" if msg['type'] == 'human' else "assistant",
                "content": msg['data']['content']
            })

    # Extract latest user message and model output
    latest_message = message_history[-1]['content'] if message_history else ""
    model_output = outputs['data']['content']

    evaluation_prompt = f"""
    System Prompt: {system_prompt}

    Message History:
    {json.dumps(message_history, indent=2)}

    Latest User Message: {latest_message}

    Model Output: {model_output}

    Based on the above information, evaluate the model's output for compliance with the system prompt and context of the conversation. 
    Give your answer on a scale of 1 to 5, where 1 means that the model_output is not helpful at all and is completely irrelevant to the latest_message, or very partial, and 5 means that the model_output completely and helpfully addresses the latest_message.

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
data = "astrology dataset 2"

# A string to prefix the experiment name with.
experiment_prefix = "astrology_ai_prompt_compliance"

# List of evaluators to score the outputs of target task
evaluators = [
    prompt_compliance_evaluator
]

# Evaluate the target task
results = evaluate(
    lambda inputs: inputs,
    data=data,
    evaluators=evaluators,
    experiment_prefix=experiment_prefix,
)

print(results)