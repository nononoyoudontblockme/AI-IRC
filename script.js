const chatDiv = document.getElementById("chat");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("send");

async function sendMessage() {
    const msg = messageInput.value.trim();
    if (!msg) return;
    const response = await fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });
    const data = await response.json();
    updateChat(data);
    messageInput.value = "";
}

function updateChat(messages) {
    chatDiv.innerHTML = "";
    messages.forEach(m => {
        const div = document.createElement("div");
        div.textContent = `[${m.time}] <${m.user}> ${m.text}`;
        chatDiv.appendChild(div);
    });
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

// Load chat history on page load
async function loadHistory() {
    const response = await fetch("/history");
    const data = await response.json();
    updateChat(data);
}
loadHistory();
