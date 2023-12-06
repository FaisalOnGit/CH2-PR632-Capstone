# Personality Test API Documentation

### This API allows users to take a personality test and receive their personality type based on their responses. The test is based on a set of questions and provides a personality type based on the user's answers.

## Base URL

http://localhost:3000

## Endpoints

### 1. Get Questions

Endpoint
GET /questions

Description
Retrieve a list of personality test questions

Status Code: 200 OK
Body:{
"questions": [
"Question 1",
"Question 2",
// ... (list of questions)
"Question N"
]
}

### 2. Calculate Personality

Endpoint
POST /calculate-personality

Description
Submit user responses to calculate their personality type.

Request
Method: POST
Body:{
"responses": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, /* ... */]
}
Response
Status Code: 200 OK
Body:{
"personality": "ISTJ",
"personalityDescription": "ISTJ is a reliable, tough, and detail-oriented individual...",
"famousPeople": ["George Washington", "Warren Buffett", "Angela Merkel"]
}

### 3. Get Response Scale

Endpoint
GET /response-scale

Description
Retrieve the response scale used in the personality test.

Response
Status Code: 200 OK
Body:{
"responseScale": ["1 (Not at all)", "2", "3", "4", "5 (Very Much)"]
}

## Example

### Fetch Questions

fetch('http://localhost:3000/questions')
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

### Submit User Responses

const userResponses = [/* user's responses array */];

fetch('http://localhost:3000/calculate-personality', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({ responses: userResponses }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

### Fetch Response Scale

fetch('http://localhost:3000/response-scale')
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
