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

          <li class="nav-item">
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/register">Register</RouterLink>
          </li>

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
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  name: 'AppHeader',
  components: {
    RouterLink
  }
};
</script>
