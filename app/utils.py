import json
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def load_json(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def preprocess_data(data: dict) -> dict:
    """Preprocess the data to keep only non-empty keys."""
    return {k: v for k, v in data.items() if v not in [None, "", 0, "0"]}

def preprocess_data_list(data_list: list) -> list:
    """Preprocess a list of dictionaries to keep only non-empty keys in each dictionary, 
       and limit the list to the first two dictionaries."""
    preprocessed_data = [preprocess_data(data) for data in data_list]
    return preprocessed_data[:2]  # Keep only the first two dictionaries

def generate_analysis(data: dict, degree: str, comparison_files: dict) -> str:
    # Preprocess the input data to keep only non-empty keys
    filtered_data = preprocess_data(data)
    
    # Adjust the engagement rate if it is a decimal
    if 'Engagement Rate' in filtered_data:
        try:
            engagement_rate = float(filtered_data['Engagement Rate'])
            if engagement_rate < 1:
                filtered_data['Engagement Rate'] = engagement_rate * 100
        except ValueError:
            pass  # If conversion fails, leave the engagement rate as it is

    # Determine which comparison file to use based on the degree
    if degree == 'excellent':
        comparison_file = comparison_files['average']
    else:
        comparison_file = comparison_files['excellent']
    
    # Load and preprocess comparison data, limiting to the first two dictionaries
    comparison_data_list = preprocess_data_list(load_json(comparison_file))
    comparative_data_str = "\n".join([f"Post {i+1}: {post}" for i, post in enumerate(comparison_data_list)])

    if degree == 'excellent':
        objective = ("explain why this post performs better than other posts in the average category, focusing on high engagement rate or other positive metrics. "
                     "The analysis should provide reasons such as engaging content, captivating media, or the hashtag in the caption, "
                     "and compare it with average posts.")
    else:
        objective = ("explain why this post is not performing as well as excellent posts. "
                     "The analysis should compare it with excellent posts to highlight the differences and suggest improvements.")

    prompt = f"""
    Analyze the provided data about a social media post and {objective}.
    Only use the data provided below for your analysis, don't talk about any other data if it's not provided. The comment should be concise and limited to 2 to 3 sentences.
    When explaining, avoid stating the figures explicitly. Instead, describe the performance in qualitative terms, take note of the terms, some terms are exclusive to different social media platforms.
    For example, don't use the term retweet when talking about Instagram, that's only for Twitter.

    Data: {filtered_data}

    Comparative Data:
    {comparative_data_str}
    """

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a social media analyst, skilled in evaluating social media posts."},
            {"role": "user", "content": prompt}
        ]
    )
    
    response = completion.choices[0].message.content
    return response
