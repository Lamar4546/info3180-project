<template>
  <div class="app-wrapper">
    <AppHeader />

    <main class="app-main">
      <RouterView />
    </main>

    <AppFooter />
  </div>
</template>

<script>
import { RouterView } from 'vue-router';
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';

export default {
  name: 'App',
  components: {
    RouterView,
    AppHeader,
    AppFooter
  }
};
</script>
