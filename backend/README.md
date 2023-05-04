# Chat

# Backend

## Setup database

```sql
-- Create the chat_messages table
CREATE TABLE chat_messages (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255),
  message TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Run the server

```bash
uvicorn main:app --reload
```

# Frontend

## Run the server

```bash
cd frontend
pnpm run dev
# npm run dev
```