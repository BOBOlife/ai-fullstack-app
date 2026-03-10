import asyncio
import json
from models import ChatRequest
from llm_app import LLMApp

#TEST
llm_app = LLMApp()

chat_history = [
    {"role":"user","content":"你好"},
    {"role":"assistant","content":"你好！有什么可以帮助你的吗？"}
]

#模拟用户输入
user_input = "给我简单介绍一下人工智能？"

response_chunks = []

# print("AI助手正在回答：", end="", flush=True)
# for chunk in llm_app.stream_chat(user_input, chat_history):  

#     response_chunks.append(chunk) 
#     # 模拟实时显示
#     print(chunk, end="", flush=True)

# #合并响应
# full_response = "".join(response_chunks)
# print(f"\n完整响应：{full_response}")

# 模拟SSE 的流式响应
async def chat_steam(request: ChatRequest):
    # 1. 发送开始事件
    yield f"data: {json.dumps({'type': 'start'})}\n\n"
    await asyncio.sleep(0.1)  # 让出控制权，以便运行其他任务
    full_response = ""
    # 2. 生成并发送token
    for token in llm_app.stream_chat(request.message, request.conversation_history):
        full_response += token
        yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
        await asyncio.sleep(0.01)  # 模拟生成token的时间
    # 3. 发送结束事件
    yield f"data: {json.dumps({'type': 'end', 'full_response': full_response})}\n\n"

# 异步测试函数
async def test_chat_stream():
    request = ChatRequest(
        message=user_input,
        conversation_history=chat_history
    )
    print("模拟SSE流式响应：")
    async for chunk in chat_steam(request):
        print(chunk, end="", flush=True)


# 在异步编程中，我们使用 asyncio.run 来运行异步函数，作为程序的入口点。
asyncio.run(test_chat_stream())