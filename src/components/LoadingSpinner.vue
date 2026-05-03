<template>
  <div class="text-center py-4">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>

    <p v-if="message" class="text-muted mt-2 mb-0">
      {{ message }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',

  props: {
    message: {
      type: String,
      default: 'Loading...'
    }
  }
};
</script>
