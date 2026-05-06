<template>
  <main class="page-section">
    <div class="container">
      <div class="browse-header mb-4">
        <div>
          <p class="dashboard-kicker text-primary">Connections</p>
          <h1>Your Matches</h1>
          <p>
            These are users who liked you back. You can start a conversation with any mutual match.
          </p>
        </div>

        <RouterLink class="btn btn-outline-primary" to="/browse">
          Browse More
        </RouterLink>
      </div>

      <AlertMessage :message="errorMessage" type="error" />

      <LoadingSpinner
        v-if="isLoading"
        message="Loading your matches..."
      />

      <section v-else>
        <div v-if="matches.length" class="row g-4">
          <div
            v-for="profile in matches"
            :key="profile.id"
            class="col-lg-6"
          >
            <ProfileCard
              :profile="profile"
              :show-message-button="true"
            />
          </div>
        </div>

        <div v-else class="page-card text-center">
          <h2>No matches yet</h2>
          <p>
            You do not have any mutual matches yet. Browse profiles and like users you are interested in.
          </p>

          <RouterLink class="btn btn-primary" to="/browse">
            Browse Matches
          </RouterLink>
        </div>
      </section>
    </div>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router';
import { getMatches } from '../api/client';
import AlertMessage from '../components/AlertMessage.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import ProfileCard from '../components/ProfileCard.vue';

export default {
  name: 'MatchesView',

  components: {
    RouterLink,
    AlertMessage,
    LoadingSpinner,
    ProfileCard
  },

  data() {
    return {
      // Stores mutual matches returned from the Flask backend.
      matches: [],

      // Controls loading and error feedback.
      isLoading: false,
      errorMessage: ''
    };
  },

  async mounted() {
    await this.loadMatches();
  },

  methods: {
    /*
      Gets users where both sides have liked each other.
      These are the only users who should be available for messaging.
    */
    
    async loadMatches() {
      this.errorMessage = '';

      try {
        this.isLoading = true;
        this.matches = await getMatches();
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>
