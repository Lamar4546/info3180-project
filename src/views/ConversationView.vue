<template>
  <main class="container py-5">
    <h1>Conversation</h1>
    <p>This page will show the message history with one matched user.</p>
  </main>
</template>

<script>
export default {
  name: 'ConversationView',
  props: {
    partnerId: {
      type: String,
      required: true
    }
  }
};
</script>
