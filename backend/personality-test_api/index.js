const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const port = 3000;
app.use(cors());

// Assuming data.json is in the same directory as index.js
const data = require("./data.json");
const {
  questions,
  personalityDescriptions,
  responseScale,
  famousPeople,
  title,
  gambar,
} = data;

app.use(bodyParser.json());

// Updated function to calculate personality based on user responses
function calculatePersonality(answers) {
  const extrovertAnswers = answers.slice(0, 10);
  const sensingAnswers = answers.slice(10, 20);
  const thinkingAnswers = answers.slice(20, 30);
  const judgingAnswers = answers.slice(30, 40);

  const extrovertScore = extrovertAnswers.reduce((a, b) => a + b, 0);
  const sensingScore = sensingAnswers.reduce((a, b) => a + b, 0);
  const thinkingScore = thinkingAnswers.reduce((a, b) => a + b, 0);
  const judgingScore = judgingAnswers.reduce((a, b) => a + b, 0);

  let personality = "";

  if (extrovertScore > 25) {
    personality += "E";
  } else {
    personality += "I";
  }

  if (sensingScore > 25) {
    personality += "S";
  } else {
    personality += "N";
  }

  if (thinkingScore > 25) {
    personality += "T";
  } else {
    personality += "F";
  }

  if (judgingScore > 25) {
    personality += "J";
  } else {
    personality += "P";
  }

  return personality;
}

// API endpoint to calculate personality based on user responses
app.post("/calculate-personality", (req, res) => {
  const userResponses = req.body.responses.map(Number);
  const userPersonality = calculatePersonality(userResponses);
  const personalityDescription = personalityDescriptions[userPersonality];
  const famousPeopleList = famousPeople[userPersonality];
  const personalityTitle = title[userPersonality];
  const personalityImage = gambar[userPersonality];

  res.json({
    personality: userPersonality,
    title: personalityTitle,
    description: personalityDescription,
    famousPeople: famousPeopleList,
    image: personalityImage,
  });
});

// Endpoint to get the list of questions
app.get("/questions", (req, res) => {
  res.json({ questions });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
