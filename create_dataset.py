from langsmith import Client

client = Client()
dataset_name = "astrology dataset"

inputs = [
    "My birthday is July 13. What's my horoscope?",
]

outputs = [
    "Your zodiac sign, based on the Gregorian calendar, would be Cancer. If you were born between June 21 and July 22, you would be a Cancer according to Western astrology. This is because the sun was in the constellation of Cancer during that time. However, it's important to note that astrology is not a science and should be taken as a form of entertainment rather than a predictor of personal traits or future events.",
]

# Store
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="QA pairs about astrology.",
)
client.create_examples(
    inputs=[{"question": q} for q in inputs],
    outputs=[{"answer": a} for a in outputs],
    dataset_id=dataset.id,
)