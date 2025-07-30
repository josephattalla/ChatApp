# Chat Application

### Problem Description

This application provides a group messaging service with role-based moderation and administration and real-time updates through websockets. Each part of the application is containerized with Docker to allow distributed deployment on the cloud.

### Interface Quirks

Admin role configuration is located in the settings.

### Backend Libraries

- fastapi
- psycopg
- pyjwt
- passlib
- bcrypt
- pytest

### Frontend Libraries

- vite
- react
- react-use-websocket

### Other Resources

- PostgreSQL
- Docker

### Running the App

The only dependency is docker.

```bash
docker-compose up
```

The front page is accessible at http://localhost:5173/.

#### Contributions

#### Joseph Attalla

Built the API endpoints and the backend logic.

#### Gabriel Clewis

Wrote tests hitting the API endpoints.

#### Justin Taing

Initialized database schema and created models.

#### Wilson Shi

Built the interface and containerized the application.
