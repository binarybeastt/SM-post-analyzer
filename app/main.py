from fastapi import FastAPI, HTTPException
from app.schemas import PostData, MultiplePostData
from app.utils import generate_analysis, compare_multiple_posts
from app.config import settings

app = FastAPI()
comparison_files = {
    'excellent': 'excellentPosts.json',
    'good': 'goodPosts.json',
    'average': 'averagePosts.json'
}

@app.post("/analyze")
async def analyze_post(post_data: PostData):
    degree = post_data.degree
    post = post_data.post

    if degree not in settings.ALLOWED_DEGREES:
        raise HTTPException(status_code=400, detail="Invalid degree type. Must be 'excellent', 'average', or 'good'.")

    analysis = generate_analysis(data=post, degree=degree, comparison_files=comparison_files)
    
    return {"comment": analysis}

@app.post("/analyze_multiple_post")
async def analyze_multiple_posts(post_data: MultiplePostData):
    posts = post_data.posts
    degrees = post_data.degrees

    if len(posts) != len(degrees):
        raise HTTPException(status_code=400, detail="The number of posts and degrees must match.")

    for degree in degrees:
        if degree not in settings.ALLOWED_DEGREES:
            raise HTTPException(status_code=400, detail="Invalid degree type. Must be 'excellent', 'average', or 'good'.")
        
    multi_analysis = compare_multiple_posts(posts=posts, degrees=degrees)
    return {"comment": multi_analysis}

