document.addEventListener("DOMContentLoaded", async () => {
    const userId = localStorage.getItem('user_id');
    const firstname = localStorage.getItem('firstname');

    if (!userId) {
        alert("Please log in to view your portfolio.");
        window.location.href = 'login.html';
        return;
    } else {
        document.getElementById('welcomeMessage').textContent = `Hello, ${firstname}!`;
    }

    // Load portfolio initially
    await loadPortfolio(userId);

    // Set up real-time updates every 3 seconds
    setInterval(() => {
        loadPortfolio(userId);
    }, 3000); // Update every 3 seconds
});

// Function to load and update the portfolio
async function loadPortfolio(userId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/stocks/user/portfolio?user_id=${userId}`);
        const result = await response.json();

        if (response.ok) {
            populatePortfolioTable(result.portfolio);
        } else {
            console.error("Failed to fetch portfolio:", result.message);
            alert("Could not fetch portfolio. Please try again.");
        }
    } catch (error) {
        console.error("Error fetching portfolio:", error);
        alert("An error occurred while fetching portfolio data.");
    }
}

// Function to populate the portfolio table
function populatePortfolioTable(portfolio) {
    const tableBody = document.querySelector("table tbody");
    tableBody.innerHTML = "";

    portfolio.forEach((stock, index) => {
        if (stock.shares > 0) { 
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${stock.name} (${stock.symbol})</td>
                <td>${stock.shares}</td>
                <td>$${stock.current_price.toFixed(2)}</td>
                <td style="color: ${stock.profit_or_loss >= 0 ? 'green' : 'red'};">
                    $${stock.profit_or_loss.toFixed(2)}
                </td>
            `;

            tableBody.appendChild(row);
        }
    });
}
