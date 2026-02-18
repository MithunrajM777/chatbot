function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");

    msgDiv.classList.add("message", sender);
    msgDiv.innerText = text;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Show suggestions ONLY after bot replies
    if (sender === "bot") {
        const suggestions = document.getElementById("suggestions");
        if (suggestions) {
            suggestions.style.display = "flex";
        }
    }
}

function sendMessage() {
    const input = document.getElementById("message");
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" }, // ✅ FIXED
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.reply, "bot");
    })
    .catch(() => {
        addMessage("⚠️ Server not responding. Please try again.", "bot");
    });
}

// Enter key support
document.getElementById("message").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

// Suggestion click handler (SINGLE correct version)
function sendSuggested(text) {
    const suggestions = document.getElementById("suggestions");
    if (suggestions) {
        suggestions.style.display = "none";
    }

    const input = document.getElementById("message");
    input.value = text;
    sendMessage();
}
