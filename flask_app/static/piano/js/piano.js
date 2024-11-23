// Key sounds
const sound = {
    65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav", // A
    87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav", // W
    83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav", // S
    69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav", // E
    68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav", // D
    70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav", // F
    84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav", // T
    71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav", // G
    89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav", // Y
    72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav", // H
    85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav", // U
    74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav", // J
    75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav", // K
    79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav", // O
    76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav", // L
    80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav", // P
    186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav", // ;
};

//String of typed letters
let typedSequence = "";

// Function to play sound
function playSound(keyCode) {
    let audio = new Audio(sound[keyCode]);
    if (audio) {
        audio.play();
    }
}

// Function show a key press visially
function keyPress(keyElement) {
    keyElement.classList.add("pressed");  // Apply visual effect
    setTimeout(() => {
        keyElement.classList.remove("pressed");  // Remove visual effect after 150ms
    }, 150);
}

// Function that handles when a key is played
function playKey(event) {
    let keyCode = event.keyCode;
    let keyElement = document.querySelector(`.key[data-key="${keyCode}"]`);
    
    if (keyElement) {
        playSound(keyCode);
        keyPress(keyElement);
    }
    
    let keyPlayed = event.key.toLowerCase();
    typedSequence += keyPlayed;
    
    if (typedSequence.includes("weseeyou")) {
        awaken();
        typedSequence = "";  // Reset
    }
}

// Function that handles when a key is played via mouse
function mouseClickKey(event) {
    let keyElement = event.target.closest('.key'); 
    if (keyElement) {
        let keyCode = keyElement.getAttribute('data-key');
        playSound(keyCode); 
        keyPress(keyElement);  
        let keyLetter = keyElement.querySelector('span').textContent.toLowerCase();
        typedSequence += keyLetter;

        if (typedSequence.includes("weseeyou")) {
            awaken();
            typedSequence = "";  // Reset
        }
    }
}

// Awaken the great old one function
function awaken() {
    let pianoContainer = document.querySelector(".piano-container");
    let piano = document.querySelector(".piano");
    piano.classList.add("fade-out");  // Add fade-out animation

    document.removeEventListener("keydown", playKey); //Stop playing keys
    document.querySelectorAll('.key').forEach(key => {
        key.removeEventListener('click', mouseClickKey);
    });

    setTimeout(() => {
        piano.style.display = "none"; 

        let greatOldOneImage = document.createElement("img");
        greatOldOneImage.src = "/static/piano/images/texture.jpeg";
        greatOldOneImage.classList.add("great-old-one");

        pianoContainer.appendChild(greatOldOneImage);

        let creepySound = new Audio("/static/piano/images/Creepy-piano-sound-effect.mp3");  // Provide the correct sound path
        creepySound.play();
    }, 1000);  
}

document.addEventListener("keydown", playKey);
document.querySelectorAll('.key').forEach(key => {
    key.addEventListener('click', mouseClickKey);
});
