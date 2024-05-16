let questions = [];

let currentQuestionIndex = 0;
let correctAnswers = 0; // Track correct answers
const questionTextElement = document.getElementById('questionText');
const questionNumberElement = document.getElementById('questionNumber');
const answerForm = document.getElementById('answerForm');
const nextButton = document.getElementById('nextButton');
const quizContainer = document.getElementById('actualcontainer');
const startContainer = document.getElementById('quizouter');
const quizResultsDiv = document.getElementById('quizResults');
const resultText = document.getElementById('resultText');
const whiteBoxes = document.querySelectorAll('.white-box');
document.getElementById('submitButton').addEventListener('click', showCorrectAnswer);

const returnButton = document.createElement('button');
returnButton.setAttribute('class', 'returnbutton');
returnButton.appendChild
returnButton.textContent = 'Return';
returnButton.addEventListener('click', function() {
    // Refresh the page
    location.reload();
});

// Append the return button to the results div
quizResultsDiv.appendChild(returnButton);
// Function to display the current question
function displayQuestion() {
    const currentQuestion = questions[currentQuestionIndex];
    questionTextElement.textContent = `${currentQuestion.question}`;
    questionNumberElement.textContent = currentQuestionIndex + 1;

    // Clear previous options
    answerForm.innerHTML = '';

    // Add options
    currentQuestion.options.forEach((option, index) => {
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'answer';
        input.value = option;
        input.id = `option${index + 1}`;
        label.htmlFor = `option${index + 1}`;
        label.textContent = option;
        label.classList.add('radioinput');
        label.insertBefore(input, label.firstChild); // Insert input before label text
        answerForm.appendChild(label);
        answerForm.appendChild(document.createElement('br'));

        // Disable the next button initially
    document.getElementById('nextButton').disabled = true;
    });
}

function showCorrectAnswer() {
    const selectedAnswer = document.querySelector('input[name="answer"]:checked');
    if (!selectedAnswer) {
        alert("Please select an answer.");
        return;
    }

    const userAnswer = selectedAnswer.value;
    const correctAnswer = questions[currentQuestionIndex].correctAnswer;

    // Mark the correct answer and wrong answer
    const labels = document.querySelectorAll('label.radioinput');
    labels.forEach(label => {
        if (label.textContent.trim() === correctAnswer) {
            label.classList.add('correct-answer');
        } else if (label.textContent.trim() === userAnswer) {
            label.classList.add('wrong-answer');
        }
    });

     // Disable all radio buttons
     const radioButtons = document.querySelectorAll('input[name="answer"]');
     radioButtons.forEach(button => {
         button.disabled = true;
     });

     document.getElementById('nextButton').disabled = false;
}

// Function to handle next button click
function nextQuestion() {
    // Get selected answer
    const selectedAnswer = document.querySelector('input[name="answer"]:checked');
    if (!selectedAnswer) {
        alert("Please select an answer.");
        return;
    }
    const userAnswer = selectedAnswer.value;

    // Check if answer is correct
    const correctAnswer = questions[currentQuestionIndex].correctAnswer;
    if (userAnswer === correctAnswer) {
        correctAnswers++; // Increment correct answers count
    }

    const labels = document.querySelectorAll('label.radioinput');
    labels.forEach(label => {
        if (label.textContent.trim() === correctAnswer) {
            label.classList.add('correct-answer');
        }
    });

    // Move to next question
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        displayQuestion();
    } else {
        whiteBoxes.forEach(box => {
            box.style.width = '60%';
        });
        const totalQuestions = questions.length;
        const percentage = ((correctAnswers / totalQuestions) * 100).toFixed(2);
        resultText.textContent = `You got ${correctAnswers}/${totalQuestions} correct (${percentage}%)`;
        quizContainer.style.display = 'none'; // Hide quiz container
        quizResultsDiv.style.display = 'block'; // Show results
    }
}

// Event listener for next button click
nextButton.addEventListener('click', nextQuestion);

// Event listener for start quiz button click
startQuizButton.addEventListener('click', function() {
    

    // Loop through each element and set its width to 100%
    whiteBoxes.forEach(box => {
        box.style.width = '100%';
    });
        startContainer.style.display = 'none';
        quizContainer.style.display = 'block';
    // Display the first question
    displayQuestion();
});