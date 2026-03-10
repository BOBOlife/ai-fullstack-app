import json 
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from llm_app import LLMApp
from datetime import datetime
from models import HealthResponse, ChatRequest


app = FastAPI(title="AI 对话助手", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
    allow_credentials=True,  # 允许携带凭证（如Cookies）
)

# 全局 LLMApp 实例
llm_app = None

@app.on_event("startup")
async def startup_event():
    global llm_app
    try:
        print("正在初始化 LLMApp...")
        llm_app = LLMApp()  # 在应用启动时初始化 LLMApp 实例
        print("LLMApp 初始化成功")
    except Exception as e:
        print(f"LLMApp 初始化失败: {e}")
        raise HTTPException(status_code=500, detail="LLMApp 初始化失败")

@app.get("/api/health")
async def health_check():
    return HealthResponse(
        status="healthy" if llm_app else "unhealthy",
        model="deepseek-chat",
        api_configured=llm_app is not None,
        timestamp=datetime.now().isoformat()
    )

@app.get("/")
def read_root():
    return {"message": "环境运行成功"}

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    if not llm_app:
        raise HTTPException(status_code=503, detail="LLMApp 未初始化")
    async def generate():
        try:
            # 1. 发送开始事件
            yield f"data: {json.dumps({'type': 'start'})}\n\n"
            await asyncio.sleep(0.01)  # 让出控制权，以便运行其他任务
            full_response = ""
            # 2. 生成并发送token
            # 注意：llm_app.stream_chat 是同步生成器，但在 FastAPI 中可以正常工作            
            # 如果需要完全异步，需要使用 AsyncChatOpenAI，这里为了简单保持同步调用
            for token in llm_app.stream_chat(request.message, request.conversation_history):
                full_response += token
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
                await asyncio.sleep(0.01)  # 模拟生成token的时间
                print(f"Generated token: {token}")  # 调试输出
            # 3. 发送结束事件
            yield f"data: {json.dumps({'type': 'end', 'full_response': full_response})}\n\n"
        except Exception as e:
            print(f"Error in chat_stream: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8080, reload=True)