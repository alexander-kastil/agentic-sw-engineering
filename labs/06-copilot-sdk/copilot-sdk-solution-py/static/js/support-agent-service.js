async function askSupportAgent(question) {
    const response = await fetch("/api/supportagent/ask", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Support agent returned ${response.status}: ${errorText}`);
    }

    const result = await response.json();
    return result.answer || "I'm sorry, I didn't receive a response. Please try again.";
}
