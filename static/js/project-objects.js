class HangmanImage {
    imageSrcStatic = '../static/img/hangmanimgs/hangman_'

    constructor() {
        this.imgElement = document.getElementById("hangman-img");
        this.imageNr = 1
        this.currentImageSrc = this.imageSrcStatic + this.imageNr + '.png'
    }

    incrementHangman() {
        console.log(this.imageNr)
        this.imageNr++;
        this.currentImageSrc = this.imageSrcStatic + this.imageNr + '.png'
        console.log(this.imageNr)
        console.log(this.currentImageSrc);
        this.imgElement.src = this.currentImageSrc;
        return this.imageNr === 7;
    }

    resetHangman() {
        this.imageNr = 1
        this.currentImageSrc = this.imageSrcStatic + this.imageNr + '.png'
        this.imgElement.src = this.currentImageSrc;
    }
}