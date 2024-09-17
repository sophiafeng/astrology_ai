from langsmith.evaluation import evaluate
from langsmith.schemas import Run, Example
from openai import OpenAI
import json
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from prompts import ASSESSMENT_PROMPT

from langsmith import traceable

# Load environment variables
load_dotenv()

# Define AI system
client = wrap_openai(OpenAI())

@traceable
def horoscope_suggestion_relevance_evaluator(run: Run, example: Example) -> dict:
    inputs = example.inputs["message_history"]
    model_output = example.outputs['output']
    print(f"\n\n-----------Inputs: {inputs}\n\n")
    print(f"\n\n-----------Outputs: {model_output}\n\n")

    # Extract system prompt
    system_prompt = next((msg['content'] for msg in inputs if msg['role'] == 'system'), "")
    print(f"\n\n-----------System Prompt: {system_prompt}\n\n")

    # Extract message history
    message_history = []
    for msg in inputs:
        if msg['role'] in ['user', 'assistant']:
            message_history.append({
                "role": msg['role'],
                "content": msg['content']
            })

    # # Extract latest user message and model output
    # latest_message = message_history[-1]['content'] if message_history else ""
    # print(f"\n\n-----------Latest User Message: {latest_message}\n\n")

    evaluation_prompt = f"""
    System Prompt: {system_prompt}

    Assessment Prompt: {ASSESSMENT_PROMPT}

    Message History:
    {json.dumps(message_history, indent=2)}

    Model Output: {model_output}

    Based on the above information, evaluate the model's output for relevance of client record based on System Prompt, Assessment Prompt, and Message History. 
    Give your answer on a scale of 1 to 5, with the following guidelines:
        5: model_output contains entirely relevant suggestions that came up in the conversation in message_history
        4: model_output contains mostly relevant suggestions that came up in the conversation in message_history
        3: model_output contains some relevant suggestions that came up in the conversation in message_history
        2: model_output contains little to no relevant suggestions based on conversation in message_history
        1: model_output contains entirely irrelevant suggestions based on conversation in message_history

    Also provide a brief explanation for your score.

    Respond in the following JSON format:
    {{
        "score": <int>,
        "explanation": "<string>",
        "irrelevant_suggestions": ["<string>", "<string>", "..."],
        "missed_suggestions": ["<string>", "<string>", "..."]
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


@traceable
def daily_horoscope_summary_accuracy_evaluator(run: Run, example: Example) -> dict:
    pass


# The name or UUID of the LangSmith dataset to evaluate on.
data = "daily-horoscope"

# A string to prefix the experiment name with.
experiment_prefix = "horoscope_suggestion_relevance"

# List of evaluators to score the outputs of target task
evaluators = [
    horoscope_suggestion_relevance_evaluator
]

# Evaluate the target task
results = evaluate(
    lambda inputs: inputs,
    data=data,
    evaluators=evaluators,
    experiment_prefix=experiment_prefix,
)

print(results)