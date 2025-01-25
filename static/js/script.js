let startTime;
let timerInterval;

async function fetchAndDisplaySentence() {
    const response = await fetch("/get_sentence");
    const data = await response.json();
    document.getElementById("sentence").innerText = data.sentence;
    document.getElementById("typedText").value = ""; // Clear the text area
}

function resetStats() {
    clearInterval(timerInterval);
    startTime = null;
    document.getElementById("time").innerText = "Time: 0s";
    document.getElementById("wpm").innerText = "WPM: 0";
    document.getElementById("accuracy").innerText = "Accuracy: 0%";
}

function startTimer() {
    if (!startTime) {
        startTime = Date.now();
        timerInterval = setInterval(updateTimer, 100);
    }
}

function updateTimer() {
    const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(1);
    document.getElementById("time").innerText = `Time: ${elapsedTime}s`;
}

async function finishTest() {
    clearInterval(timerInterval);

    const typedText = document.getElementById("typedText").value;
    const originalText = document.getElementById("sentence").innerText;
    const timeTaken = (Date.now() - startTime) / 1000;

    const response = await fetch("/result", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ typed_text: typedText, original_text: originalText, time_taken: timeTaken }),
    });

    const data = await response.json();

    if (data.error) {
        alert(`Error: ${data.error}`);
    } else {
        document.getElementById("wpm").innerText = `WPM: ${data.wpm}`;
        document.getElementById("accuracy").innerText = `Accuracy: ${data.accuracy}%`;
    }
}

window.onload = () => {
    fetchAndDisplaySentence();
    document.getElementById("typedText").addEventListener("input", startTimer);

    // Add event listener to detect "Enter" key press
    document.getElementById("typedText").addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent default behavior of a new line
            finishTest(); // Trigger finishTest function on Enter key
        }
    });

    // Add event listener to Restart button
    document.getElementById("restartBtn").addEventListener("click", function () {
        location.reload(); // Refresh the page
    });
};
