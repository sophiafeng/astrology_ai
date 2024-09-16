from langsmith import Client

client = Client()
dataset_name = "astrology dataset 2"

inputs = [
    "My birthday is July 13. What's my horoscope?",
    "What job should I get based on my horoscope?",
    "I'm a Cancerian. What should I do today?",
]

outputs = [
    "Your zodiac sign, based on the Gregorian calendar, would be Cancer. If you were born between June 21 and July 22, you would be a Cancer according to Western astrology. This is because the sun was in the constellation of Cancer during that time. However, it's important to note that astrology is not a science and should be taken as a form of entertainment rather than a predictor of personal traits or future events.",
    """
As an AI, I don't know your personal interests, skills, experiences, or goals, which are all important factors in choosing a job. However, if you're a Cancer as per the zodiac, you're typically known for being intuitive, empathetic, and caring. These traits are often well-suited to careers in:

Healthcare: Such as nursing, therapy, or counseling where you can use your caring nature to help others.
Social Work: Your empathy and desire to help can be a great asset in this field.
Education: Teaching or child care could be a good fit, as Cancers often have a nurturing nature.
Arts: Many Cancers are also highly creative. You might thrive in a career as a writer, painter, musician, or designer.
Hospitality: Jobs in hospitality or food service, such as a chef or hotel manager, could be a good fit for Cancers who enjoy making others feel comfortable and cared for.
Remember, these are just suggestions based on typical traits of the Cancer zodiac sign. It's important to consider your personal interests, skills, and passions when choosing a career.
""",
    "Cancerians are known for their emotional intelligence and their strong connection to their home and family. Today, consider spending quality time with your loved ones. You could organize a family game night or cook a special meal for them. Alternatively, you could also spend some time redecorating or reorganizing your home to make it more comfortable and inviting. Self-care is also important, so don't forget to take some time for yourself. You could take a relaxing bath, read a book, or do anything else that helps you relax and recharge."

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