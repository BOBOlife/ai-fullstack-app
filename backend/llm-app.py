import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv() # 加载环境变量

llm = ChatOpenAI(
    model="deepseek-chat", # 模型名称
    api_key=os.getenv("DEEPSEEK_API_KEY"), # 从环境变量获取 API 密钥
    base_url="https://api.deepseek.com/", # API 基础 URL
    temperature=0.7, # 生成文本的随机程度，值越高越随机
)
system = SystemMessagePromptTemplate.from_template("你是一个心灵导师。") # 定义一个系统消息提示模板
human = HumanMessagePromptTemplate.from_template("{question}") # 定义一个人类消息提示模板
prompt = ChatPromptTemplate.from_messages([system, human]) # 定义一个简单的聊天提示模板

parser = StrOutputParser() # 定义一个字符串输出解析器
# LCEL语法示例：{question} 是一个占位符，表示用户输入的问题。这个提示模板会将用户的问题传递给 LLM 进行处理。   
chain = prompt | llm | parser # 将提示、LLM和解析器组合成一个链
# 等价于：输入 -> 模版填充 -> LLM处理 -> 输出解析
result = chain.invoke({"question": "你是谁?"}) # 调用链，传入用户问题

print(result) # 输出结果
