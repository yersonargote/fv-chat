<template>
  <div class="container">
    <h1>Real-Time Chat</h1>
    <div class="card">
      <div class="card-body messages">
        <div v-for="message in messages" :key="message.id" class="message">
          <strong>{{ message.username }}:</strong> {{ message.message }}
        </div>
      </div>
    </div>
    <form class="form-inline" @submit.prevent="sendMessage">
      <div class="form-group">
        <label for="username">Username:</label>
        <input v-model="username" id="username" type="text" class="form-control" placeholder="Your username">
      </div>
      <div class="form-group mx-sm-3">
        <label for="message">Message:</label>
        <input v-model="message" id="message" type="text" class="form-control" placeholder="Your message">
      </div>
      <button type="submit" class="btn btn-primary">Send</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      message: "",
      messages: [],
      socket: null,
    };
  },
  mounted() {
    this.socket = new WebSocket("ws://localhost:8000/ws");
    this.socket.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      this.messages.push(message);
    });
    this.getMessages();
  },
  methods: {
    async getMessages() {
      const response = await this.$axios.$get("/api/messages");
      this.messages = response;
    },
    async sendMessage() {
      const message = {
        username: this.username,
        message: this.message,
      };
      this.socket.send(JSON.stringify(message));
      this.message = "";
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.card {
  margin-top: 20px;
}
.messages {
  max-height: 400px;
  overflow-y: auto;
}
.message {
  margin-bottom: 10px;
}
</style>
