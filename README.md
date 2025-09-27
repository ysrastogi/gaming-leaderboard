# Gaming Leaderboard System

This project implements a scalable gaming leaderboard system using Next.js for the frontend and FastAPI for the backend. The leaderboard tracks player performance based on scores submitted after gameplay, allowing players to view their rankings and compare with others.

## Project Structure


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

## Scalability

The system is designed to handle up to 1 million records efficiently. The backend utilizes a robust database management system.

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
     pip install -r requirements.txt
     ```
   - Run the FastAPI application:
     ```
     uvicorn app.main:app --reload
     ```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.