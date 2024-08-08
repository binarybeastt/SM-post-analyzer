from pydantic import BaseModel
from typing import Dict, List

class PostData(BaseModel):
    degree: str
    post: Dict

class MultiplePostData(BaseModel):
    posts: List[Dict]
    degrees: List[str]
