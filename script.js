const chatDiv = document.getElementById("chat");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("send");
const channelInput = document.getElementById("channel");
const setChannelBtn = document.getElementById("setChannel");

let currentChannel = "";
let chatLog = [];

// Predefined AI users with personalities
const aiUsers = [
    {name: "GhostHunter92", personality: "excited, conspiracy theorist"},
    {name: "FactCheckBot", personality: "sarcastic, pedantic"},
    {name: "WeirdAlex", personality: "dramatic, easily impressed"},
    {name: "TechieTom", personality: "tech geek, logical"},
    {name: "ChattyCathy", personality: "friendly, chatterbox"}
];

// Simple JS AI reply generator
function generateAIResponse(lastMessage) {
    const user = aiUsers[Math.floor(Math.random() * aiUsers.length)];
    const templates = [
        "I totally agree with that!",
        "That's interesting...",
        "Can you explain more?",
        "Haha, that's funny!",
        "Wow, I never thought of it that way.",
        "Hmm… let me think about that."
    ];
    const text = templates[Math.floor(Math.random() * templates.length)];
    return {time: new Date().toLocaleTimeString().slice(0,5), user: user.name, text};
}

// ---- Typing simulation ----
async function typeMessage(fullText) {
    return new Promise((resolve) => {
        const div = document.createElement("div");
        chatDiv.appendChild(div);
        let i = 0;

        function typeChar() {
            if (i < fullText.length) {
                div.textContent += fullText[i];
                i++;
                const delay = Math.random() * 50 + 20; // 20-70ms per char
                setTimeout(typeChar, delay);
            } else {
                resolve();
            }
        }

        typeChar();
    });
}

// ---- Display chat log ----
async function renderChat() {
    chatDiv.innerHTML = "";
    for (const msg of chatLog) {
        if (msg.user === "You") {
            const div = document.createElement("div");
            div.textContent = `[${msg.time}] <${msg.user}> ${msg.text}`;
            chatDiv.appendChild(div);
        } else {
            await typeMessage(`[${msg.time}] <${msg.user}> ${msg.text}`);
        }
    }
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

// ---- Handle user sending message ----
async function sendMessage() {
    const msg = messageInput.value.trim();
    if (!msg) return;
    const userMsg = {time: new Date().toLocaleTimeString().slice(0,5), user: "You", text: msg};
    chatLog.push(userMsg);
    messageInput.value = "";
    await renderChat();

    // AI response after a short delay
    setTimeout(async () => {
        const aiMsg = generateAIResponse(msg);
        chatLog.push(aiMsg);
        await renderChat();
    }, Math.random()*1500 + 500); // random 0.5–2 sec delay
}

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

// ---- Channel setup ----
setChannelBtn.addEventListener("click", () => {
    const channel = channelInput.value.trim() || "general";
    currentChannel = channel;
    const topicMsg = {time: new Date().toLocaleTimeString().slice(0,5), user: "System", text: `Channel ${currentChannel} created. Topic: Welcome to ${currentChannel}!`};
    chatLog.push(topicMsg);

    chatDiv.style.display = "block";
    messageInput.style.display = "inline-block";
    sendBtn.style.display = "inline-block";
    channelInput.style.display = "none";
    setChannelBtn.style.display = "none";

    renderChat();
});
