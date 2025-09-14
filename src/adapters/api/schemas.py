from pydantic import BaseModel, Field
from typing import List, Literal, Optional


Role = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    temperature: Optional[float] = None
    max_new_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    reply: str

