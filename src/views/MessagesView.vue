<template>
  <main class="page-section">
    <div class="container">
      <div class="browse-header mb-4">
        <div>
          <p class="dashboard-kicker text-primary">Inbox</p>
          <h1>Messages</h1>
          <p>
            View your conversations with users you have matched with.
          </p>
        </div>
      </div>

      <AlertMessage :message="errorMessage" type="error" />

      <LoadingSpinner
        v-if="isLoading"
        message="Loading your conversations..."
      />

      <section v-else>
        <div v-if="conversations.length" class="conversation-list">
          <RouterLink
            v-for="conversation in conversations"
            :key="conversation.partner.id"
            class="conversation-card"
            :to="`/messages/${conversation.partner.id}`"
          >
            <div class="conversation-avatar">
              <img
                v-if="conversation.partner.profile && conversation.partner.profile.photo"
                :src="getProfilePhoto(conversation.partner.profile.photo)"
                alt="Profile photo"
              />
              <span v-else>👤</span>
            </div>

            <div class="conversation-details">
              <h2>
                {{ getPartnerName(conversation.partner) }}
              </h2>

              <p v-if="conversation.last_message">
                {{ conversation.last_message.body }}
              </p>

              <p v-else>
                No messages yet.
              </p>
            </div>

            <span
              v-if="conversation.last_message"
              class="conversation-time"
            >
              {{ formatDate(conversation.last_message.created_at) }}
            </span>
          </RouterLink>
        </div>

        <div v-else class="page-card text-center">
          <h2>No conversations yet</h2>
          <p>
            Once you match with someone and start messaging, your conversations will appear here.
          </p>

          <RouterLink class="btn btn-primary" to="/matches">
            View Matches
          </RouterLink>
        </div>
      </section>
    </div>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router';
import { getConversations, getPhotoUrl } from '../api/client';
import AlertMessage from '../components/AlertMessage.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
  name: 'MessagesView',

  components: {
    RouterLink,
    AlertMessage,
    LoadingSpinner
  },

  data() {
    return {
      // Stores conversations returned from the Flask backend.
      conversations: [],

      // Controls loading and error feedback.
      isLoading: false,
      errorMessage: ''
    };
  },

  async mounted() {
    await this.loadConversations();
  },

  methods: {
    /*
      Gets all message conversations for the logged-in user.
      Each conversation includes the partner and the latest message.
    */
    
    async loadConversations() {
      this.errorMessage = '';

      try {
        this.isLoading = true;
        this.conversations = await getConversations();
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
      }
    },

    /*
      Safely builds the display name for a conversation partner.
      Falls back to username if profile details are missing.
    */
    
    getPartnerName(partner) {
      if (partner.profile) {
        return `${partner.profile.first_name} ${partner.profile.last_name}`;
      }

      return partner.username || 'Unknown User';
    },

    /*
      Converts a saved profile photo filename into the full backend image URL.
    */
    
    getProfilePhoto(filename) {
      return getPhotoUrl(filename);
    },

    /*
      Converts the backend timestamp into a friendlier date/time.
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
