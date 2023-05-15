<template>
  <div class="container">
    <h1>Real-Time Chat</h1>
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
    <div class="card">
      <div class="card-body messages">
        <div v-for="message in messages" :key="message.id" class="message">
          <div class="message-header">
            <h2 class="message-username">{{ message.message.username}}</h2>
          </div>
          <div class="message-body">
            <p class="message-content">{{ message.message.message }}</p>
          </div>
        </div>
      </div>
    </div>

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
* {
  box-sizing: border-box;
}

html,
body,
div,
h2,
p,
label,
input,
textarea {
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, sans-serif;
  font-size: 16px;
  background-color: #1d1d1d;
  color: #fff;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.card-body {
  display: flex;
  flex-direction: column;
}

.message {
  margin: 0.5rem 0;
  background-color: #292929;
  border-radius: 5px;
  padding: 10px;
}

.message-header {
  color: #a35d41;
}

.message-username {
  font-size: 20px;
  font-weight: bold;
}

.message-content {
  color: #fff;
  font-size: 16px;
}

.form-inline {
  display: grid;
  grid-template-columns: 1fr;
}

.btn {
  margin: 0.5rem 0;
  text-align: center;
  line-height: 1.5;
  border-radius: 0.25rem;
  color: #fff;
  background-color: #a35d41;
  border-color: #a35d41;
  padding: 0.5rem 1rem;
}

.btn-primary:hover {
  color: #fff;
  background-color: #7b4530;
  border-color: #7b4530;
}

.btn-primary:focus,
.btn-primary.focus {
  box-shadow: 0 0 0 0.2rem rgba(163, 93, 65, 0.5);
}

.btn-primary.disabled,
.btn-primary:disabled {
  color: #fff;
  background-color: #a35d41;
  border-color: #a35d41;
}

.btn-primary:not(:disabled):not(.disabled):active,
.btn-primary:not(:disabled):not(.disabled).active,
.show > .btn-primary.dropdown-toggle {
  color: #fff;
  background-color: #7b4530;
  border-color: #7b4530;
}

.btn-primary:not(:disabled):not(.disabled):active:focus,
.btn-primary:not(:disabled):not(.disabled).active:focus,
.show > .btn-primary.dropdown-toggle:focus {
  box-shadow: 0 0 0 0.2rem rgba(163, 93, 65, 0.5);
}

.form-control {
  width: 100%;
  height: calc(1.5em + 0.75rem + 2px);
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #fff;
  background-color: #363636;
  background-clip: padding-box;
  border: 1px solid #555555;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  color: #fff;
  background-color: #363636;
  border-color: #a35d41;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(163, 93, 65, 0.25);
}
</style>