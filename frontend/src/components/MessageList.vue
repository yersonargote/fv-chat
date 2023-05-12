<template>
    <div class="message">
      <div class="message-header">
        <h2 class="message-username">{{ message.username }}</h2>
      </div>
      <div class="message-body">
        <p class="message-content">{{ message.message }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ["message"],
  };
  </script>

<style scoped>
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
</style>
