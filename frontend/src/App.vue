<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { ChatAPI } from "./api/chat";
import { useChat } from "./composables/useChat";

const inputContent = ref("");
const textareaRef = ref<HTMLTextAreaElement | null>(null);
const isServerOnline = ref(false);
const { messages, isLoading, sendMessage, clearMessages } = useChat();

// 检查服务器状态
onMounted(async () => {
  const health = await ChatAPI.healthCheck();
  console.log("🐸🔥 ~ health:", health);
  isServerOnline.value = health.status === "healthy";
});

// 自动调整输入框高度
watch(inputContent, () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = "auto";
    textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`;
  }
});

const handleSend = () => {
  if (inputContent.value.trim() && !isLoading.value) {
    sendMessage(inputContent.value.trim());
    inputContent.value = "";
    // 重制高度
    if (textareaRef.value) {
      textareaRef.value.style.height = "auto";
    }
  }
};
</script>

<template>
  <div class="app-container">
    <header class="chat-header">
      <div>DeepSeek 对话助手</div>
      <div class="status-badge" :class="{ online: isServerOnline }">
        {{ isServerOnline ? "在线" : "离线" }}
      </div>
      <button @click="clearMessages" class="clear-btn" title="清空消息">
        CLEAR
      </button>
    </header>
    <main class="message-list">
      <div v-if="messages.length === 0" class="empty-state">
        <p>👋 你好！我是基于DeepSeek的AI 助手</p>
        <p>请在下方输入你的问题，我会尽力帮助你！</p>
      </div>
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message-wrapper"
        :class="msg.role"
      >
        <div class="avatar">
          {{ msg.role === "user" ? "👤" : "🤖" }}
        </div>
        <div class="message-content">
          <div class="bubble">
            {{ msg.content }}
            <span v-if="msg.streaming" class="cursor">|</span>
          </div>
        </div>
      </div>
    </main>
    <footer class="input-area">
      <div class="input-container">
        <textarea
          v-model="inputContent"
          placeholder="输入消息...（Enter 发送， Shift + Enter 换行）"
          @keydown.enter.exact.prevent="handleSend"
          :disabled="isLoading"
          rows="1"
          ref="textareaRef"
        ></textarea>
        <button
          @click="handleSend"
          :disabled="isLoading || !inputContent.trim()"
          class="send-btn"
        >
          {{ isLoading ? "..." : "发送" }}
        </button>
      </div>
    </footer>
  </div>
</template>

<style>
:root {
  --primary-color: #4a90e2;
  --bg-color: #f5f7fa;
  --chat-bg: #ffffff;
  --user-msg-bg: #e1f5fe;
  --bot-msg-bg: #f0f0f0;
  --border-color: #e0e0e0;
}
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu,
    Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  background-color: var(--bg-color);
  height: 100vh;
  overflow: hidden;
}
.app-container {
  max-width: 800px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--chat-bg);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}
/* Header */
.chat-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  z-index: 10;
}
.header-content h1 {
  font-size: 1.2rem;
  color: #333;
}
.status-badge {
  font-size: 0.8rem;
  padding: 2px 6px;
  border-radius: 4px;
  background: #ff5252;
  color: white;
  display: inline-block;
  margin-left: 8px;
}
.status-badge.online {
  background: #4caf50;
}
.clear-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 5px;
  border-radius: 50%;
  transition: background 0.2s;
}
.clear-btn:hover {
  background: #f0f0f0;
}
/* Message List */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.empty-state {
  text-align: center;
  margin-top: 50px;
  color: #888;
}
.message-wrapper {
  display: flex;
  gap: 12px;
  max-width: 85%;
}
.message-wrapper.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}
.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.bubble {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}
.message-wrapper.user .bubble {
  background: var(--user-msg-bg);
  color: #0d47a1;
  border-radius: 12px 2px 12px 12px;
}
.message-wrapper.assistant .bubble {
  background: var(--bot-msg-bg);
  color: #333;
  border-radius: 2px 12px 12px 12px;
}
.cursor {
  display: inline-block;
  width: 2px;
  height: 1em;
  background: #333;
  animation: blink 1s infinite;
  vertical-align: middle;
}
@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
/* Input Area */
.input-area {
  padding: 20px;
  border-top: 1px solid var(--border-color);
  background: white;
}
.input-container {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}
textarea {
  flex: 1;
  color: #000;
  border: none;
  background: transparent;
  resize: none;
  max-height: 150px;
  padding: 8px;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
}
.send-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.2s;
}
.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
