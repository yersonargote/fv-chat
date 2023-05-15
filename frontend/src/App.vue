<!-- App.vue -->
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

<script lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const username = ref('')
    const message = ref('')
    const messages = ref([])
    let socket: WebSocket | null = null

    const getMessages = async () => {
      const response = await axios.get('/api/messages')
      messages.value = response.data
    }

    const sendMessage = async () => {
      if (socket) {
        const messageObj = {
          username: username.value,
          message: message.value,
        }
        socket.send(JSON.stringify(messageObj))
        message.value = ''
      }
    }

    onMounted(() => {
      socket = new WebSocket('ws://localhost:8000/ws')
      socket.addEventListener('message', (event) => {
        const message = JSON.parse(event.data)
        messages.value.push(message)
      })
      getMessages()
    })

    return {
      username,
      message,
      messages,
      sendMessage,
    }
  },
}
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
  background-color: #f5f5f5;
  border-radius: 5px;
}

.message-header {
  color: #005cbf;
}

.message-username {
  font-size: 20px;
  font-weight: bold;
}

.message-content {
  color: black;
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
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  color: #fff;
  background-color: #0069d9;
  border-color: #0062cc;
}

.btn-primary:focus,
.btn-primary.focus {
  box-shadow: 0 0 0 0.2rem rgba(38, 143, 255, 0.5);
}

.btn-primary.disabled,
.btn-primary:disabled {
  color: #fff;
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:not(:disabled):not(.disabled):active,
.btn-primary:not(:disabled):not(.disabled).active,
.show>.btn-primary.dropdown-toggle {
  color: #fff;
  background-color: #0062cc;
  border-color: #005cbf;
}

.btn-primary:not(:disabled):not(.disabled):active:focus,
.btn-primary:not(:disabled):not(.disabled).active:focus,
.show>.btn-primary.dropdown-toggle:focus {
  box-shadow: 0 0 0 0.2rem rgba(38, 143, 255, 0.5);
}

.form-control {
  width: 100%;
  height: calc(1.5em + 0.75rem + 2px);
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out,
    box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  color: #495057;
  background-color: #fff;
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>

