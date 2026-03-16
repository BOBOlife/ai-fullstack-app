# AI 全栈应用

这是一个基于 Vue.js 前端和 Python FastAPI 后端的 AI 全栈应用。项目集成了大语言模型（LLM），提供聊天和智能代理功能。

## 功能特性

- **前端界面**：使用 Vue 3 和 TypeScript 构建的现代化用户界面
- **后端服务**：基于 FastAPI 的高性能 Python 后端
- **AI 集成**：集成大语言模型，支持智能对话和代理功能
- **实时通信**：前后端通过 API 进行实时数据交互

## 技术栈

### 前端

- Vue 3.5.30
- TypeScript
- Vite 8.0.0
- @vitejs/plugin-vue
- vue-tsc

### 后端

- **Python 3.14+**：核心编程语言
- **FastAPI**：现代化的高性能 Web 框架，支持异步处理和自动 API 文档生成
- **Uvicorn**：ASGI 服务器，用于运行 FastAPI 应用
- **LangChain**：用于构建 LLM 应用的框架，提供链式调用、提示模板等功能
- **LangChain-OpenAI**：LangChain 的 OpenAI 集成，支持多种 LLM 模型
- **DeepSeek API**：使用的具体 LLM 模型，通过自定义 base_url 集成
- **python-dotenv**：环境变量管理，用于安全存储 API 密钥等敏感信息
- **Pytest**：测试框架，用于编写和运行单元测试

#### 核心功能模块

- **LLMApp 类**：封装 LLM 逻辑，支持流式和非流式响应
- **智能代理 (Agent)**：使用 LangChain Agents 框架，实现工具调用和复杂任务处理
- **自定义工具 (Tools)**：如搜索和天气查询工具，扩展 AI 能力
- **流式响应**：支持实时对话，通过 StreamingResponse 实现
- **CORS 中间件**：处理跨域请求，支持前后端分离部署

## 项目结构

````
ai-fullstack-app/
├── backend/                 # Python 后端
│   ├── agent.py            # AI 代理逻辑
│   ├── llm_app.py          # LLM 应用核心
│   ├── main.py             # 应用入口
│   ├── models.py           # 数据模型
│   ├── server.py           # 服务器配置
│   └── pyproject.toml      # Python 项目配置
├── frontend/                # Vue 前端
│   ├── src/
│   │   ├── components/     # Vue 组件
│   │   ├── composables/    # Vue 组合式 API
│   │   ├── types/          # TypeScript 类型定义
│   │   └── api/            # API 调用模块
│   ├── public/             # 静态资源
│   └── package.json        # Node.js 项目配置
## 环境准备

### 安装 uv 包管理器

本项目使用 `uv` 作为 Python 包管理器。如果您还没有安装 uv，请使用以下命令安装：

**macOS (使用 Homebrew)**:
```bash
brew install uv
````

**其他系统**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装完成后，验证 uv 是否正常工作：

```bash
uv --version
```

## 安装和运行

### 后端安装

1. 进入后端目录：

   ```bash
   cd backend
   ```

2. 安装依赖：

   ```bash
   uv pip install -e .
   ```

3. 运行后端服务：
   ```bash
   uv run python server.py
   # 或者使用 uvicorn 直接启动
   uvicorn server:app --reload
   ```

### 前端安装

1. 进入前端目录：

   ```bash
   cd frontend
   ```

2. 安装依赖：

   ```bash
   pnpm install
   ```

3. 运行开发服务器：
   ```bash
   pnpm dev
   ```

## 使用说明

1. 启动后端服务（默认端口 8080）
2. 启动前端开发服务器（默认端口 5173）
3. 在浏览器中访问前端界面
4. 开始与 AI 进行对话

## API 文档

后端启动后，可以访问 `http://localhost:8080/docs` 查看自动生成的 API 文档。

## 开发说明

- 后端使用 FastAPI，支持异步处理和高并发
- 前端使用 Vue 3 Composition API 和 TypeScript
- 支持热重载开发模式

## 未来计划

本项目将持续升级和开发，实现更多 AI 应用功能，包括但不限于：

- 扩展智能代理功能，支持更多类型的工具和任务
- 集成多种大语言模型，提供更丰富的对话体验
- 添加用户界面增强功能，如聊天历史管理、主题切换等
- 实现多用户支持和数据持久化
- 探索更多 AI 应用场景，如代码生成、文档分析等

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
