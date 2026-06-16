async function sendMessage() {

    let input = document.getElementById("user-input");
    let message = input.value.trim();

    if (message === "") return;

    let chatBox = document.getElementById("chat-box");

    // User message
    chatBox.innerHTML += `
        <div class="user">
            <b>You:</b> ${message}
        </div>
    `;

    input.value = "";

    // Loading message
    let loadingDiv = document.createElement("div");
    loadingDiv.className = "bot";
    loadingDiv.innerHTML = `<b>🤖 AI:</b> Thinking...`;

    chatBox.appendChild(loadingDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Remove loading message
        loadingDiv.remove();

        // Show bot response
        chatBox.innerHTML += `
            <div class="bot">
                <b>🤖 AI:</b> ${data.response}
            </div>
        `;

    } catch (error) {

        loadingDiv.remove();

        chatBox.innerHTML += `
            <div class="bot">
                <b>🤖 AI:</b> Error connecting to server.
            </div>
        `;

        console.error(error);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}
document.getElementById("user-input")
.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});