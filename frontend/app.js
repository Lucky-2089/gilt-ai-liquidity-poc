const API_BASE = '';

let currentQuote = null;

async function requestQuote() {
    const isin = document.getElementById('isin-select').value;
    const side = document.querySelector('input[name="trade-type"]:checked').value;
    const quantity = parseInt(document.getElementById('quantity-input').value);

    try {
        const response = await fetch('/api/request-quote', {  // Remove API_BASE
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ isin, side, quantity })
        });

function displayQuote(quote) {
    document.getElementById('quote-isin').textContent = quote.isin;
    document.getElementById('quote-side').textContent = quote.side;
    document.getElementById('quote-quantity').textContent = quote.quantity;
    document.getElementById('quote-price').textContent = quote.price.toFixed(2);
    document.getElementById('quote-total').textContent = (quote.quantity * quote.price).toFixed(2);

    const expiryDate = new Date(quote.expiration);
    document.getElementById('quote-expiry').textContent = expiryDate.toLocaleTimeString();

    // Display AI explanation
    const explanationDiv = document.getElementById('price-explanation');
    explanationDiv.innerHTML = `
        <p>The AI calculated a fair value of £${quote.explanation.fair_value.toFixed(2)} based on:</p>
        <ul>
            <li>Base value: £${quote.explanation.components.base_value.toFixed(2)}</li>
            <li>Time premium: £${quote.explanation.components.time_premium.toFixed(2)}</li>
            <li>Yield adjustment: £${quote.explanation.components.yield_adjustment.toFixed(2)}</li>
            <li>Risk adjustment: £${quote.explanation.components.risk_adjustment.toFixed(2)}</li>
            <li>Market movement: £${quote.explanation.components.market_move.toFixed(2)}</li>
        </ul>
        <p>Current benchmark yields: UK5Y=${(quote.explanation.benchmark_yields.UK5Y * 100).toFixed(2)}%,
        UK10Y=${(quote.explanation.benchmark_yields.UK10Y * 100).toFixed(2)}%</p>
    `;

    document.getElementById('quote-section').style.display = 'block';
    document.getElementById('result-section').style.display = 'none';
}

async function executeTrade() {
    if (!currentQuote) return;

    try {
        const response = await fetch(`${API_BASE}/api/execute-trade`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                isin: currentQuote.isin,
                side: currentQuote.side,
                quantity: currentQuote.quantity,
                price: currentQuote.price
            })
        });

        if (!response.ok) {
            throw new Error('Failed to execute trade');
        }

        const result = await response.json();
        displayTradeResult(result);

    } catch (error) {
        alert('Error executing trade: ' + error.message);
    }
}

function displayTradeResult(result) {
    const resultDiv = document.getElementById('trade-result');

    if (result.status === 'success') {
        resultDiv.innerHTML = `
            <div class="success-message">
                <h3>✅ Trade Executed Successfully!</h3>
                <p><strong>Trade ID:</strong> ${result.tradeId}</p>
                <p><strong>Status:</strong> ${result.details.status}</p>
                <p><strong>Settled on:</strong> ${new Date(result.details.timestamp).toLocaleString()}</p>
                <p><strong>Details:</strong> ${result.details.quantity} units of ${result.details.isin}
                at £${result.details.price} each</p>
                <p><strong>Message:</strong> ${result.message}</p>
            </div>
        `;
    } else {
        resultDiv.innerHTML = `
            <div class="error-message">
                <h3>❌ Trade Failed</h3>
                <p>${result.message}</p>
            </div>
        `;
    }

    document.getElementById('result-section').style.display = 'block';
}