<template>
  <div id="app" class="main-container">
    <!-- Sidebar for Active Chats -->
    <div class="sidebar">
      <b>
        <div class="w-40px">
          <select name="" id="" v-model="chatStatusFilter" @change="filterChatsByStatus"
            class="no-border px-3 py-2 text-black" style="font-size: 16px; outline: none;">
            <option value="" selected style="font-size: 16px; color: black;">All Chats</option>
            <option value="true" style="font-size: 16px; color: black;">Active Chats
            </option>

          </select>
        </div>

      </b>
      <ul class="chat-list">
        <ul>
          <li v-for="chat in activeChat" :key="chat.message_id">

            <div class="flex bg-white justify-between rounded-lg p-4 text-black shadow-md"
              @click="ConversationSSE(chat.sender_wa_id), ActiveWaid = chat.sender_wa_id, ActiveWaidName = chat.sender_name">

              <div class="">

                <p><strong>{{ chat.sender_name }}</strong></p>
                <div v-html="truncateMessage(chat.message_content)"></div>
              </div>


              <div class="messageTime">
                <p>{{ chat.last_chat_time.split('T')[1].substring(0, 5) }}</p>
              </div>
            </div>


          </li>
        </ul>
      </ul>
    </div>


    <!-- Chat Area -->
    <div class="chat-area">

      <!-- Chat Header -->
      <div class="chat-header">

        <div class="timer">

          <div class="text-gray-600" v-if="ActiveWaid">
            <i class="bi bi-person-circle" style="font-size: 2.1rem;"></i>
          </div>


          <div class="flex flex-col items-start justify-start w-full text-[14px]  p-3">
            <h3><b>{{ ActiveWaidName }}</b></h3>
            <p style="font-size: 13px; color: rgb(132, 138, 134);"><b>{{ ActiveWaid }}</b></p>
          </div>

          <div class="flex items-start justify-end w-full">
            <span id="currentTime">{{ selectedRemainingTime }}</span>
          </div>

        </div>
      </div>

      <!-- Chat Content Section -->
      <div class="chat-content" id="chatContent" ref="chatContent">
        <div v-html="chatContent"></div>
        <div id="messages">
          <div v-for="(message, index) in selectedchat" :key="message.id">
            <!-- Show Date Separator if Date Changes -->
            <div v-if="shouldShowDate(index)" class="text-center my-2 text-sm text-gray-500">
              <p>{{ formatDate(selectedchat[index].timestamp.split('T')[0]) }}</p>
            </div>

            <!-- Message Bubble -->
            <div :class="{ 'message': true, 'sent-message': message.direction == 'sent' }"
              @contextmenu.prevent="showContextMenu($event, message)">

              <div style="width: 100%;max-width: 300px;">
                <div v-if="message.context_message_id" class="replied-message-context mb-2 text-sm text-gray-600">

                  <div class="replied-message">

                    <p><strong>Replied to:</strong></p>
                    <div class="p-2 border border-gray-300 rounded-md"
                      v-html="getRepliedMessageContent(message.context_message_id)"></div>
                  </div>

                </div>
                <!-- Message Content -->
                <div style="white-space: pre-line; word-wrap: break-word; overflow-wrap: break-word; max-width: 100%" v-html="processMessageContent(message.message_content)"></div>

                <div class="messageTime">
                  <p>{{ message.timestamp.split('T')[1].substring(0, 5) }}</p>
                </div>

              </div>
            </div>

          </div>
          <!-- Custom Context Menu -->
          <div v-if="contextMenuVisible"
            :style="{ top: contextMenuPosition.y + 'px', left: contextMenuPosition.x + 'px' }"
            class="custom-context-menu">
            <ul>
              <li @click="replyToMessage">Reply</li>
            </ul>
          </div>
        </div>

          <!-- AI Draft Preview -->
          <div
            v-if="generatedTemplatePreview && !replyMessage"
            class="message sent-message draft-message"
            style="margin: 15px; border: 2px solid #10b981; background-color: rgba(16, 185, 129, 0.1); max-width: 600px; position: relative; z-index: 1000;"
          >
            <div class="draft-message-wrapper">
              <div class="draft-message-header">
                <span class="draft-chip">🤖 AI Generated Template</span>
                <div class="draft-actions">
                  <button type="button" class="draft-send" @click="sendChatMessage">
                    📤 Send Now
                  </button>
                  <button type="button" class="draft-clear" @click="clearDraftPreview">
                    🗑️ Discard
                  </button>
                </div>
              </div>
              <div class="draft-message-body" v-html="generatedTemplatePreview"></div>
              <div class="messageTime">
                <p>Generated at {{ formatTime(draftGeneratedAt) }}</p>
              </div>
            </div>
          </div>

      </div>
      
      <!-- Message Input Area -->
      <div v-if="selectedRemainingTime != 'Chat is expired'">

        <div v-if="replyMessage" class="flex justify-between p-4 ">
          <div>
            <b>Replying to: </b>
            <p v-html="this.getRepliedMessageContent(selectedMessage.message_id)"></p>
          </div>

          <span class="relative bottom-1 text-xl cursor-pointer text-black mr-4"
            @click="replyMessageClose">&times;</span>
        </div>
        <div class="message-input-area">
          <div v-if="templateError" class="mb-2 rounded-md border border-red-400 bg-red-100 px-3 py-2 text-sm text-red-700">
            {{ templateError }}
          </div>
          <input
            ref="messageInput"
            type="text"
            v-model="newMessage"
            @keyup.enter="sendMessage"
            placeholder="Type a message..."
          />
          <label for="file-upload" class="upload-label">
            <i class="bi bi-paperclip"></i>
          </label>

          <button @click.stop="togglePicker" class="emoji-button"><i class="bi bi-emoji-smile"></i></button>

          <!-- Emoji Picker (conditionally rendered) -->
          <div v-if="showPicker" class="custom-picker" ref="picker">
            <EmojiPicker @select="onEmojiSelect" />
          </div>

          <input type="file" id="file-upload" @change="FileUpload" class="file-input" />

          <button 
            id="send-button" 
            class="bg-green-700 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-green-800"
            @click="sendChatMessage()" 
            v-if="!replyMessage"
            :disabled="!newMessage && !draftTemplateMessage"
          >
            {{ draftTemplateMessage ? 'Send Template' : 'Send' }}
          </button>
          <button
            id="send-button"
            class="bg-blue-700 text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:bg-blue-800 ml-2 disabled:cursor-not-allowed disabled:opacity-70"
            @click="generateCRMTemplate()"
            :disabled="templateLoading"
            v-if="!replyMessage"
          >
            <span v-if="!templateLoading">AI Generate</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V2A10 10 0 002 12h2zm2 5.291A7.962 7.962 0 014 12H2a10.003 10.003 0 005.001 8.66l-.001-3.369z"></path>
              </svg>
              Generating...
            </span>
          </button>
          <button id="send-button" @click="sendChatMessageReply()" v-if="replyMessage">Reply</button>


        </div>



      </div>
      <div v-else class="message-input-area flex justify-center text-center">

        <h2>Chats are marked as expired 24 hours after the last received customer message.
          <br>WhatsApp allows only template messages to be sent in such chats.
        </h2>

      </div>
    </div>

    <!-- Contact Information -->
    <div class="contact-info">

      <div class="inner-container bg-white p-4 border-radius-4 h-inherit">
        <h4><i class="bi bi-person-vcard"
            style=" font-size:18px; color: gray; font-weight: 300; margin-right:2px"></i><strong> Contact
            Details</strong> </h4>
        <table class="contact-table">
          <tbody>
            <tr>
              <td style=" color: gray; font-weight: 300;">Name</td>
              <td>{{ contactInfo.name }}</td>
            </tr>
            <tr>
              <td style=" color: gray; font-weight: 300;">Phone</td>
              <td>{{ contactInfo.phone }}</td>
            </tr>
            <tr>
              <td style=" color: gray; font-weight: 300;">Email</td>
              <td>{{ contactInfo.email }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="inner-container bg-white p-4 border-radius-4 h-inherit">
        <h4><i class="bi bi-at" style=" color: gray; font-weight: 300; margin-right:2px"></i><strong>Contact
            Attributes</strong></h4>
        <table class="contact-table">
          <tbody>
            <tr>
              <td style=" color: gray; font-weight: 300;">Created at</td>
              <td>{{ contactInfo.created_at }}</td>
            </tr>
<tr v-for="(tag, index) in contactInfo.tags" :key="index">
  <td style="color: gray; font-weight: 300;">{{ tag.split(':')[0] }}</td>
  <td>{{ tag.split(':')[1] }}</td>
</tr>

          </tbody>
        </table>
      </div>


    </div>
  </div>

</template>

<script>
import EmojiPicker from 'vue3-emoji-picker';
import { toZonedTime } from "date-fns-tz";
export default {
  components: { EmojiPicker },
  name: 'ChatbotView',

  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      
      contextMenuVisible: false,
      contextMenuPosition: { x: 0, y: 0 },
      selectedMessage: null,
      replyMessage: false,
      parsedTemplate: null,
      // Default to first item
      chatStatusFilter: "",
      showPicker: false,
      activeChat: [],
      selectedchat: [],
      selectedChatTime: null,
      selectedRemainingTime: null,
      timer: null,
      ActiveWaid: "",
      ActiveWaidName: "",
      chats: [],
      chatTitle: "",
      chatContent: "",
      contactInfo: {},
      messages: [],
      newMessage: "",
      currentTime: "",
      progressSeconds: 0,
      eventSourceA: null,
      eventSourceB: null,
      templateLoading: false,
      templateError: "",
      generatedTemplatePreview: "",
      draftGeneratedAt: null,
      draftTemplateMessage: "",
    };
  },
  async mounted() {
    // Add click event listener when component is mounted
    document.addEventListener('click', this.handleClickOutside);
    await this.fetchActiveChatlist();
    // Close context menu on click outside
    document.addEventListener("click", () => {
      this.contextMenuVisible = false;
    });

  },

    beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
    // Clean up the EventSource instance
    if (this.eventSourceB) {
      console.log("Closing eventSourceB:", this.eventSourceB);
      this.eventSourceB.close();
      this.eventSourceB = null;
    }
    if (this.eventSourceA) {
      this.eventSourceA.close();
      console.log("SSE connection closed on component unmount.");
    }
  },

  methods: {
    async generateCRMTemplate() {
      if (this.templateLoading) {
        return;
      }

      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.templateError = "You need to log in again before using AI templates.";
          setTimeout(() => this.$router.push('/login'), 1200);
          return;
        }

        this.templateError = "";
        this.templateLoading = true;

        const agentHint = this.deriveAgentGuidance();
        const customerContext = this.buildCustomerContext();
        const dynamicIntent = this.deriveIntent(customerContext, agentHint);

        // Build rich context without generic defaults
        const contextParts = [];
        if (customerContext) {
          contextParts.push(customerContext);
        }
        if (agentHint) {
          contextParts.push(agentHint);
        }
        
        // Only add guidance if we have specific context
        if (contextParts.length === 0) {
          contextParts.push('Create a personalized follow-up message.');
        }

        const payload = {
          customer_name: this.contactInfo?.name || this.ActiveWaidName || 'Customer',
          product_name: this.detectProductMention(),
          intent: dynamicIntent,
          notes: contextParts.join('\n\n')
        };

        const baseUrl = this.apiUrl?.trim();
        const sanitizedBase = baseUrl?.replace(/\/+$/, "") || "";
        const endpoint = sanitizedBase
          ? `${sanitizedBase}/ai/generate-template`
          : "/api/ai/generate-template";

        const resp = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload)
        });
        if (!resp.ok) {
          if (resp.status === 401) {
            this.templateError = "Session expired. Please log in again.";
            setTimeout(() => this.$router.push('/login'), 1200);
            return;
          }

          const text = await resp.text();
          let parsedDetail = text;
          try {
            const json = JSON.parse(text);
            parsedDetail = json?.detail || json?.message || text;
          } catch (_err) {
            parsedDetail = text;
          }
          throw new Error(parsedDetail);
        }
        const contentType = resp.headers.get('content-type') || '';
        const data = contentType.includes('application/json') ? await resp.json() : { template: await resp.text() };

        // The backend returns { template: '<json>' }
        const templateJson = data.template;
        // Wrap following existing rendering convention
        if (!templateJson) {
          throw new Error('The AI service responded without a template.');
        }

        // Store the template for sending, but don't show in input
        const templateMessage = `#template_message# ${templateJson}`;

        
        // Store the template for sending, but don't show in input
        this.templateError = "";
        this.setDraftPreview(templateMessage);
        // Keep input field clean
        this.newMessage = "";
      } catch (e) {
        console.error('AI generation failed', e);
        const rawMessage = e?.message || 'Unknown error while generating template.';
        this.templateError = typeof rawMessage === 'string' ? rawMessage : JSON.stringify(rawMessage);
        this.clearDraftPreview();
      } finally {
        this.templateLoading = false;
      }
    },

    truncateMessage(message) {
      if (message.length > 60) {
        return `${message.slice(0, 60)} <span style="color: gray; cursor: pointer;">...read more</span>`;
      }
      return message;
    },

    processMessageContent(content) {
      if (content === null || content === undefined) {
        return "";
      }

      const stringContent = typeof content === "string" ? content : JSON.stringify(content);
      const normalized = stringContent.trimStart();
      const templatePrefix = "#template_message#";
      let templatePayload = normalized;

      if (normalized.startsWith(templatePrefix)) {
        templatePayload = normalized.slice(templatePrefix.length).trimStart();
      }

      if (templatePayload.startsWith("{") || templatePayload.startsWith("[")) {
        try {
          const parsedTemplate = JSON.parse(templatePayload);
          const components = this.normalizeTemplateComponents(
            Array.isArray(parsedTemplate?.components)
              ? parsedTemplate.components
              : []
          );

          if (!components.length) {
            return `<div class="template-body mb-2">${this.escapeHtml(stringContent)}</div>`;
          }

          return components
            .map((component) => {
              if (component.type === "HEADER") {
                if (component.format === "TEXT" && component.text) {
                  return `<strong>${this.escapeHtml(component.text)}</strong>`;
                }
                if (
                  component.format === "IMAGE" &&
                  component.example?.header_handle?.[0]
                ) {
                  const imageUrl = this.escapeAttribute(component.example.header_handle[0]);
                  return `
                    <div style="width: auto; height: 200px; overflow: hidden; position: relative; border-radius: 5px">
                      <img src="${imageUrl}" alt="Template image" 
                        style="width: 100%; height: 100%; object-fit: cover; object-position: center; display: block; border-radius: 4px">
                    </div>`;
                }
              }

              if (component.type === "BODY" && component.text) {
                return `<div class="template-body mb-2">${this.escapeHtml(component.text).replace(/\n/g, "<br>")}</div>`;
              }

              if (component.type === "FOOTER" && component.text) {
                return `<div class="template-footer text-sm text-gray-500">${this.escapeHtml(component.text)}</div>`;
              }

              if (component.type === "BUTTONS" && Array.isArray(component.buttons)) {
                return component.buttons
                  .map((button) => {
                    if (button.type === "URL" && button.url) {
                      const safeUrl = this.escapeAttribute(button.url);
                      return `
                        <div style="text-align: left; font-size: 16px;">
                          <a href="${safeUrl}" target="_blank"
                            style="display: inline-flex; align-items: center; text-decoration: none; font-weight: 600; color: #007bff; border-top: 1px solid #ddd; padding-top: 6px;">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="#007bff" width="18" height="18" viewBox="0 0 24 24" style="margin-right: 6px;">
                              <path d="M14 3v2h3.586l-8.293 8.293 1.414 1.414 8.293-8.293v3.586h2v-7h-7z"/>
                              <path d="M5 5h6v-2h-6c-1.103 0-2 .897-2 2v14c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-6h-2v6h-14v-14z"/>
                            </svg>
                            <span>${this.escapeHtml(button.text || "Open link")}</span>
                          </a>
                        </div>`;
                    }

                    if (button.type === "REPLY") {
                      return `
                        <div style="text-align: left;">
                          <button style="display: inline-block; margin: 5px 0; padding: 10px 16px; background-color: #007bff; color: white; border: none; border-radius: 9999px; cursor: pointer; font-weight: 600;">
                            ${this.escapeHtml(button.text || "Reply")}
                          </button>
                        </div>`;
                    }

                    return "";
                  })
                  .join("");
              }

              return "";
            })
            .filter(Boolean)
            .join("");
        } catch (error) {
          console.error("Failed to parse template message:", error, templatePayload);
          return `<div class="template-error">${this.escapeHtml(stringContent)}</div>`;
        }
      }

      return `<p>${this.escapeHtml(stringContent).replace(/\n/g, "<br>")}</p>`;
    },

    escapeHtml(value) {
      return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    },

    escapeAttribute(value) {
      return this.escapeHtml(value).replace(/"/g, "&quot;");
    },

    normalizeTemplateComponents(rawComponents) {
      return rawComponents
        .map((component) => {
          if (!component || typeof component !== "object") {
            return null;
          }

          const rawType = (component.type || component.format || "").toString().trim();
          const upperType = rawType.toUpperCase();

          // If component already matches expected schema, return as-is
          if (
            ["HEADER", "BODY", "FOOTER"].includes(upperType) &&
            (component.text || component.example || component.buttons)
          ) {
            return {
              ...component,
              type: upperType,
            };
          }

          if (upperType === "HEADER") {
            const text = this.extractTextFromParameters(component.parameters) || component.text;
            if (!text) return null;
            return {
              type: "HEADER",
              format: "TEXT",
              text,
            };
          }

          if (upperType === "BODY") {
            const text = this.extractTextFromParameters(component.parameters) || component.text;
            if (!text) return null;
            return {
              type: "BODY",
              text,
            };
          }

          if (upperType === "FOOTER") {
            const text = this.extractTextFromParameters(component.parameters) || component.text;
            if (!text) return null;
            return {
              type: "FOOTER",
              text,
            };
          }

          if (upperType === "BUTTON" || upperType === "BUTTONS") {
            if (Array.isArray(component.buttons) && component.buttons.length) {
              return {
                type: "BUTTONS",
                buttons: component.buttons,
              };
            }

            if (Array.isArray(component.parameters) && component.parameters.length) {
              const buttons = component.parameters
                .map((param) => {
                  if (!param || typeof param !== "object") return null;
                  const paramType = (param.type || "").toString().trim().toUpperCase();
                  const text = param.text || param.payload || "";
                  if (!text) return null;
                  if (paramType === "QUICK_REPLY") {
                    return { type: "REPLY", text };
                  }
                  if (paramType === "URL") {
                    return { type: "URL", text, url: param.url || text };
                  }
                  return { type: paramType || "REPLY", text };
                })
                .filter(Boolean);

              if (buttons.length) {
                return {
                  type: "BUTTONS",
                  buttons,
                };
              }
            }
          }

          return null;
        })
        .filter(Boolean);
    },

    extractTextFromParameters(parameters) {
      if (!Array.isArray(parameters)) {
        return null;
      }

      for (const param of parameters) {
        if (!param || typeof param !== "object") {
          continue;
        }

        if (typeof param.text === "string" && param.text.trim()) {
          return param.text;
        }

        if (typeof param.payload === "string" && param.payload.trim()) {
          return param.payload;
        }
      }

      return null;
    },

    setDraftPreview(templateString) {
      this.generatedTemplatePreview = this.processMessageContent(templateString);
      this.draftTemplateMessage = templateString;
      this.draftGeneratedAt = new Date().toISOString();
      this.$nextTick(() => {
        this.$refs.messageInput?.focus();
        this.scrollToBottom();
      });
    },

    clearDraftPreview() {
      this.generatedTemplatePreview = "";
      this.draftGeneratedAt = null;
      this.draftTemplateMessage = "";
    },

    formatTime(isoString) {
      if (!isoString) {
        return "";
      }

      try {
        const date = new Date(isoString);
        if (Number.isNaN(date.getTime())) {
          return "";
        }
        return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      } catch (_err) {
        return "";
      }
    },

    deriveAgentGuidance() {
      const draft = (this.newMessage || "").trim();
      if (!draft || draft.startsWith("#template_message#")) {
        return "";
      }
      return `Agent guidance: ${draft}`;
    },

    deriveIntent(customerContext, agentHint) {
      // Analyze context to determine appropriate intent
      const contextLower = (customerContext + " " + agentHint).toLowerCase();
      
      if (contextLower.includes('order') || contextLower.includes('purchase') || contextLower.includes('buy')) {
        return 'order_support';
      }
      if (contextLower.includes('payment') || contextLower.includes('invoice') || contextLower.includes('bill')) {
        return 'payment_reminder';
      }
      if (contextLower.includes('problem') || contextLower.includes('issue') || contextLower.includes('help')) {
        return 'support_follow_up';
      }
      if (contextLower.includes('welcome') || contextLower.includes('new') || contextLower.includes('first')) {
        return 'welcome';
      }
      if (contextLower.includes('upsell') || contextLower.includes('upgrade') || contextLower.includes('offer')) {
        return 'upsell_opportunity';
      }
      
      return 'personalized_follow_up';
    },

    detectProductMention() {
      const recentMessages = this.selectedchat?.slice(-5) || [];
      const allText = recentMessages
        .map(msg => this.extractPlainTextFromMessage(msg.message_content))
        .join(' ')
        .toLowerCase();
      
      // Look for common product/service keywords
      if (allText.includes('pro') || allText.includes('premium')) return 'Pro Plan';
      if (allText.includes('basic') || allText.includes('starter')) return 'Basic Plan';
      if (allText.includes('subscription') || allText.includes('plan')) return 'Subscription';
      if (allText.includes('service') || allText.includes('support')) return 'Support Services';
      
      return '';
    },

    buildCustomerContext() {
      if (!Array.isArray(this.selectedchat) || !this.selectedchat.length) {
        return "Customer has not sent any messages yet. This is likely a new conversation.";
      }

      const recentCustomerMessages = this.selectedchat
        .filter((message) => (message.direction || "").toLowerCase() !== "sent")
        .slice(-3);

      if (!recentCustomerMessages.length) {
        return "This is an ongoing conversation. Customer has previously engaged but no recent messages to show.";
      }

      const formatted = recentCustomerMessages
        .map((message) => {
          const when = this.formatTimestampForPrompt(message.timestamp);
          const body = this.extractPlainTextFromMessage(message.message_content);
          const snippet = this.truncateForPrompt(body, 220);
          const speaker = message.sender_name || this.ActiveWaidName || "Customer";
          return `- ${speaker}${when ? ` (${when})` : ""}: "${snippet}"`;
        })
        .join("\n");

      return `Recent customer messages:\n${formatted}\n\nBased on this conversation, create a relevant and personalized response.`;
    },

    formatTimestampForPrompt(timestamp) {
      if (!timestamp) {
        return "";
      }

      try {
        const date = new Date(timestamp);
        if (Number.isNaN(date.getTime())) {
          return "";
        }
        return date.toLocaleString([], { hour: "2-digit", minute: "2-digit", month: "short", day: "numeric" });
      } catch (_err) {
        return "";
      }
    },

    truncateForPrompt(text, limit = 240) {
      if (!text) {
        return "";
      }
      if (text.length <= limit) {
        return text;
      }
      return `${text.slice(0, limit - 1).trim()}…`;
    },

    extractPlainTextFromMessage(rawContent) {
      if (rawContent === null || rawContent === undefined) {
        return "";
      }

      const asString = typeof rawContent === "string" ? rawContent : JSON.stringify(rawContent);
      const trimmed = asString.trim();
      const templatePrefix = "#template_message#";
      let payload = trimmed;

      if (trimmed.startsWith(templatePrefix)) {
        payload = trimmed.slice(templatePrefix.length).trimStart();
      }

      if (payload.startsWith("{") || payload.startsWith("[")) {
        try {
          const parsed = JSON.parse(payload);
          const normalized = this.normalizeTemplateComponents(
            Array.isArray(parsed?.components) ? parsed.components : []
          );
          if (!normalized.length) {
            return this.cleanWhitespace(payload);
          }

          const parts = normalized
            .map((component) => {
              if (["HEADER", "BODY", "FOOTER"].includes(component.type) && component.text) {
                return component.text;
              }

              if (component.type === "BUTTONS" && Array.isArray(component.buttons)) {
                return component.buttons
                  .map((button) => button.text || button.url)
                  .filter(Boolean)
                  .join(" / ");
              }

              return "";
            })
            .filter(Boolean)
            .join("\n");

          return this.cleanWhitespace(parts);
        } catch (_err) {
          return this.cleanWhitespace(payload);
        }
      }

      return this.cleanWhitespace(asString);
    },

    cleanWhitespace(value) {
      if (!value) {
        return "";
      }

      return value
        .replace(/\r\n/g, "\n")
        .split("\n")
        .map((line) => line.trim())
        .filter(Boolean)
        .join("\n");
    },

    replyMessageClose() {
      this.replyMessage = false;
      this, this.selectedMessage = '';
    },

    showContextMenu(event, message) {
      this.contextMenuVisible = true;
      this.contextMenuPosition = { x: event.clientX, y: event.clientY };
      this.selectedMessage = message;
    },
    replyToMessage() {
      if (this.selectedMessage) {

        this.replyMessage = true;

        // Add your reply logic here
        console.log("Replying to:", this.getRepliedMessageContent(this.selectedMessage.message_id));
      }
      this.contextMenuVisible = false;
    },


    getRepliedMessageContent(replyToId) {
      if (!Array.isArray(this.selectedchat)) {
        console.error("selectedchat is not defined or is not an array");
        return '';
      }

      const repliedMessage = this.selectedchat.find(message => message.message_id === replyToId);

      if (!repliedMessage) {
        console.warn(`Message with ID ${replyToId} not found in selectedchat`);
        return '';
      }

      return this.processMessageContent(repliedMessage.message_content);
    },

    shouldShowDate(index) {
      if (index === 0) return true; // Always show the date for the first message
      const currentDate = this.selectedchat[index].timestamp.split('T')[0];
      const previousDate = this.selectedchat[index - 1].timestamp.split('T')[0];
      return currentDate !== previousDate; // Show date separator if the date changes
    },
    formatDate(date) {
      // Format date to a more readable format if needed
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },

    FileUpload(event) {
      const file = event.target.files[0];
      console.log('File uploaded:', file);
    },

    togglePicker() {
      this.showPicker = !this.showPicker;
    },
    handleClickOutside(event) {
      if (this.showPicker && !this.$refs.picker.contains(event.target)) {
        this.showPicker = false; // Hide the picker
      }
    },

    onEmojiSelect(emoji) {
      if (emoji && emoji.i) {
        this.newMessage += emoji.i; // Append the emoji from the 'i' property
      } else {
        console.error("Invalid emoji object:", emoji);
      }
    },

    SetChatTime(chatTime) {

      console.log(chatTime);
      this.selectedChatTime = chatTime;

      // Convert the chatTime string to a Date object
      const chatDate = new Date(chatTime);



      const TimeZoneChatTime = chatDate;


      // Add 24 hours to chatDate
      const EndDate = new Date(TimeZoneChatTime.setHours(TimeZoneChatTime.getHours() + 24));


      // Clear any existing timer to avoid multiple intervals
      if (this.timer) {
        clearInterval(this.timer);
      }

      // Function to update the remaining time
      const updateRemainingTime = () => {


        const currentDate = new Date();
        const utcDate = toZonedTime(currentDate, "UTC");// Local timezone

        // console.log(utcDate);
        // console.log(EndDate);
        // Get the current date and time
        const timeDifference = EndDate - utcDate; // Calculate the difference

        if (timeDifference <= 0) {
          // If time has expired, stop the timer and show "Chat is expired"
          clearInterval(this.timer);
          this.selectedRemainingTime = 'Chat is expired';

          return;
        }

        // Calculate remaining days, hours, minutes, seconds

        const minutes = Math.floor((timeDifference / 1000 / 60) % 60);
        const hours = Math.floor((timeDifference / 1000 / 60 / 60) % 24);
        const days = Math.floor(timeDifference / 1000 / 60 / 60 / 24);

        // Construct remaining time string
        let remainingTime = '';
        if (days > 0) remainingTime += `${days} : `;
        remainingTime += `${String(hours).padStart(2, '0')} : `; // Format hours
        remainingTime += `${String(minutes).padStart(2, '0')}  `; // Format minutes
        this.selectedRemainingTime = remainingTime.trim();
      };

      // Call the update function immediately to show the initial remaining time
      updateRemainingTime();

      // Set up the interval to update the remaining time every second
      this.timer = setInterval(updateRemainingTime, 1000);
    },

    beforeDestroy() {
      // Clear the timer when the component is destroyed to avoid memory leaks
      if (this.timer) {
        clearInterval(this.timer);
      }
    },

    async fetchActiveChatlist(chatStatusFilter = null) {
      try {

        if (this.eventSourceB) {
          // Close the previous EventSource connection
          this.eventSourceB.close();
          console.log("Previous SSE connection closed.");
        }

        const token = localStorage.getItem('token');

        // Create a new EventSource for receiving SSE
        this.eventSourceB = new EventSource(`${this.apiUrl}/active-conversations?token=${token}`, {

        });

        // Listen for events
        this.eventSourceB.onmessage = (event) => {
          const activeChats = JSON.parse(event.data);

          // Map the received active chat data
          this.activeChat = activeChats.map((activechat) => ({
            message_content: activechat.message_content,
            sender_name: activechat.sender_name,
            business_account_id: activechat.business_account_id,
            active: activechat.active,
            message_id: activechat.message_id,
            id: activechat.id,
            sender_wa_id: activechat.sender_wa_id,
            last_chat_time: activechat.last_chat_time
          })).filter(activechat => {
  if (chatStatusFilter === null || chatStatusFilter === '') {
    // No filter applied, return all items
    return true;
  }
  // Apply the filter based on the value of chatStatusFilter
  return activechat.active == (chatStatusFilter === 'true');
});

        };



        // Handle connection errors
        this.eventSourceB.onerror = (error) => {
          console.error("Unable to fetch active conversations", error);
          this.eventSourceB.close(); // Close the connection on error
        };

      } catch (error) {
        console.error("Unable to fetch active conversations");
      }
    },

    filterChatsByStatus(event) {
      const status = event.target.value;
      this.fetchActiveChatlist(status);
    },

    async ConversationSSE(wa_id) {

      this.selectedRemainingTime = null;
      // Check if there's an existing EventSource instance
      if (this.eventSourceA) {
        // Close the previous EventSource connection
        this.eventSourceA.close();
        console.log("Previous SSE connection closed.");
      }

      // Fetch the token
      const token = localStorage.getItem('token');

      // Create a new EventSource instance with the new wa_id
      this.eventSourceA = new EventSource(`${this.apiUrl}/sse/conversations/${wa_id}?token=${token}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      await this.ActiveContactDetails(wa_id);
      this.contactInfo.name=this.contactInfo.name?this.contactInfo.name:this.ActiveWaidName
      this.contactInfo.phone=this.contactInfo.phone?this.contactInfo.phone:this.ActiveWaid
      
      // Handle incoming messages
      this.eventSourceA.onmessage = (event) => {
        try {
          // Parse the new conversations data
          const newConversations = JSON.parse(event.data);

          // Determine if the user is already scrolled to the bottom
          const chatContent = this.$refs.chatContent;
          const isAtBottom = chatContent.scrollHeight - chatContent.scrollTop <= chatContent.clientHeight + 10;

          this.selectedchat = newConversations;  // Update the UI with the new data

          // Get the last chat timestamp and call SetChatTime
          if (newConversations.length > 0) {
            // Filter messages to only include those with direction "received"
            const receivedMessages = newConversations.filter(
              (message) => message.direction === "Receive"
            );

            if (receivedMessages.length > 0) {
              // Get the last "received" message
              const lastReceivedMessage =
                receivedMessages[receivedMessages.length - 1];

              // Pass its timestamp to SetChatTime
              this.SetChatTime(lastReceivedMessage.timestamp);
            }
          }



          // Only scroll to the bottom if the user is already at (or near) the bottom
          if (isAtBottom) {
            this.scrollToBottom();
          }
        } catch (error) {
          console.error("Error parsing SSE data", error);
        }
      };

      // Handle errors
      this.eventSourceA.onerror = (error) => {
        console.error("SSE connection error:", error);
        // You can handle reconnections or notify the user here if needed
      };

      console.log("New SSE connection established.");
    },

    // Scroll logic to be called after new data is loaded
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContent = this.$refs.chatContent;
        if (chatContent) {
          chatContent.scrollTop = chatContent.scrollHeight;
        }
      });
    },

    async ActiveContactDetails(wa_id) {
      this.contactInfo= {};
      const token = localStorage.getItem('token');

      try {

        const response = await fetch(`${this.apiUrl}/contacts/${wa_id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }


        const contact = await response.json()

        this.contactInfo = contact;

      } catch (error) {

        console.error("Error fetching contact details:", error);

      }
    },


    async sendChatMessage() {
      // Use draft template if available, otherwise use typed message
      const message = this.draftTemplateMessage || this.newMessage;
      const reciever = this.ActiveWaid
      try {
        const token = localStorage.getItem("token");

        const requestBody = {
          wa_id: reciever,
          body: message
        }

        const response = await fetch(`${this.apiUrl}/send-text-message/`, {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody)

        })
        if (!response.ok) {
          throw new Error("Network response not okay");
        }
        else {
          this.newMessage = "";
          this.clearDraftPreview();
        }

      } catch (error) {
        console.error("Error sending message")
      }
    },

    async sendChatMessageReply() {
      const message = this.newMessage
      const reciever = this.ActiveWaid
      try {
        const token = localStorage.getItem("token");

        const requestBody = {
          wa_id: reciever,
          body: message,
          context_message_id: this.selectedMessage.message_id

        }

        const response = await fetch(`${this.apiUrl}/send-text-message-reply/`, {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody)

        })
        if (!response.ok) {
          throw new Error("Network response not okay");
        }
        else {
          this.newMessage = "";
          this.selectedMessage = '';
          this.replyMessage = false;
          this.clearDraftPreview();
        }

      } catch (error) {
        console.error("Error sending message")
      }
    }

  },







};
</script>





