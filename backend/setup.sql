CREATE DATABASE postgres;
\c mydb;
CREATE TABLE chat_messages (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255),
  message TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);