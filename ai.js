async function askAI() {
    const query = document.getElementById('userQuery').value;
    const responseElement = document.getElementById('aiResponse');

    if (!query) {
        responseElement.innerHTML = "<p style='color: red;'>⚠️ Please enter a question!</p>";
        return;
    }

    responseElement.innerHTML = "<p>⏳ Thinking...</p>";

    try {
        const response = await fetch('http://127.0.0.1:5000/ai/ask_ai', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        console.log("AI API Response:", data);

        if (data.response) {
            responseElement.innerHTML = formatAIResponse(data.response);
        } else {
            responseElement.innerHTML = `<p style='color: red;'>❌ Error: ${data.error || "AI could not generate a response."}</p>`;
        }
    } catch (error) {
        console.error("AI Fetch Error:", error);
        responseElement.innerHTML = "<p style='color: red;'>❌ An error occurred. Please try again.</p>";
    }
}

// ✅ Function to Format AI Response with Better Readability
function formatAIResponse(text) {
    return `
        <h3>📌 AI's Explanation</h3>
        <p>${text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>")}</p>
    `;
}
