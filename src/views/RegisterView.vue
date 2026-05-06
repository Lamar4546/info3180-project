<template>
  <main class="auth-page">
    <section class="auth-card auth-card-wide">
      <h1>Sign Up</h1>

      <AlertMessage :message="errorMessage" type="error" />
      <AlertMessage :message="successMessage" type="success" />

      <form @submit.prevent="handleRegister">
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
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model.trim="form.username"
            type="text"
            class="form-control"
            placeholder="username"
            required
          />
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="firstName" class="form-label">First Name</label>
            <input
              id="firstName"
              v-model.trim="form.first_name"
              type="text"
              class="form-control"
              placeholder="First Name"
              required
            />
          </div>

          <div class="col-md-6 mb-3">
            <label for="lastName" class="form-label">Last Name</label>
            <input
              id="lastName"
              v-model.trim="form.last_name"
              type="text"
              class="form-control"
              placeholder="Last Name"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label for="dateOfBirth" class="form-label">Date of Birth</label>
          <input
            id="dateOfBirth"
            v-model="form.date_of_birth"
            type="date"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label for="gender" class="form-label">Gender</label>
          <select
            id="gender"
            v-model="form.gender"
            class="form-select"
            required
          >
            <option value="">Select gender</option>
            <option value="Female">Female</option>
            <option value="Male">Male</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="mb-3">
          <label for="lookingFor" class="form-label">Looking For</label>
          <select
            id="lookingFor"
            v-model="form.looking_for"
            class="form-select"
          >
            <option value="Any">Any</option>
            <option value="Female">Female</option>
            <option value="Male">Male</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="mb-3">
          <label for="parish" class="form-label">Location / Parish</label>
          <input
            id="parish"
            v-model.trim="form.parish"
            type="text"
            class="form-control"
            placeholder="eg: Kingston, Jamaica"
          />
        </div>

        <div class="mb-3">
          <label for="bio" class="form-label">Short Bio</label>
          <textarea
            id="bio"
            v-model.trim="form.bio"
            class="form-control"
            rows="3"
            placeholder="Write a short introduction..."
          ></textarea>
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
          <small class="text-muted">Password must be at least 8 characters.</small>
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Creating account...' : 'Sign Up' }}
        </button>
      </form>

      <LoadingSpinner
        v-if="isLoading"
        message="Creating your DriftDater account..."
      />

      <p class="auth-link-text mt-3 mb-0">
        Already have an account?
        <RouterLink to="/login">Login here</RouterLink>
      </p>
    </section>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router';
import { registerUser } from '../api/client';
import AlertMessage from '../components/AlertMessage.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
  name: 'RegisterView',

  components: {
    RouterLink,
    AlertMessage,
    LoadingSpinner
  },

  data() {
    return {
      form: {
        email: '',
        username: '',
        password: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        gender: '',
        looking_for: 'Any',
        parish: '',
        bio: ''
      },
      isLoading: false,
      errorMessage: '',
      successMessage: ''
    };
  },

  methods: {
    /*
      Sends the registration form to Flask.
      If successful, Flask creates the user and logs them in.
    */
    async handleRegister() {
      this.errorMessage = '';
      this.successMessage = '';

      if (this.form.password.length < 8) {
        this.errorMessage = 'Password must be at least 8 characters long.';
        return;
      }

      try {
        this.isLoading = true;

        await registerUser(this.form);

        this.successMessage = 'Account created successfully. Redirecting...';

        setTimeout(() => {
          this.$router.push('/dashboard');
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
