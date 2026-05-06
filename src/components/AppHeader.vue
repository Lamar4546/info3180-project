<template>
  <header class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm">
    <div class="container">
      <RouterLink class="navbar-brand d-flex align-items-center gap-2" to="/">
        <img
          src="../assets/images/DriftDaterLogo.png"
          alt="DriftDater Logo"
          class="navbar-logo"
        />
        <span>DriftDater</span>
      </RouterLink>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#mainNavbar"
        aria-controls="mainNavbar"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <nav id="mainNavbar" class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/">Home</RouterLink>
          </li>

          <!-- These links show when no user is logged in. -->
          <template v-if="!currentUser">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
          </template>

          <!-- These links show after the user logs in. -->
          <template v-else>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/browse">Browse</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/matches">Matches</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/messages">Messages</RouterLink>
            </li>

            <li class="nav-item">
              <button
                type="button"
                class="btn btn-link nav-link logout-link"
                @click="handleLogout"
              >
                Logout
              </button>
            </li>
          </template>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
import { RouterLink } from 'vue-router';
import { getCurrentUser, logoutUser } from '../api/client';

export default {
  name: 'AppHeader',

  components: {
    RouterLink
  },

  data() {
    return {
      // Stores the logged-in user if a Flask session exists.
      currentUser: null
    };
  },

  async mounted() {
    await this.checkCurrentUser();
  },

  watch: {
    /*
      Re-checks login status whenever the route changes.
      This keeps the navbar updated after login/logout navigation.
    */
    '$route.path': async function () {
      await this.checkCurrentUser();
    }
  },

  methods: {
    /*
      checkCurrentUser()

      Calls /api/auth/me to see whether a user is logged in.
      If the backend returns 401, the navbar treats the user as logged out.
    */
    async checkCurrentUser() {
      try {
        this.currentUser = await getCurrentUser();
      } catch {
        this.currentUser = null;
      }
    },

    /*
      handleLogout()

      Logs the user out using the Flask logout endpoint,
      updates the navbar, and sends them back to the login page.
    */
    async handleLogout() {
      try {
        await logoutUser();
      } finally {
        this.currentUser = null;
        this.$router.push('/login');
      }
    }
  }
};
</script>
