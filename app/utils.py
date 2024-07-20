from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_analysis(data: dict, degree: str) -> str:
    if degree == 'excellent':
        objective = "make AI-based comments on why the excellent post is performing well"
    else:
        objective = "make AI-based comments on why the post is not creating an impact or audience, and what is missing from these posts"
    
    prompt = f"""
    Analyze the provided data about a social media post and {objective}.
    Only use the data provided below for your analysis. The comment should be concise and limited to 2 to 3 sentences.
    Data: {data}
    """
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a social media analyst, skilled in evaluating social media posts."},
        {"role": "user", "content": prompt}
    ]
    )

    response=completion.choices[0].message.content
    return response
