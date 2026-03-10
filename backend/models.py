from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    # 单条聊天消息模型
    role: str  # "user" 或 "assistant"
    content: str

class ChatRequest(BaseModel):
    # 聊天请求模型
    message: str  
    conversation_history: Optional[List[ChatMessage]] = []  # 可选的对话历史，默认为空列表