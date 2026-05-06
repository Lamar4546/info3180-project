<template>
  <article class="profile-card">
    <div class="profile-card-photo">
      <img
        v-if="profile.photo"
        :src="photoUrl"
        :alt="`${profile.first_name}'s profile photo`"
      />
      <span v-else>👤</span>
    </div>

    <div class="profile-card-body">
      <div class="profile-card-header">
        <div>
          <h2>{{ profile.first_name }} {{ profile.last_name }}</h2>
          <p class="profile-meta">
            {{ profile.age }} years old
            <span v-if="profile.parish"> • {{ profile.parish }}</span>
          </p>
        </div>

        <span
          v-if="showScore && profile.match_score !== undefined"
          class="match-score"
        >
          {{ profile.match_score }}%
        </span>
      </div>

      <p class="profile-bio">
        {{ profile.bio || 'No bio added yet.' }}
      </p>

      <div v-if="profile.interests && profile.interests.length" class="interest-list">
        <span
          v-for="interest in profile.interests"
          :key="interest"
          class="interest-pill"
        >
          {{ interest }}
        </span>
      </div>

      <div v-if="showActions" class="profile-card-actions">
        <button
          type="button"
          class="btn btn-outline-secondary"
          @click="$emit('pass', profile.id)"
        >
          Pass
        </button>

        <button
          type="button"
          class="btn btn-primary"
          @click="$emit('like', profile.id)"
        >
          Like
        </button>
      </div>

      <div v-if="showMessageButton" class="profile-card-actions">
        <RouterLink
          class="btn btn-primary w-100"
          :to="`/messages/${profile.user_id}`"
        >
          Message
        </RouterLink>
      </div>
    </div>
  </article>
</template>

<script>
import { RouterLink } from 'vue-router';
import { getPhotoUrl } from '../api/client';

export default {
  name: 'ProfileCard',

  components: {
    RouterLink
  },

  props: {
    // The profile object to display.
    profile: {
      type: Object,
      required: true
    },

    // Shows Like and Pass buttons on browse pages.
    showActions: {
      type: Boolean,
      default: false
    },

    // Shows a Message button on mutual match pages.
    showMessageButton: {
      type: Boolean,
      default: false
    },

    // Shows the match score if the backend provides one.
    showScore: {
      type: Boolean,
      default: true
    }
  },

  emits: ['like', 'pass'],

  computed: {
    // Converts the stored photo filename into a full backend image URL.
    photoUrl() {
      return getPhotoUrl(this.profile.photo);
    }
  }
};
</script>
