import os
from typing import Generator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv() # 加载环境变量

class LLMApp:
    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.7):
        # 初始化 LLMApp 类，设置模型名称和温度

        # 检查环境变量中是否存在 API 密钥
        if not os.getenv("DEEPSEEK_API_KEY"):
            raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
        # 初始化配置
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/"
        # 初始化 非流式 LLM （普通任务）
        self.llm = self.create_llm()
        self.streaming_llm = self.create_llm(streaming=True)  # 流式 LLM 初始化为 
        self.output_parser = StrOutputParser() # 输出解析器
        self._setup_chains()

    def create_llm(self, streaming: bool = False):
        # 创建一个 LLM 实例
        return ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
        )
    def _setup_chains(self):
        # 带上下文的对话Prompt
        conversation_prompt = PromptTemplate(
            input_variables=["conversation_history", "user_input"],
            template="""你是一个实用的AI助手。请根据对话历史回答用户的问题。
            对话历史：{conversation_history}
            用户问题：{user_input}
            助手：""",
        )
        self.conversation_prompt = conversation_prompt
    
    def format_history(self, history_list) -> str:
        # 格式化对话历史
        if not history_list:
            return "无历史对话"
        formatted_history = []
        for msg in history_list:
            if isinstance(msg, str):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
            else:
                role = getattr(msg, "role", "unknown")
                content = getattr(msg, "content", "")
            formatted_history.append(f"{role}: {content}")
        return "\n".join(formatted_history[-10:])  # 只保留最近的10条对话历史
    
    def stream_chat(self, user_input: str, conversation_history: list) -> Generator[str, None, None]:
        # 流式聊天生成器
        try:
            history_text = self.format_history(conversation_history)
            # 构建链 Prompt ｜ Streaming LLM ｜ 输出解析器
            chain = self.conversation_prompt | self.streaming_llm | self.output_parser
            for chunk in chain.stream({
                "conversation_history": history_text,
                "user_input": user_input
            }):
                yield chunk
        except Exception as e:
            print(f"Error occurred: {e}")