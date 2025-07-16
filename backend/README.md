# Gaming Leaderboard Backend

This is the backend service for the Gaming Leaderboard application, built using FastAPI. The backend is responsible for handling player score submissions, retrieving the leaderboard, and checking player rankings.

## Project Structure

- `app/`: Contains the main application code.
  - `main.py`: Entry point for the FastAPI application.
  - `api/`: Contains API-related code.
    - `endpoints/`: Defines the API endpoints for leaderboard functionalities.
    - `dependencies.py`: Defines dependencies for the API routes.
  - `core/`: Contains core application logic.
    - `config.py`: Configuration settings for the application.
    - `database.py`: Database connection and interaction logic.
  - `models/`: Contains database models for the leaderboard system.
  - `schemas/`: Defines Pydantic schemas for request and response validation.
  - `services/`: Contains business logic for managing leaderboard data.

- `alembic/`: Contains migration scripts and configuration for database migrations.

- `requirements.txt`: Lists the dependencies required for the backend application.

- `Dockerfile`: Instructions for building a Docker image for the backend application.

## API Endpoints

1. **Submit Score**
   - **Endpoint:** `POST /api/leaderboard/submit`
   - **Description:** Accepts `user_id` and `score`, updates the score in the database.

2. **Get Leaderboard**
   - **Endpoint:** `GET /api/leaderboard/top`
   - **Description:** Retrieves the top 10 players sorted by `total_score`.

3. **Get Player Rank**
   - **Endpoint:** `GET /api/leaderboard/rank/{user_id}`
   - **Description:** Fetches the player's current rank.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gaming-leaderboard/backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

4. Access the API documentation at `http://localhost:8000/docs`.

## Database

Ensure that your database is set up and configured in `app/core/config.py`. Use Alembic for managing database migrations.

## Docker

To build and run the backend service using Docker, use the following commands:
```
docker build -t gaming-leaderboard-backend .
docker run -d -p 8000:8000 gaming-leaderboard-backend
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.