<template>
  <main class="page-section dashboard-page">
    <div class="container">
      <section class="dashboard-hero mb-4">
        <div>
          <p class="dashboard-kicker">Welcome back</p>
          <h1>Ready to find your next match?</h1>
          <p>
            Complete your profile, browse compatible users, and start conversations with mutual matches.
          </p>
        </div>

        <RouterLink class="btn btn-light dashboard-hero-btn" to="/profile/edit">
          Edit Profile
        </RouterLink>
      </section>

      <section class="row g-4 mb-4">
        <div class="col-md-4">
          <div class="dashboard-stat-card">
            <span class="stat-icon">💘</span>
            <div>
              <h2>0</h2>
              <p>New Matches</p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="dashboard-stat-card">
            <span class="stat-icon">💬</span>
            <div>
              <h2>0</h2>
              <p>Unread Messages</p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="dashboard-stat-card">
            <span class="stat-icon">⭐</span>
            <div>
              <h2>70%</h2>
              <p>Profile Complete</p>
            </div>
          </div>
        </div>
      </section>

      <section class="row g-4">
        <div class="col-lg-8">
          <div class="page-card h-100">
            <h2 class="section-title">What would you like to do?</h2>

            <div class="dashboard-action-list">
              <RouterLink class="dashboard-action" to="/browse">
                <span>🔍</span>
                <div>
                  <h3>Browse Matches</h3>
                  <p>Discover potential matches based on age, interests, and location.</p>
                </div>
              </RouterLink>

              <RouterLink class="dashboard-action" to="/matches">
                <span>💕</span>
                <div>
                  <h3>Your Matches</h3>
                  <p>View users who mutually liked you and are ready to connect.</p>
                </div>
              </RouterLink>

              <RouterLink class="dashboard-action" to="/messages">
                <span>📩</span>
                <div>
                  <h3>Messages</h3>
                  <p>Continue conversations with people you have matched with.</p>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="page-card h-100">
            <h2 class="section-title">Next Steps</h2>

            <ul class="dashboard-checklist">
              <li>Upload a profile picture</li>
              <li>Add at least 3 interests</li>
              <li>Set your age preferences</li>
              <li>Use location to improve matches</li>
            </ul>

            <RouterLink class="btn btn-primary w-100 mt-3" to="/profile/edit">
              Complete Profile
            </RouterLink>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  name: 'DashboardView',

  components: {
    RouterLink
  }
};
</script>
