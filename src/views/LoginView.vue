<template>
  <main class="auth-page">
    <section class="auth-card">
      <h1 class="text-center mb-4">Login</h1>

      <!-- Shows login errors or success messages. -->
      <AlertMessage :message="errorMessage" type="error" />
      <AlertMessage :message="successMessage" type="success" />

      <!-- Vue handles the submit so the browser does not reload the page. -->
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model.trim="form.email"
            type="email"
            class="form-control"
            placeholder="your@email.com"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-control"
            placeholder="Password"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <LoadingSpinner
        v-if="isLoading"
        message="Checking your login details..."
      />

      <p class="text-center mt-3 mb-0">
        Don't have an account?
        <RouterLink to="/register">Sign up here</RouterLink>
      </p>
    </section>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router';
import { loginUser } from '../api/client';
import AlertMessage from '../components/AlertMessage.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
  name: 'LoginView',

  components: {
    RouterLink,
    AlertMessage,
    LoadingSpinner
  },

  data() {
    return {
      // Stores the values typed into the login form.
      form: {
        email: '',
        password: ''
      },

      // Controls loading state and feedback messages.
      isLoading: false,
      errorMessage: '',
      successMessage: ''
    };
  },

  methods: {
    /*
      Sends the login details to Flask.
      If successful, the user is redirected to the dashboard.
    */
    async handleLogin() {
      this.errorMessage = '';
      this.successMessage = '';

      if (!this.form.email || !this.form.password) {
        this.errorMessage = 'Please enter both email and password.';
        return;
      }

      try {
        this.isLoading = true;

        await loginUser(this.form);

        this.successMessage = 'Login successful. Redirecting...';

        setTimeout(() => {
          const redirectPath = this.$route.query.redirect || '/dashboard';
          this.$router.push(redirectPath);
        }, 700);
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>
