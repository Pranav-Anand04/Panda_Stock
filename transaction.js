document.addEventListener("DOMContentLoaded", () => {
    const transactionTypeElement = document.getElementById('transaction-type');
    const numSharesInfo = document.getElementById('num-shares-info');
    const numberOfSharesInput = document.getElementById('number-of-shares');

    displayBuyingPower();

    // Function to toggle visibility and required attribute
    const toggleVisibility = () => {
        const transactionTypeValue = transactionTypeElement.value; 

        if (transactionTypeValue === "view") {
            numSharesInfo.style.display = "none"; 
            numberOfSharesInput.required = false; 
        } else {
            numSharesInfo.style.display = "block"; 
            numberOfSharesInput.required = true; 
        }
    };

    toggleVisibility();

    transactionTypeElement.addEventListener('change', toggleVisibility);
});


document.getElementById('transaction-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const transactionType = document.getElementById('transaction-type').value; 
    const stockName = document.getElementById('stock-name').value; 
    const numberOfShares = parseInt(document.getElementById('number-of-shares').value, 10);
    const userId = localStorage.getItem('user_id');

    // Handle the "View" case
    if (transactionType === 'view') {
        try {
            const response = await fetch(`http://127.0.0.1:5000/stocks/stock/${stockName}`);
            const stockData = await response.json();

            if (response.ok) {
                document.getElementById('stock-section').innerHTML = `
                    <h2>Stock: ${stockData.symbol}</h2>
                    <p>Company Name: ${stockData.company_name}</p>
                    <p>Current Price: $${stockData.price.toFixed(2)}</p>
                    <p>Beta (Volatility): ${stockData.beta}</p>
                    <p>Market Cap: $${(stockData.market_cap / 1e9).toFixed(2)} Billion</p>
                    <p>Dividend Yield: ${stockData.dividend_yield}</p>
                    <p>52-Week Range: ${stockData.range}</p>
                    <p>Sector: ${stockData.sector}</p>
                    <p>Industry: ${stockData.industry}</p>
                    <p>Website: <a href="${stockData.website}" target="_blank">${stockData.website}</a></p>
                    <img src="${stockData.image}" alt="${stockData.company_name}" style="max-width: 100%; height: auto;" />
                `;
            } else {
                alert(`Error: ${stockData.message}`);
            }
        } catch (error) {
            console.error("Error fetching stock details:", error);
            alert("An error occurred while fetching stock details.");
        }
    } else if (transactionType === 'buy') {
        try {
            const response = await fetch(`http://127.0.0.1:5000/stocks/transaction/buy`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify({
                    user_id: userId,
                    symbol: stockName,
                    quantity: numberOfShares
                }),
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message);
                updateBuyersPower();
            } else {
                alert('Error: ${result.message}');
            }
        } catch (error) {
            console.error("Error during transaction:", error);
            alert("An error occurred. Please try again.");
        }
        // This is sell stock
    } else {
        try {
            const response = await fetch('http://127.0.0.1:5000/stocks/transaction/sell', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    symbol: stockName,
                    quantity: numberOfShares
                }),
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message)
                updateBuyersPower();
            } else {
                alert(`Error: ${result.message}`)
            }
        } catch (error) {
            console.error("Error during sell transaction:", error);
            alert("An error occurred. Please try again.");
        }
    }
});

async function updateBuyersPower() {
    const userId = localStorage.getItem('user_id');
    try {
        const response = await fetch(`http://127.0.0.1:5000/user/buyers_power?user_id=${userId}`);
        const result = await response.json();
        if (response.ok) {
            document.querySelector('[for="buyer-power"]').textContent = `Buyer's power ($): ${result.buyers_power}`;
        } else {
            console.error("Failed to update buyer's power:", result.message);
        }
    } catch (error) {
        console.error("Error updating buyer's power:", error);
    }
}

async function displayBuyingPower() {
    const userId = localStorage.getItem('user_id'); 

    if (!userId) {
        alert("Please log in to access your account.");
        window.location.href = 'login.html';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/auth/buyers_power?user_id=${userId}`);
        if (!response.ok) {
            console.error(`Failed to fetch buyer's power: ${response.statusText}`);
            alert("Could not fetch buying power. Please try again.");
            return;
        }

        const result = await response.json(); // This might throw if the response isn't JSON
        document.querySelector('[for="buyer-power"]').textContent = `Buyer's power ($): ${result.buyers_power.toFixed(2)}`;
    } catch (error) {
        console.error("Error fetching buyer's power:", error);
        alert("An error occurred. Please try again.");
    }
}
