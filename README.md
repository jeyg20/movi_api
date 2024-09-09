# Movie api

This API is built with FastAPI, it performs all CRUD operetions on a SQlite databse
for managing movies.

## API Endpoints

| Method | Endpoint             | Description             |
|--------|----------------------|-------------------------|
| POST   | `/login`             | Login aunthentication   |
| GET    | `/movies`            | Get all movies          |
| GET    | `/movies/{movie_id}` | Get a movie by ID       |
| GET    | `/movies/{category}` | Get movies by category  |
| POST   | `/movies`            | Create a new movie      |
| POST   | `/movies/batch`      | Create multilple movies |
| PUT    | `/movies/{movie_id}` | Update a movie by ID    |
| PATCH  | `/movies/{movie_id}` | Patch a movie by ID     |
| DELETE | `/movies/{movie_id}` | Delete a movie by ID    |
