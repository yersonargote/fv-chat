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

### Docker compose
  
```bash
docker-compose up -d
```

### Run with poetry

- Install [poetry](https://python-poetry.org/docs/#installation)

```bash
poetry install
poetry shell
uvicorn backend.main:app --reload
```
