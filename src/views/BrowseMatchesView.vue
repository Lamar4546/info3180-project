<template>
  <main class="page-section">
    <div class="container">
      <div class="browse-header mb-4">
        <div>
          <p class="dashboard-kicker text-primary">Discover</p>
          <h1>Browse Matches</h1>
          <p>
            Search for compatible users, review their profiles, and choose whether to like or pass.
          </p>
        </div>
      </div>

      <!-- Filters are kept in a separate reusable component. -->
      <MatchFilters
        class="mb-4"
        @filter="handleFilter"
        @clear="handleClearFilters"
      />

      <AlertMessage :message="errorMessage" type="error" />
      <AlertMessage :message="successMessage" type="success" />

      <LoadingSpinner
        v-if="isLoading"
        message="Loading potential matches..."
      />

      <section v-else>
        <div v-if="profiles.length" class="row g-4">
          <div
            v-for="profile in profiles"
            :key="profile.id"
            class="col-lg-6"
          >
            <ProfileCard
              :profile="profile"
              :show-actions="true"
              @like="handleLike"
              @pass="handlePass"
            />
          </div>
        </div>

        <div v-else class="page-card text-center">
          <h2>No profiles found</h2>
          <p class="mb-0">
            Try changing your filters or check again later for new users.
          </p>
        </div>
      </section>
    </div>
  </main>
</template>

<script>
import { browseMatches, sendMatchAction } from '../api/client';
import AlertMessage from '../components/AlertMessage.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import MatchFilters from '../components/MatchFilters.vue';
import ProfileCard from '../components/ProfileCard.vue';

export default {
  name: 'BrowseMatchesView',

  components: {
    AlertMessage,
    LoadingSpinner,
    MatchFilters,
    ProfileCard
  },

  data() {
    return {
      // Stores the profiles returned from the Flask browse endpoint.
      profiles: [],

      // Stores the active filters selected by the user.
      activeFilters: {},

      // Controls loading and feedback messages.
      isLoading: false,
      errorMessage: '',
      successMessage: ''
    };
  },

  async mounted() {
    await this.loadProfiles();
  },

  methods: {
    /*
      Gets potential matches from the backend.
      If filters are active, they are sent as query parameters.
    */
    
    async loadProfiles() {
      this.errorMessage = '';
      this.successMessage = '';

      try {
        this.isLoading = true;

        this.profiles = await browseMatches(this.activeFilters);
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
      }
    },

    /*
      Receives filter values from MatchFilters.vue, stores them,
      and reloads the browse results.
    */
    
    async handleFilter(filters) {
      this.activeFilters = filters;
      await this.loadProfiles();
    },

    /*
      Clears all active filters and reloads the default browse list.
    */
    
    async handleClearFilters() {
      this.activeFilters = {};
      await this.loadProfiles();
    },

    /*
      Sends a like action for the selected profile.
      The profile is removed from the browse list after the action.
    */
    
    async handleLike(profileId) {
      await this.handleMatchAction(profileId, 'like');
    },

    /*
      Sends a pass action for the selected profile.
      The profile is removed from the browse list after the action.
    */
    
    async handlePass(profileId) {
      await this.handleMatchAction(profileId, 'pass');
    },

    /*
      Sends either "like" or "pass" to Flask.
      If the backend reports a mutual match, a special message is shown.
    */
    
    async handleMatchAction(profileId, action) {
      this.errorMessage = '';
      this.successMessage = '';

      try {
        const result = await sendMatchAction(profileId, action);

        this.profiles = this.profiles.filter((profile) => profile.id !== profileId);

        if (result.is_match) {
          this.successMessage = 'It’s a match! You can now message this user.';
        } else if (action === 'like') {
          this.successMessage = 'Profile liked.';
        } else {
          this.successMessage = 'Profile passed.';
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    }
  }
};
</script>
