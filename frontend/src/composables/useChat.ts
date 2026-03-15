import { nextTick, ref } from "vue";
import type { Message } from "../types/chat";
import { ChatAPI } from "../api/chat";

export function useChat() {
  const messages = ref<Message[]>([]);
  const isLoading = ref(false);
  const currentStreamingMessage = ref<Message | null>(null);
  // 用于取消当前的流式请求
  let cancelCurrentStream: (() => void) | null = null;

  /**
   * 滚动到底部
   */
  const scrollToBottom = () => {
    nextTick(() => {
      const chatContainer = document.getElementById("chat-container");
      if (chatContainer) {
        chatContainer.scrollTo({
          top: chatContainer.scrollHeight,
          behavior: "smooth",
        });
      }
    });
  };

  /**
   * 发送消息
   */
  const sendMessage = async (content: string) => {
    if (!content.trim() || isLoading.value) return;
    //1. 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: Date.now(),
    };
    messages.value.push(userMessage);
    // 准备发送给后端的历史记录（去掉刚加上的这一条，后端只要之前的）
    // 或者可以根据设计决定是否包含当前条，通常 API 设计是： 新消息 + 历史
    // 我们后端设计是  message + history，所以这里直接传 messages.value 就行，后端会处理
    const historyPayload = messages.value.slice(0, -1).map((msg) => ({
      role: msg.role,
      content: msg.content,
    }));
    // 2. 创建 AI 消息占位符
    const aiMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: "",
      timestamp: Date.now(),
      streaming: true,
    };
    messages.value.push(aiMessage);
    currentStreamingMessage.value = aiMessage;
    isLoading.value = true;
    scrollToBottom();

    // 3. 调用流式接口
    cancelCurrentStream = ChatAPI.streamChat(
      {
        message: content,
        chat_history: historyPayload,
      },
      // onToken
      (token) => {
        if (currentStreamingMessage.value) {
          currentStreamingMessage.value.content += token;
          scrollToBottom();
        }
      },
      // onComplete
      (fullResponse) => {
        if (currentStreamingMessage.value) {
          // 确保流式消息的内容是完整的
          if (
            currentStreamingMessage.value.content !== fullResponse &&
            fullResponse
          ) {
            currentStreamingMessage.value.content = fullResponse;
          }
          currentStreamingMessage.value.streaming = false;
        }
        currentStreamingMessage.value = null;
        isLoading.value = false;
        cancelCurrentStream = null;
        scrollToBottom();
      },
      // onError
      () => {
        if (currentStreamingMessage.value) {
          currentStreamingMessage.value.content += "\n\n[消息生成被取消]";
          currentStreamingMessage.value.streaming = false;
        }
        currentStreamingMessage.value = null;
        isLoading.value = false;
        cancelCurrentStream = null;
        scrollToBottom();
      },
    );
  };

  /**
   * 清空聊天记录
   */
  const clearMessages = () => {
    if (cancelCurrentStream) {
      cancelCurrentStream();
      cancelCurrentStream = null;
    }
    messages.value = [];
    isLoading.value = false;
    currentStreamingMessage.value = null;
  };

  return {
    sendMessage,
    clearMessages,
    messages,
    isLoading,
  };
}
