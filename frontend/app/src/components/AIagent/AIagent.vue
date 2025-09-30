<script>
import axios from "axios";
import { nextTick } from "vue";

export default {
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      messages: [
        {
          role: "assistant",
          text: "Hello! How can I assist you today?",
          isIntro: true,
        },
      ],
      inputMessage: "",
      isConfigMode: false,
      apiKey: localStorage.getItem("aiOverrideApiKey") || "",
      isLoading: false,
      errorMessage: "",
    };
  },
  methods: {
    async sendMessage() {
      const content = this.inputMessage.trim();
      if (!content || this.isLoading) return;

      // Add user message
      this.messages.push({ role: "user", text: content });
      this.inputMessage = "";
      this.errorMessage = "";
      this.isLoading = true;
      await this.scrollToBottom();

      try {
        const history = this.messages
          .filter((message, index) => !(index === 0 && message.isIntro))
          .slice(-12)
          .map((message) => ({
            role: message.role,
            content: message.text,
          }));

        const payload = {
          messages: history,
        };

        if (history.length === 1 && history[0].role === "user") {
          payload.situation = history[0].content;
        }

        const overrideKey = this.apiKey.trim();
        if (overrideKey) {
          payload.api_key_override = overrideKey;
        }

        const token = localStorage.getItem("token");
        const headers = {
          "Content-Type": "application/json",
        };
        if (token) {
          headers.Authorization = `Bearer ${token}`;
        }

        const baseUrl = this.apiUrl?.trim();
        const sanitizedBase = baseUrl?.replace(/\/+$/, "") || "";
        const endpoint = sanitizedBase
          ? `${sanitizedBase}/ai/chat`
          : "/api/ai/chat";

        const response = await axios.post(endpoint, payload, { headers });
        const reply = response?.data?.reply?.trim();

        this.messages.push({
          role: "assistant",
          text: reply || "I'm here to help, but I couldn't generate a response.",
        });
      } catch (error) {
        console.error("AI chat failed", error);
        const detail =
          error?.response?.data?.detail || error?.message || "Error connecting to server";
        this.errorMessage = typeof detail === "string" ? detail : JSON.stringify(detail);
        this.messages.push({
          role: "assistant",
          text: "I ran into an issue generating a response. Please try again.",
        });
      }
      this.isLoading = false;
      await this.scrollToBottom();
    },
    saveApiKey() {
      localStorage.setItem("aiOverrideApiKey", this.apiKey.trim());
      this.isConfigMode = false;
    },
    scrollToBottom() {
      nextTick(() => {
        const chatContainer = this.$refs.chatList;
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      });
    },
  },
};
</script>

<template>
  <div class="content-section flex flex-col h-screen bg-gray-900 text-white md:ml-64 " >
    <!-- Header -->
    <div class="fixed w-full flex items-center top-0 px-6 py-4 bg-gray-800">
      <div class="text-2xl font-bold">ChatGPT</div>
      <div class="ml-auto text-sm cursor-pointer hover:bg-gray-700 px-3 py-2 rounded-md" @click="isConfigMode = !isConfigMode">
        Settings
      </div>
    </div>

    <!-- Chat Messages -->
    <div ref="chatList" class="flex-1 overflow-y-auto p-4 mt-16 mb-20 space-y-4">
      <div v-for="(msg, index) in messages" :key="index"
        class="p-3 rounded-lg max-w-xl whitespace-pre-line"
        :class="msg.role === 'user' ? 'bg-blue-600 self-end ml-auto' : 'bg-gray-700 self-start mr-auto'">
        {{ msg.text }}
      </div>
      <div v-if="isLoading" class="flex items-center space-x-3 text-sm text-gray-300">
        <span class="inline-flex h-4 w-4 animate-spin rounded-full border-2 border-current border-r-transparent"></span>
        <span>Thinking...</span>
      </div>
    </div>

    <!-- Settings Mode -->
    <div v-if="isConfigMode" class="p-6 bg-gray-800 border-t border-gray-700">
      <div class="text-sm text-gray-400 mb-2">Enter API Key:</div>
      <div class="flex">
        <input v-model="apiKey" class="flex-1 p-2 bg-gray-700 text-white rounded-lg outline-none" type="password" placeholder="sk-xxxxxxxxxx"/>
        <button @click="saveApiKey" class="ml-2 px-4 py-2 bg-green-500 rounded-lg">Save</button>
      </div>
    </div>

    <!-- Input Box -->
    <div v-else class="fixed bottom-0 w-[1350px] p-6 bg-gray-800 border-t border-gray-700 flex flex-col space-y-3">
      <div v-if="errorMessage" class="rounded-md bg-red-500/10 border border-red-500/40 text-red-200 text-sm px-3 py-2">
        {{ errorMessage }}
      </div>
      <div class="flex items-center">
        <input
          v-model="inputMessage"
          @keydown.enter.prevent="sendMessage"
          class="flex-1 p-2 bg-gray-700 text-white rounded-lg outline-none"
          placeholder="Describe the customer situation or ask a CRM question..."
        />
        <button
          @click="sendMessage"
          class="ml-2 px-4 py-2 bg-blue-500 rounded-lg disabled:opacity-70 disabled:cursor-not-allowed"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Generating...' : 'Send' }}
        </button>
      </div>
    </div>
  </div>
</template>
