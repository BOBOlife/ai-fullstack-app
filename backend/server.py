from time import process_time
from fastapi import FastAPI, Request
from typing import Optional, List
import re
from pydantic import BaseModel, Field, validator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
    allow_credentials=True,  # 允许携带凭证（如Cookies）
)

@app.get("/")
def read_root():
    return {"message": "环境运行成功"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello, World!"}

@app.get("/items/{id}")
def read_item(
    id: int,
    limit: int = 10,    #默认值为10
    q: Optional[str] = None, #可选参数q，类型为字符串，默认值为None
    short : bool = False,   #布尔类型参数short，默认值为False
    tags: List[str] = []  #列表类型参数tags，默认值为空列表
):
    item = { "id": id, "limit": limit, "tags": tags}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"desc": "长说明"})
    return item


# 请求体（Request Body）
class UserRequest(BaseModel):  
    username:str= Field(..., min_length=3, max_length=50)  
    password:str  
    email:str  
    @validator('username')
    def username_alphanumeric(cls, v):  
        if not re.match('^[a-zA-Z0-9_]+$', v):
            raise ValueError('只能包含字母、数字和下划线')   
        return v  
    @validator('email') 
    def email_valid(cls, v):   
        if '@' not in v:     
            raise ValueError('无效的邮箱地址')   
        return v.lower() # 转换为小写  
    @validator('password') 
    def password_strong(cls, v):   
        if len(v) <6:     
            raise ValueError('密码至少6位')   
        return v 

# 响应模型（Response Model）
class UserResponse(BaseModel):  
    username:str  
    email:str

@app.post("/user/", response_model=UserResponse)
async def create_user(user: UserRequest): # 密码会被过滤，不会出现在响应中 
    return user


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(process_time())
    print(f"处理请求 {request.url.path} 的时间: {str(process_time())} 秒")
    return response  # 模





# 程序的入口点

if __name__ == "__main__":  
    import uvicorn   
    uvicorn.run("server:app", host="127.0.0.1", port=3000, reload=True)  # 启动服务器，监听