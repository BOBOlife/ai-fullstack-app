import type { ChatRequest, SSEEvent } from "../types/chat";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export class ChatAPI {
  /**
   * 流式对话接口
   */

  static streamChat(
    payload: ChatRequest,
    onToken: (token: string) => void,
    onComplete: (fullResponse: string) => void,
    onError: (error: string) => void,
  ): () => void {
    // 使用fetch API配合ReadableStream来处理 POST 请求的流式响应
    //因为标准 EventSource 不支持 POST 请求，所以我们需要自己实现流式处理
    const controller = new AbortController();
    const signal = controller.signal;
    const fetchStream = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
          signal,
        });

        if (!response.ok || !response.body) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder("utf-8");
        let fullResponse = "";
        if (!reader) {
          throw new Error("Failed to get reader from response body");
        }
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;

          // 处理 SSE 格式的数据
          let lines = buffer.split("\n");
          buffer = lines.pop() || ""; // 最后一行可能不完整，保留在 buffer 中

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const dataStr = line.slice(6);
              try {
                const data: SSEEvent = JSON.parse(dataStr);
                switch (data.type) {
                  case "start":
                    // 可以在这里处理对话开始的事件，例如显示加载动画
                    break;
                  case "token":
                    if (data.content) onToken(data.content);
                    break;
                  case "end":
                    if (data.full_response) {
                      fullResponse = data.full_response!;
                      onComplete(fullResponse);
                    }
                    return; // 对话结束，退出循环
                  case "error":
                    onError(data.message || "Unknown error");
                    return; // 出现错误，退出循环
                }
              } catch (error) {
                console.error("Failed to parse SSE data:", error);
              }
            }
          }
        }
      } catch (error) {
        console.error("Failed to fetch stream:", error);
      }
    };
    fetchStream();
    return () => controller.abort(); // 返回一个函数，用于取消请求
  }
  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      return await response.json();
    } catch (error) {
      console.error("Health check failed:", error);
      return { status: "error", message: "Health check failed" };
    }
  }
}
