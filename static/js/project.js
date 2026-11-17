const wordHTMLElement = document.getElementById("hangman-letters");
const hintHTMLElement = document.getElementById("hangman-hint");
let inputField = document.getElementById("letter-choice");
const submitButton = document.getElementById('letter-submit');
const notice = document.getElementById("notice");
const noticeText = document.getElementById("notice-text");
const noticeClose = document.getElementById("notice-close");
const noticeRestart = document.getElementById("notice-restart");
let hangmanImage = new HangmanImage();
let finalWord = ''
let guesses = [];


submitButton.addEventListener('click', (e) => {
    e.preventDefault();
    currentInput = inputField.value.toLowerCase();
    inputField.value = "";
    if (!/^[a-z]$/.test(currentInput)) {
        showNotice("Please enter a single alphabetic character.");
    }
    else if (currentInput.length < 1) {
        showNotice("Please enter a character.");
    }
    else if (guesses.includes(currentInput)) {
        showNotice(`You have already chosen the letter: ${currentInput}`);
    }
    else {
        guesses.push(currentInput);
        if (finalWord.includes(currentInput)) {
            for (let index = 0; index < finalWord.length; index++) {
                if (finalWord[index] === currentInput) {
                    const blank = document.getElementById(`blank-${index}`);
                    blank.textContent = currentInput;
                }
            }
            win = true;
            for (let index = 0; index < finalWord.length; index++) {
                const currentLetter = document.getElementById(`blank-${index}`);
                console.log(currentLetter.textContent);
                if (currentLetter.textContent === `___`) {
                    win = false;
                }
            }
            if (win) {
                inputField.disabled = true;
                submitButton.disabled = true;
                showNotice(`You win! :)`, true);
            }
        }
        else {
            shakeHangman()
            gameOver = hangmanImage.incrementHangman();
            if (gameOver) {
                inputField.disabled = true;
                submitButton.disabled = true;
                showNotice(`You have lost :(`, true);
            }
        }
    }
})

noticeClose.addEventListener("click", closeNotice);
noticeRestart.addEventListener("click", () => {
    closeNotice();
    initializeGame()
    location.reload();
});

initializeGame()