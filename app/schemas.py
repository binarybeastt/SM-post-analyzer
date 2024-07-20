from pydantic import BaseModel
from typing import Dict

class PostData(BaseModel):
    degree: str
    post: Dict
