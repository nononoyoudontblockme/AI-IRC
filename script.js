const chatDiv = document.getElementById("chat");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("send");
const channelInput = document.getElementById("channel");
const setChannelBtn = document.getElementById("setChannel");

let currentChannel = "";

setChannelBtn.addEventListener("click", async () => {
    const channel = channelInput.value.trim() || "general";
    const response = await fetch("/set_channel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ channel })
    });
    const data = await response.json();
    currentChannel = data.channel;
    // Show chat UI
    chatDiv.style.display = "block";
    messageInput.style.display = "inline-block";
    sendBtn.style.display = "inline-block";
    channelInput.style.display = "none";
    setChannelBtn.style.display = "none";
    loadHistory();
});

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
