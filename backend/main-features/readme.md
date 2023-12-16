# Petamimpi API

This is a simple Express.js API for a personality quiz that calculates personality, talent, and interest based on user responses. The API provides endpoints to retrieve questions and perform calculations.

## Installation

Clone the repository to your local machine:
https://github.com/FaisalOnGit/CH2-PR632-Capstone.git

### npm install

### Running the Server

### Start the server by running:

### npm start

The server will run on http://localhost:3000.

## Endpoints

1. Calculate Talent
   Endpoint: /calculate-talent
   Method: POST
   Request Body:
   json
   Copy code
   {
   "answers": ["ya", "tidak", "ya", "tidak", ...]
   }
   Response:
   json
   Copy code
   {
   "talent": {
   "verbal": 25,
   "matematis": 50,
   "musikal": 75,
   "kinestetik": 30,
   "interpersonal": 40,
   "intrapersonal": 60,
   "spasial": 80,
   "naturalistik": 45
   }
   }
2. Get Talent Questions
   Endpoint: /talent-questions
   Method: GET
   Response:
   json
   Copy code
   {
   "questions": ["Question 1", "Question 2", "Question 3", ...]
   }
3. Calculate Interest
   Endpoint: /calculate-interest
   Method: POST
   Request Body:
   json
   Copy code
   {
   "answers": ["ya", "tidak", "ya", "tidak", ...]
   }
   Response:
   json
   Copy code
   {
   "interest": {
   "social": 25,
   "artistic": 50,
   "investigative": 75,
   "enterprising": 30,
   "realistic": 40
   }
   }
4. Get Interest Questions
   Endpoint: /interest-questions
   Method: GET
   Response:
   json
   Copy code
   {
   "questions": ["Question 1", "Question 2", "Question 3", ...]
   }
5. Calculate Personality
   Endpoint: /calculate-personality
   Method: POST
   Request Body:
   json
   Copy code
   {
   "responses": [1, 2, 3, 4, 5, ...]
   }
   Response:
   json
   Copy code
   {
   "personality": "ENTJ",
   "title": "Commander",
   "description": "Commanders are natural-born leaders...",
   "famousPeople": ["Steve Jobs", "Margaret Thatcher"],
   "image": "https://example.com/entj-image.jpg"
   }
6. Get All Questions
   Endpoint: /questions
   Method: GET
   Response:
   json
   Copy code
   {
   "questions": ["Question 1", "Question 2", "Question 3", ...]
   }
   Usage
7. Calculate Talent
   To calculate talent, send a POST request to /calculate-talent with user answers. You can get talent questions using /talent-questions.

8. Calculate Interest
   To calculate interest, send a POST request to /calculate-interest with user answers. You can get interest questions using /interest-questions.

9. Calculate Personality
   To calculate personality, send a POST request to /calculate-personality with user responses. You can get all questions using /questions.

Example Usage
You can refer to the HTML file or use tools like Postman to interact with the API endpoints.

Feel free to customize and adapt this README according to your project's specifics.