<style scoped>
/* Main container layout */
.custom-context-menu {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  list-style: none;
  padding: 5px 0;
  margin: 0;
  width: 150px;
}



.custom-context-menu ul {
  margin: 0;
  padding: 0;
}

.custom-context-menu li {
  padding: 10px;
  cursor: pointer;
}

.custom-context-menu li:hover {
  background-color: #f5f5f5;
}

.draft-message {
  background-color: rgba(8, 150, 120, 0.08);
  border: 1px solid rgba(8, 150, 120, 0.25);
}

.draft-message-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 300px;
}

.draft-message-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.draft-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #056952;
  background-color: rgba(5, 105, 82, 0.12);
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
}

.draft-actions {
  display: flex;
  gap: 0.5rem;
}

.draft-send {
  background: #16a34a;
  border: none;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.draft-send:hover {
  background: #15803d;
}

.draft-clear {
  background: transparent;
  border: none;
  color: #1d4ed8;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

.draft-clear:hover {
  text-decoration: underline;
}

.draft-message-body {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  font-size: 0.95rem;
  line-height: 1.5rem;
}


.main-container {
  display: flex;
  height: 92.2vh;
  width: 100%;
  background-color: #f4f4f4;
  font-family: Arial, sans-serif;
}

/* Sidebar styling */
.sidebar {
  width: 20%;
  padding: 15px;
  background-color: #ffffff;
  color: #ffffff;
  overflow-y: auto;
}

.sidebar h1 {
  color: #000;
  margin-bottom: 10px;
}

.chatType {
  display: flex;
  border-bottom: 1px solid #ccc;
  margin-bottom: 20px;
}

.chat-list {
  list-style: none;
  padding: 0;
}

.chat-list li {
  margin-bottom: 15px;
}

.chat-list a {
  display: block;
  padding: 10px;
  color: #ffffff;
  background-color: #128C7E;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.chat-list a:hover {
  background-color: #25D366;
}

/* Chat area styling */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f5f6fa;
  border-left: 1px solid #ddd;
}

.chat-header {
  display: flex;
  align-items: center;
  height: 65px;
  padding: 10px 30px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ccc;
  color: #000;
  font-size: 1rem;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

.chat-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-image: url("@/assets/chat-bg.jpg");
  background-size: contain;
  /* Scales the image to fit within the container */
  background-repeat: repeat;
  /* Prevents the image from repeating */
  background-position: center;
  height: calc(100vh - 200px);
}

.chat-content::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 1);
  /* Set the opacity here */
  z-index: -1;
  /* Keeps the overlay behind the content */
}

