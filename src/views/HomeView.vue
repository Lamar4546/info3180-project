<template>
  <main class="home-page">
    <section class="hero-section text-center">
      <div class="container">
        <h1 class="display-4 fw-bold mb-3">Find meaningful matches with DriftDater</h1>

        <p class="lead text-muted mb-4">
          Create your profile, discover compatible users, and connect with people who share your interests.
        </p>

        <div class="d-flex justify-content-center gap-3 flex-wrap">
          <RouterLink class="btn btn-primary btn-lg" to="/register">
            Create Account
          </RouterLink>

          <RouterLink class="btn btn-outline-primary btn-lg" to="/login">
            Login
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="container py-5">
      <div class="row g-4">
        <div class="col-md-4">
          <div class="feature-card h-100">
            <h2 class="h5 fw-bold">Build Your Profile</h2>
            <p class="text-muted mb-0">
              Add your personal details, interests, location, preferences, and profile photo.
            </p>
          </div>
        </div>

        <div class="col-md-4">
          <div class="feature-card h-100">
            <h2 class="h5 fw-bold">Browse Matches</h2>
            <p class="text-muted mb-0">
              Search and filter potential matches based on age, location, interests, and compatibility.
            </p>
          </div>
        </div>

        <div class="col-md-4">
          <div class="feature-card h-100">
            <h2 class="h5 fw-bold">Start Conversations</h2>
            <p class="text-muted mb-0">
              Message users only after both people mutually like each other.
            </p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  name: 'HomeView',
  components: {
    RouterLink
  }
};
</script>
