const conversations = [];
let isLoading = false;

const messagesArea = document.getElementById("chat-messages");
const questionInput = document.getElementById("question");
const sendButton = document.getElementById("send");
const errorAlert = document.getElementById("error-message");

function renderMessages() {
    if (conversations.length === 0) {
        messagesArea.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="bi bi-chat-dots display-4 mb-2"></i>
                <p>Ask me about your orders! For example:</p>
                <ul class="list-unstyled">
                    <li><em>"What is the status of order #1001?"</em></li>
                    <li><em>"Show me all my orders"</em></li>
                    <li><em>"I want to return order #1005"</em></li>
                </ul>
            </div>`;
        return;
    }

    const entries = conversations.map(entry => `
        <div class="mb-3">
            <div class="d-flex align-items-start mb-1">
                <span class="badge bg-primary me-2">You</span>
                <span>${escapeHtml(entry.question)}</span>
            </div>
            ${entry.answer ? `
            <div class="d-flex align-items-start ms-2">
                <span class="badge bg-info me-2">Agent</span>
                <span style="white-space: pre-line;">${escapeHtml(entry.answer)}</span>
            </div>` : ""}
        </div>`).join("");

    const thinking = isLoading ? `
        <div class="d-flex align-items-start ms-2">
            <span class="badge bg-info me-2">Agent</span>
            <span class="text-muted"><em>Thinking...</em></span>
        </div>` : "";

    messagesArea.innerHTML = entries + thinking;
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

function updateControls() {
    questionInput.disabled = isLoading;
    sendButton.disabled = isLoading || questionInput.value.trim() === "";
}

function showError(message) {
    errorAlert.querySelector("span").textContent = message;
    errorAlert.classList.toggle("d-none", message === "");
}

async function submitQuestion() {
    const question = questionInput.value.trim();
    if (question === "" || isLoading) {
        return;
    }

    showError("");
    questionInput.value = "";

    const entry = { question, answer: "" };
    conversations.push(entry);

    try {
        isLoading = true;
        renderMessages();
        updateControls();

        entry.answer = await askSupportAgent(question);
    } catch (error) {
        showError("Sorry, something went wrong. Please try again or contact our support team.");
        console.error(`Agent error: ${error.message}`);
    } finally {
        isLoading = false;
        renderMessages();
        updateControls();
        questionInput.focus();
    }
}

questionInput.addEventListener("input", updateControls);
questionInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        submitQuestion();
    }
});
sendButton.addEventListener("click", submitQuestion);

renderNav();
renderMessages();
