from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_analysis(data: dict, degree: str) -> str:
    relevant_keys = {
        'twitter': [
            'Engagement', 'Engagement Rate', 'Comments', 'Impressions', 'Likes', 'Quote Retweets', 
            'Retweets', 'Saves', 'Shares', 'Bookmarks', 'Post URL', 'Number of Words in Caption', 
            'Post Clicks', 'Reach', 'Creation Date'
        ],
        'instagram': [
            'Engagement', 'Engagement Rate', 'Comments', 'Impressions', 'Likes', 'Saves', 
            'Shares', 'instagramImage', 'instagramThumbnail', 'Media Type', 'Number of Media', 
            'Number of Words in Caption', 'Post URL', 'Reach', 'Creation Date'
        ],
        'facebook': [
            'Engagement', 'Engagement Rate', 'Comments', 'Impressions', 'Likes', 
            'Shares', 'Facebook Media URLs', 'Facebook Reactions Total', 'facebookImage', 
            'facebookMedia', 'Media Type', 'Number of Words in Caption', 'Post URL', 'Reach', 'Creation Date'
        ],
        'linkedIn': [
            'Engagement', 'Engagement Rate', 'Comments', 'Impressions', 'Likes', 
            'Shares', 'LinkedIn Media URLs', 'LinkedIn Reactions Total', 'LinkedIn Unique Impressions', 
            'linkedinMediaId', 'linkedinMultiImageId', 'Media Type', 'Number of Words in Caption', 
            'Post URL', 'Reach', 'Creation Date'
        ],
    }
    platform = data.get('Social Media', '')
    keys = relevant_keys.get(platform, [])
    filtered_data = {k: v for k, v in data.items() if k in keys and v not in [None, "", 0, "0"]}
    
    if degree == 'excellent':
        objective = "explain why this excellent post performs better than other posts, don't suggest how it can be improved"
    else:
        objective = "explain why this post is not creating an impact or audience, and suggest how it can be improved upon."

    prompt = f"""
    Analyze the provided data about a social media post from {platform} and {objective}.
    Only use the data provided below for your analysis, don't talk about any other data if it's not provided. The comment should be concise and limited to 2 to 3 sentences.
    When explaining, avoid stating the figures explicitly. Instead, describe the performance in qualitative terms, take note of the terms, some terms are exclusive to different social media platforms
    for example, don't use the term retweet when talking about instagram, that's only for twitter.
    Data: {filtered_data}
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a social media analyst, skilled in evaluating social media posts."},
            {"role": "user", "content": prompt}
        ]
    )
    
    response = completion.choices[0].message.content
    return response
