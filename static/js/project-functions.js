async function determineChoice() {
    const response = await fetch("../assets/hangman_words.json");
    const words = await response.json();
    const choices = Object.entries(words);
    const randomIndex = Math.floor(Math.random() * choices.length);
    const [word, hint] = choices[randomIndex];
    return {
        word: word,
        hint: hint
    };
}

async function addData (wordHTMLElement, hintHTMLElement) {
    const choice = await determineChoice();
    const wordBlanksLen = choice.word.length;
    hintHTMLElement.innerHTML = `Hint: ${choice.hint}`;
    wordHTMLElement.innerHTML =
        Array.from({ length: wordBlanksLen }, (_, index) =>
        `<span class="empty-letter" id="blank-${index}">___</span>`
        ).join("");
    return choice.word;
}

function showNotice(noticeString, restartGame = false) {
    noticeText.textContent = noticeString;
    noticeRestart.hidden = !restartGame;
    if (restartGame) {
        noticeClose.hidden = true;
    }
    notice.classList.remove("show");
    void notice.offsetWidth;
    notice.classList.add("show");
}

function closeNotice() {
    notice.classList.remove("show");
}

function shakeHangman() {
    const hangmanDiv = document.getElementById("hangman-div");
    hangmanDiv.classList.remove("shake");
    void hangmanDiv.offsetWidth;
    hangmanDiv.classList.add("shake");
}

async function initializeGame() {
    newWord = await addData(wordHTMLElement, hintHTMLElement);
    finalWord = newWord.toLowerCase();
    inputField.value = ''
    guesses = [];
    hangmanImage.resetHangman()
    inputField.disabled = false;
    submitButton.disabled = false;
    console.log(finalWord);
}