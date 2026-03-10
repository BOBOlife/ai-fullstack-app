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

class HealthResponse(BaseModel):
    # 健康检查响应模型
    status: str
    model: Optional[str] = None
    api_configured: Optional[bool] = None
    timestamp: Optional[str] = None