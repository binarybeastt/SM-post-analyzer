from fastapi import FastAPI, HTTPException
from app.schemas import PostData
from app.utils import generate_analysis
from app.config import settings

app = FastAPI()

@app.post("/analyze")
async def analyze_post(post_data: PostData):
    degree = post_data.degree
    post = post_data.post

    if degree not in settings.ALLOWED_DEGREES:
        raise HTTPException(status_code=400, detail="Invalid degree type. Must be 'excellent', 'average', or 'good'.")

    analysis = generate_analysis(data=post, degree=degree)
    
    return {"comment": analysis}
