<template>
  <main class="page-section">
    <div class="container">
      <div class="conversation-layout">
        <div class="conversation-header">
          <div>
            <p class="dashboard-kicker text-primary">Conversation</p>
            <h1>Message History</h1>
            <p>
              Send and view messages with this matched user.
            </p>
          </div>

          <RouterLink class="btn btn-outline-primary" to="/messages">
            Back to Messages
          </RouterLink>
        </div>

        <AlertMessage :message="errorMessage" type="error" />
        <AlertMessage :message="successMessage" type="success" />

        <LoadingSpinner
          v-if="isLoading"
          message="Loading conversation..."
        />

        <section v-else class="message-panel">
          <div v-if="messages.length" class="message-list">
            <div
              v-for="message in messages"
              :key="message.id"
              class="message-row"
              :class="{ 'message-row-own': message.sender_id === currentUserId }"
            >
              <div class="message-bubble">
                <p>{{ message.body }}</p>
                <small>{{ formatDate(message.created_at) }}</small>
              </div>
            </div>
          </div>

          <div v-else class="empty-message-state">
            <h2>No messages yet</h2>
            <p>Start the conversation by sending the first message.</p>
          </div>

          <form class="message-form" @submit.prevent="handleSendMessage">
            <input
              v-model.trim="newMessage"
              type="text"
              class="form-control"
              placeholder="Type a message..."
              :disabled="isSending"
            />

            <button
              type="submit"
              class="btn btn-primary"
              :disabled="isSending || !newMessage"
            >
              {{ isSending ? 'Sending...' : 'Send' }}
            </button>
          </form>
        </section>
      </div>
    </div>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router';
import {
  getCurrentUser,
  getMessageHistory,
  sendMessage
} from '../api/client';
import AlertMessage from '../components/AlertMessage.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
  name: 'ConversationView',

  components: {
    RouterLink,
    AlertMessage,
    LoadingSpinner
  },

  props: {
    partnerId: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      // The logged-in user's ID is used to align their own messages to the right.
      currentUserId: null,

      // Stores messages between the logged-in user and the selected partner.
      messages: [],

      // Stores the text being typed before sending.
      newMessage: '',

      // Loading and feedback states.
      isLoading: false,
      isSending: false,
      errorMessage: '',
      successMessage: ''
    };
  },

  async mounted() {
    await this.loadConversation();
  },

  methods: {
    /*
      Gets the logged-in user and message history for the selected partner.
      The partnerId comes from the route: /messages/:partnerId
    */
    async loadConversation() {
      this.errorMessage = '';
      this.successMessage = '';

      try {
        this.isLoading = true;

        const user = await getCurrentUser();
        this.currentUserId = user.id;

        this.messages = await getMessageHistory(this.partnerId);
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
      }
    },

    /*
      Sends a new message to the matched user.
      If successful, the message is added to the message list immediately.
    */
    
    async handleSendMessage() {
      this.errorMessage = '';
      this.successMessage = '';

      if (!this.newMessage) {
        return;
      }

      try {
        this.isSending = true;

        const sentMessage = await sendMessage(this.partnerId, this.newMessage);

        this.messages.push(sentMessage);
        this.newMessage = '';
        this.successMessage = 'Message sent.';
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isSending = false;
      }
    },

    /*
      Displays backend timestamps in a readable format.
    */
    
    formatDate(dateString) {
      if (!dateString) {
        return '';
      }

      return new Date(dateString).toLocaleString([], {
        dateStyle: 'short',
        timeStyle: 'short'
      });
    }
  }
};
</script>