/* Message styling */
.message {
  display: flex;
  justify-content: space-between;
  background-color: white;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  max-width: 60%;
  min-width: 80px;
  width: fit-content;
}

.sent-message {
  align-self: flex-end;
  margin-left: auto;
  background-color: #dcf8c6;
}

.messageTime {
  display: flex;
  margin-left: 5px;
  font-size: 12px;
  color: #666;
  align-items: flex-end;
}

/* Message input area */
.message-input-area {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f1f1f1;
}

.message-input-area input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}



#send-button {
  padding: 10px 15px;
  margin-left: 10px;
  
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}


/* Upload button */
.upload-label {
  cursor: pointer;
  margin-left: 10px;
}

.upload-label i {
  font-size: 18px;
  color: #666;
}

.upload-label:hover i {
  color: #25d366;
}

.file-input {

  display: none;

}

/* Contact information styling */
.contact-info {
  width: 30%;
  padding: 10px;
  padding-top: 13px;
  background-color: #f0f0f0;
  border-left: 1px solid #ddd;
}

.contact-info h3 {
  margin-top: 0;
}

.tags {
  margin-top: 20px;
}

.tags h4 {
  margin-bottom: 10px;
}

.tags ul {
  list-style: none;
  padding: 0;
}

.tags ul li {
  display: inline-block;
  margin-bottom: 5px;
  background-color: #128C7E;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.tags ul li button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 10px;
}

.tags input {
  padding: 5px;
  margin-top: 10px;
  width: 80%;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.tags button {
  padding: 5px 10px;
  background-color: #128C7E;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.tags button:hover {
  background-color: #25D366;
}

/* Timer styling */
.timer {
  display: flex;
  align-items: center;
  padding: 19px 0 15px 0;
  width: inherit;
  margin-right: 10px;
}



.progress-circle {
  fill: none;
  stroke: #4caf50;
  stroke-width: 5;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

/* Contact table styling */
.contact-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.contact-table th,
.contact-table td {

  padding: 8px;
  text-align: left;
}

.contact-table th {
  background-color: #f2f2f2;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
  }

  .chat-area,
  .contact-info {
    width: 100%;
    margin-top: 10px;
  }

  .chat-area {
    order: 2;
  }

  .contact-info {
    order: 1;

  }

  .main-container {
    flex-direction: column;
  }
}
</style>