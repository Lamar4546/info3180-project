<template>
  <div
    v-if="message"
    class="alert"
    :class="alertClass"
    role="alert"
  >
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'AlertMessage',

  props: {
    message: {
      type: String,
      default: ''
    },

    type: {
      type: String,
      default: 'info'
    }
  },

  computed: {
    // Converts the message type into a Bootstrap alert class.
    alertClass() {
      return {
        success: 'alert-success',
        error: 'alert-danger',
        warning: 'alert-warning',
        info: 'alert-info'
      }[this.type] || 'alert-info';
    }
  }
};
</script>
