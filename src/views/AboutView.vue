<template>
  <main class="page-section">
    <div class="container">
      <div class="page-card about-card">
        <p class="dashboard-kicker text-primary">About DriftDater</p>

        <h1>Connecting people through shared interests</h1>

        <p>
          DriftDater is a dating application that allows registered users to create profiles,
          browse compatible matches, like or pass on profiles, and message users after a mutual match.
        </p>

        <div class="row g-4 mt-3">
          <div class="col-md-4">
            <div class="about-feature">
              <span>👤</span>
              <h2>Profiles</h2>
              <p>
                Users can add personal details, interests, preferences, and profile photos.
              </p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="about-feature">
              <span>💘</span>
              <h2>Matching</h2>
              <p>
                DriftDater helps users discover profiles based on preferences and shared interests.
              </p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="about-feature">
              <span>💬</span>
              <h2>Messaging</h2>
              <p>
                Users can send messages after both people mutually like each other.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: 'AboutView'
};
</script>
