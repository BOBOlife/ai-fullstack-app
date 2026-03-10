type Role = "user" | "assistant";
export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: number;
  stream?: boolean; // 是否正在流式生成
}

export interface ChatRequest {
  message: string;
  conversation_history: Array<{ role: Role; content: string }>;
}

export interface SSEEvent {
  type: "token" | "start" | "end" | "error";
  content?: string; // token内容
  full_response?: string; // 完整响应（仅在end事件中提供）
  message?: string; // 错误信息（仅在error事件中提供）
}
