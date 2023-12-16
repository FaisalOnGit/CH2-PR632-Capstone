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
  talentQuestions,
  interestQuestions,
} = data;

app.use(bodyParser.json());

// Updated function to calculate personality based on user responses
function calculateTalent(answers) {
  const verbalTalent =
    (answers.slice(0, 4).filter((answer) => answer === "ya").length / 4) * 100;
  const matematisTalent =
    (answers.slice(4, 8).filter((answer) => answer === "ya").length / 4) * 100;
  const musikalTalent =
    (answers.slice(8, 12).filter((answer) => answer === "ya").length / 4) * 100;
  const kinestetikTalent =
    (answers.slice(12, 16).filter((answer) => answer === "ya").length / 4) *
    100;
  const interpersonalTalent =
    (answers.slice(16, 20).filter((answer) => answer === "ya").length / 4) *
    100;
  const intrapersonalTalent =
    (answers.slice(20, 24).filter((answer) => answer === "ya").length / 4) *
    100;
  const spasialTalent =
    (answers.slice(24, 28).filter((answer) => answer === "ya").length / 4) *
    100;
  const naturalistikTalent =
    (answers.slice(28, 32).filter((answer) => answer === "ya").length / 4) *
    100;

  const talentPercentages = {
    verbal: verbalTalent,
    matematis: matematisTalent,
    musikal: musikalTalent,
    kinestetik: kinestetikTalent,
    interpersonal: interpersonalTalent,
    intrapersonal: intrapersonalTalent,
    spasial: spasialTalent,
    naturalistik: naturalistikTalent,
  };

  return talentPercentages;
}

function calculateInterest(answers) {
  const socialInterest =
    (answers.slice(0, 4).filter((answer) => answer === "ya").length / 4) * 100;
  const artisticInterest =
    (answers.slice(4, 8).filter((answer) => answer === "ya").length / 4) * 100;
  const investigativeInterest =
    (answers.slice(8, 12).filter((answer) => answer === "ya").length / 4) * 100;
  const enterprisingInterest =
    (answers.slice(12, 16).filter((answer) => answer === "ya").length / 4) *
    100;
  const realisticInterest =
    (answers.slice(16, 20).filter((answer) => answer === "ya").length / 4) *
    100;

  const interestPercentages = {
    social: socialInterest,
    artistic: artisticInterest,
    investigative: investigativeInterest,
    enterprising: enterprisingInterest,
    realistic: realisticInterest,
  };

  return interestPercentages;
}

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

app.get("/talent-questions", (req, res) => {
  res.json({ questions: talentQuestions });
});

app.post("/calculate-talent", (req, res) => {
  const userAnswers = req.body.answers;
  const userTalent = calculateTalent(userAnswers);
  res.json({ talent: userTalent });
});

app.get("/interest-questions", (req, res) => {
  res.json({ questions: interestQuestions });
});

app.post("/calculate-interest", (req, res) => {
  const userAnswers = req.body.answers;
  const userInterest = calculateInterest(userAnswers);
  res.json({ interest: userInterest });
});

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

app.get("/questions", (req, res) => {
  res.json({ questions });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
