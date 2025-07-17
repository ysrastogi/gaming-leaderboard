# Gaming Leaderboard System

This project implements a scalable gaming leaderboard system using Next.js for the frontend and FastAPI for the backend. The leaderboard tracks player performance based on scores submitted after gameplay, allowing players to view their rankings and compare with others.

## Project Structure

The project is organized into two main directories: `frontend` and `backend`.

### Frontend

The frontend is built with Next.js and includes the following key components:

- **Public Assets**: Contains static files like the favicon.
- **App Structure**: The main application files are located in `src/app`, including the main page and layout.
- **Components**: Reusable components such as `Leaderboard`, `PlayerCard`, and `ScoreSubmission` are located in `src/components`.
- **API Integration**: The `lib/api.ts` file handles API calls to the backend.
- **Custom Hooks**: The `hooks/useLeaderboard.ts` file manages the leaderboard state.

### Backend

The backend is built with FastAPI and includes:

- **Main Application**: The entry point is `app/main.py`, which sets up the FastAPI application and routes.
- **API Endpoints**: The `api/endpoints/leaderboard.py` file contains the API endpoints for submitting scores, retrieving the leaderboard, and fetching player ranks.
- **Database Models**: The `models/leaderboard.py` file defines the database schema for leaderboard data.
- **Services**: Business logic for managing leaderboard data is implemented in `services/leaderboard_service.py`.

## API Endpoints

The following API endpoints are implemented:

1. **Submit Score**: 
   - **POST** `/api/leaderboard/submit`
   - Accepts `user_id` and `score` to update the player's score.

2. **Get Leaderboard**: 
   - **GET** `/api/leaderboard/top`
   - Retrieves the top 10 players sorted by total score.

3. **Get Player Rank**: 
   - **GET** `/api/leaderboard/rank/{user_id}`
   - Fetches the current rank of the specified player.

## CLI Commands

The backend provides several CLI commands to manage the database and perform administrative tasks. These commands can be found in `backend/cli.py`.

### Available Commands

1. **Initialize Database**
   ```bash
   python -m backend.cli init-db
   ```
   Initializes the database by running all Alembic migrations.

2. **Populate Database**
   ```bash
   python -m backend.cli populate [OPTIONS]
   ```
   Populates the database with test data.

   Options:
   - `--users INTEGER`: Number of users to create (default: 1,000,000)
   - `--sessions INTEGER`: Number of game sessions to create (default: 5,000,000)
   - `--clear`: Clear all data before populating
   - `--users-only`: Only populate users
   - `--sessions-only`: Only populate game sessions
   - `--leaderboard-only`: Only populate leaderboard

3. **Execute SQL**
   ```bash
   python -m backend.cli execute-sql --sql-file PATH
   ```
   Executes a SQL file against the database.

   Options:
   - `--sql-file PATH`: Path to the SQL file to execute


## Scalability

The system is designed to handle up to 1 million records efficiently. The backend utilizes a robust database management system, and the frontend is optimized for performance to ensure a smooth user experience.

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gaming-leaderboard
   ```

2. Set up the backend:
   - Navigate to the `backend` directory and install dependencies:
     ```
     cd backend
     pip install -r requirements.txt
     ```
   - Run the FastAPI application:
     ```
     uvicorn app.main:app --reload
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory and install dependencies:
     ```
     cd frontend
     npm install
     ```
   - Run the Next.js application:
     ```
     npm run dev
     ```

4. Access the application:
   - Open your browser and go to `http://localhost:3000` for the frontend.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
