// Global State
let currentTicker = 'TSLA';
let charts = {};

// Metric Definitions for Tooltips
// Metric Definitions for Tooltips
const METRIC_DEFINITIONS = {
    "Current Ratio": {
        definition: "Measures a company's ability to pay short-term obligations or those due within one year.",
        formula: "Current Assets / Current Liabilities",
        interpretation: "A ratio above 1.0 indicates the company can cover its short-term debt. Higher is generally better, but too high might mean inefficient use of assets."
    },
    "Quick Ratio": {
        definition: "An indicator of a company's short-term liquidity position, measuring ability to meet obligations with most liquid assets.",
        formula: "(Current Assets - Inventory) / Current Liabilities",
        interpretation: "Also known as the 'Acid Test'. It's a more conservative measure than Current Ratio because it excludes inventory."
    },
    "Debt-to-Equity": {
        definition: "A ratio used to evaluate a company's financial leverage.",
        formula: "Total Liabilities / Total Shareholder Equity",
        interpretation: "High ratios indicate the company is aggressively financing growth with debt, which can be risky if earnings are volatile."
    },
    "Interest Coverage": {
        definition: "Measures how easily a company can pay interest on its outstanding debt.",
        formula: "EBIT / Interest Expense",
        interpretation: "A ratio below 1.5 is a warning sign. Higher ratios indicate the company is more capable of meeting interest obligations."
    },
    "Gross Margin": {
        definition: "The difference between revenue and cost of goods sold (COGS), divided by revenue.",
        formula: "(Revenue - COGS) / Revenue",
        interpretation: "Indicates how efficiently a company uses labor and supplies in production. Higher margins mean more capital to pay for other costs."
    },
    "Net Margin": {
        definition: "The percentage of revenue remaining after all operating expenses, interest, taxes and preferred stock dividends have been deducted.",
        formula: "Net Income / Revenue",
        interpretation: "The 'bottom line'. It shows how much of each dollar collected by the company translates into profit."
    },
    "Inventory Turnover": {
        definition: "A ratio showing how many times a company has sold and replaced inventory during a given period.",
        formula: "Cost of Goods Sold / Average Inventory",
        interpretation: "Higher turnover generally means strong sales or ineffective buying. Low turnover implies poor sales and excess inventory."
    },
    "ROIC": {
        definition: "Return on Invested Capital. Assesses a company's efficiency at allocating capital to profitable investments.",
        formula: "NOPAT / Invested Capital",
        interpretation: "If ROIC > WACC (Cost of Capital), the company is creating value. If ROIC < WACC, it is destroying value."
    }
};

// Realistic Starting Prices
const REAL_PRICES = {
    "TSLA": 427.06,
    "AAPL": 276.25,
    "NVDA": 177.41,
    "MSFT": 490.48,
    "GOOG": 317.99,
    "AMZN": 231.42,
    "META": 641.29,
    "NFLX": 890.00 // Estimated based on recent trends
};

// Data Factory: Generate Mock Data for New Tickers
function generateMockData(ticker) {
    const seed = ticker.charCodeAt(0) + ticker.charCodeAt(1) || 0; // Simple seed
    const random = () => Math.random(); // In a real app, use a seeded random

    // 1. Try to get Real-Time Data from Python Script
    let liveData = null;
    if (typeof LIVE_MARKET_DATA !== 'undefined' && LIVE_MARKET_DATA[ticker]) {
        liveData = LIVE_MARKET_DATA[ticker];
    }

    // Use real price if available, else fallback to hardcoded or random
    let basePrice = 100 + (random() * 900);
    if (liveData && liveData.price > 0) {
        basePrice = liveData.price;
    } else if (REAL_PRICES[ticker]) {
        basePrice = REAL_PRICES[ticker];
    }

    const price = basePrice;

    // Use real ratios if available
    const marketCap = (liveData && liveData.ratios.marketCap) ? liveData.ratios.marketCap : (100 + random() * 2000) * 1e9;
    const trailingPE = (liveData && liveData.ratios.trailingPE) ? liveData.ratios.trailingPE : (10 + random() * 50);
    const forwardPE = (liveData && liveData.ratios.forwardPE) ? liveData.ratios.forwardPE : (10 + random() * 40);
    const beta = (liveData && liveData.ratios.beta) ? liveData.ratios.beta : (0.5 + random() * 1.5);

    return {
        financials: Array.from({ length: 4 }, (_, i) => ({
            year: 2024 - i,
            revenue: (50 + random() * 100) * 1e9,
            netIncome: (5 + random() * 20) * 1e9
        })),
        ratios: {
            marketCap: marketCap,
            trailingPE: trailingPE,
            forwardPE: forwardPE,
            beta: beta
        },
        technicals: {
            currentPrice: price,
            sma50: price * (0.9 + random() * 0.2),
            sma200: price * (0.8 + random() * 0.4),
            rsi: 30 + random() * 40,
            macd: (random() * 5) - 2.5,
            bbUpper: price * 1.1,
            bbLower: price * 0.9,
            summary: random() > 0.5 ? "Bullish Trend" : "Consolidation",
            key_levels: {
                support: [Math.floor(price * 0.9), Math.floor(price * 0.85)],
                resistance: [Math.floor(price * 1.1), Math.floor(price * 1.15)]
            },
            indicators: [
                { name: "RSI (14)", value: (30 + random() * 40).toFixed(1), signal: "Neutral" },
                { name: "MACD", value: "0.5", signal: "Buy" }
            ]
        },
        priceHistory: Array.from({ length: 30 }, (_, i) => ({
            date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split('T')[0],
            close: price * (1 + (Math.random() * 0.1 - 0.05))
        })),
        qualitative: {
            moat: { score: 70 + Math.floor(random() * 25), details: ["Strong Brand", "Network Effects"] },
            management: { score: 70 + Math.floor(random() * 25), details: "Experienced leadership team." },
            sentiment: { score: 50 + Math.floor(random() * 40), label: "Neutral", details: "Market is waiting for next earnings." },
            deep_research: {
                ratios: {
                    liquidity: [
                        { name: "Current Ratio", value: (1 + random()).toFixed(1), industry: "1.2", status: "Healthy", insight: "Sufficient liquidity." },
                        { name: "Quick Ratio", value: (0.8 + random()).toFixed(1), industry: "0.9", status: "Healthy", insight: "Good acid-test results." }
                    ],
                    solvency: [
                        { name: "Debt-to-Equity", value: (random()).toFixed(2), industry: "0.6", status: "Good", insight: "Manageable leverage." },
                        { name: "Interest Coverage", value: (5 + random() * 10).toFixed(1), industry: "8.0", status: "Excellent", insight: "No default risk." }
                    ],
                    profitability: [
                        { name: "Gross Margin", value: (20 + random() * 40).toFixed(1) + "%", industry: "30%", status: "Good", insight: "Healthy margins." },
                        { name: "Net Margin", value: (10 + random() * 20).toFixed(1) + "%", industry: "15%", status: "Good", insight: "Profitable operations." }
                    ],
                    efficiency: [
                        { name: "Inventory Turnover", value: (4 + random() * 4).toFixed(1), industry: "5.0", status: "Neutral", insight: "Standard efficiency." },
                        { name: "ROIC", value: (10 + random() * 15).toFixed(1) + "%", industry: "12%", status: "Good", insight: "Value creating." }
                    ]
                },
                qualitative: {
                    swot: {
                        strengths: ["Market Leader", "Innovation"],
                        weaknesses: ["High Costs", "Competition"],
                        opportunities: ["Global Expansion", "New Products"],
                        threats: ["Regulation", "Economic Downturn"]
                    },
                    pestel: { political: "Stable", economic: "Growing", social: "Positive", technological: "Advanced", environmental: "Compliant", legal: "Clear" },
                    porters: { supplier_power: "Low", buyer_power: "Medium", rivalry: "High", threat_of_substitutes: "Low", threat_of_new_entrants: "Low" },
                    management_deep_dive: { bio: "CEO has 20+ years exp.", track_record: "Solid growth.", governance: "Independent board." }
                },
                technicals: {
                    summary: "Neutral",
                    key_levels: { support: [Math.floor(price * 0.9)], resistance: [Math.floor(price * 1.1)] },
                    indicators: [{ name: "RSI", value: "50", signal: "Neutral" }]
                },
                valuation: {
                    dcf: { intrinsic_value: price * 1.1, current_price: price, upside: "+10%", assumptions: { wacc: "10%", terminal_growth: "3%", revenue_cagr_5yr: "12%" } },
                    multiples: { pe_fwd: "20x", industry_pe: "18x", peg: "1.2", verdict: "Fairly Valued" }
                },
                news: [
                    { headline: `${ticker} Announces New Partnership`, impact: "Positive", connection: "Revenue growth potential.", date: "Today" },
                    { headline: "Sector Volatility Increases", impact: "Negative", connection: "Short-term price pressure.", date: "Yesterday" }
                ]
            }
        }
    };
}

// Handle Search
async function handleSearch(event) {
    if (event.key === 'Enter') {
        const ticker = event.target.value.toUpperCase();
        if (!ticker) return;

        // Show Loading Overlay
        const overlay = document.getElementById('loading-overlay');
        const timerEl = document.getElementById('loading-timer');
        overlay.classList.remove('hidden');

        let timeLeft = 3;
        timerEl.innerText = timeLeft;

        const timer = setInterval(() => {
            timeLeft--;
            timerEl.innerText = timeLeft;
            if (timeLeft <= 0) clearInterval(timer);
        }, 1000);

        try {
            // Attempt to fetch from local server
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000); // 8s timeout

            const response = await fetch(`http://localhost:5000/api/research/${ticker}`, {
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (response.ok) {
                const data = await response.json();
                marketData[ticker] = data;
                console.log(`Loaded real-time data for ${ticker}`);
            } else {
                throw new Error("Server returned error");
            }
        } catch (error) {
            console.warn("Local server unavailable or failed, falling back to mock data.", error);
            if (!marketData[ticker]) {
                marketData[ticker] = generateMockData(ticker);
            }
        }

        // Add to Sidebar if new
        const navLinks = document.getElementById('company-list');
        const existingBtn = Array.from(navLinks.children).find(btn => btn.querySelector('.ticker')?.innerText === ticker);

        if (!existingBtn) {
            const btn = document.createElement('button');
            btn.className = 'nav-item';
            btn.onclick = () => switchCompany(ticker);
            btn.innerHTML = `
                <span class="ticker">${ticker}</span>
                <span class="name">${marketData[ticker].companyName || ticker + ' Corp'}</span>
            `;
            navLinks.appendChild(btn);
        }

        // Hide Overlay and Switch
        overlay.classList.add('hidden');
        switchCompany(ticker);
        event.target.value = ''; // Clear input
    }
}

// Explanation Modal Logic
function showExplanation(metricName) {
    const modal = document.getElementById('explanation-modal');
    const title = document.getElementById('modal-title');
    const desc = document.getElementById('modal-description');

    const metric = METRIC_DEFINITIONS[metricName];
    title.innerText = metricName;

    if (metric) {
        desc.innerHTML = `
            <div class="explanation-section">
                <h4>Definition</h4>
                <p>${metric.definition}</p>
            </div>
            <div class="explanation-section">
                <h4>Formula</h4>
                <code class="formula-block">${metric.formula}</code>
            </div>
            <div class="explanation-section">
                <h4>Interpretation</h4>
                <p>${metric.interpretation}</p>
            </div>
        `;
    } else {
        desc.innerText = "No detailed explanation available for this metric.";
    }

    modal.classList.remove('hidden');
}

function closeExplanation() {
    document.getElementById('explanation-modal').classList.add('hidden');
}

// Close modal on outside click
window.onclick = function (event) {
    const modal = document.getElementById('explanation-modal');
    if (event.target == modal) {
        modal.classList.add('hidden');
    }
}

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadCompany(currentTicker);

    // Enhanced Live Updates Simulation
    setInterval(() => {
        // 1. Price Update
        const priceEl = document.getElementById('company-price');
        const changeEl = document.getElementById('price-change');

        if (priceEl && changeEl) {
            const current = parseFloat(priceEl.innerText.replace('$', ''));
            const jitter = (Math.random() * 0.4) - 0.2; // +/- $0.20
            const newPrice = current + jitter;

            // Calculate Change (Assuming open price is roughly 1% lower for demo)
            // In a real app, we'd store the open price. Here we approximate.
            const openPrice = newPrice / 1.012;
            const changeAmt = newPrice - openPrice;
            const changePct = (changeAmt / openPrice) * 100;

            priceEl.innerText = `$${newPrice.toFixed(2)}`;
            changeEl.innerText = `${changeAmt >= 0 ? '+' : ''}${changeAmt.toFixed(2)} (${changePct.toFixed(2)}%)`;

            // Color Logic
            const isPositive = changeAmt >= 0;
            changeEl.className = `change ${isPositive ? 'positive' : 'negative'}`;

            // Flash effect
            priceEl.style.color = jitter > 0 ? 'var(--success-color)' : 'var(--danger-color)';
            setTimeout(() => priceEl.style.color = '#fff', 500);
        }

        // 2. Randomly update a metric occasionally to feel "alive"
        if (Math.random() > 0.7) {
            // Simulate P/E ratio shifting slightly with price
            const peEl = document.querySelector('.metric-card:nth-child(2) .metric-value');
            if (peEl) {
                const currentPE = parseFloat(peEl.innerText);
                peEl.innerText = (currentPE + (Math.random() * 0.1 - 0.05)).toFixed(2);
            }
        }
    }, 2000); // Faster updates
});

// Switch Company
function switchCompany(ticker) {
    currentTicker = ticker;

    // Update Sidebar Active State
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.classList.remove('active');
        if (btn.querySelector('.ticker').innerText === ticker) {
            btn.classList.add('active');
        }
    });

    loadCompany(ticker);
}

// Switch Tab
function switchTab(tabId) {
    // Update Buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    // Update Content
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}

// Switch Research Tab
function switchResearchTab(tabId) {
    document.querySelectorAll('.sub-nav-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    document.querySelectorAll('.research-sub-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}

// Load Company Data
// Load Company Data
function loadCompany(ticker) {
    try {
        const data = marketData[ticker];
        if (!data) {
            console.error(`No data found for ${ticker}`);
            // Try to generate mock data if missing
            if (typeof generateMockData === 'function') {
                console.log(`Generating mock data for ${ticker}`);
                marketData[ticker] = generateMockData(ticker);
                loadCompany(ticker); // Retry
                return;
            }
            return;
        }

        // 1. Update Header
        const nameEl = document.getElementById('company-name');
        if (nameEl) {
            nameEl.innerText = data.companyName || `${ticker} Inc.`;
        }
        const tickerEl = document.getElementById('company-ticker');
        if (tickerEl) tickerEl.innerText = ticker;

        const priceEl = document.getElementById('company-price');
        const currentPrice = data.technicals.currentPrice;
        if (priceEl) priceEl.innerText = `$${currentPrice.toFixed(2)}`;

        // Calculate daily change
        let change = 0;
        let changePercent = 0;
        if (data.priceHistory && data.priceHistory.length > 1) {
            const lastDay = data.priceHistory[data.priceHistory.length - 1];
            const prevDay = data.priceHistory[data.priceHistory.length - 2];
            change = currentPrice - prevDay.close;
            changePercent = (change / prevDay.close) * 100;
        }

        const changeEl = document.getElementById('company-change');
        if (changeEl) {
            changeEl.innerText = `${change >= 0 ? '+' : ''}${change.toFixed(2)} (${changePercent.toFixed(2)}%)`;
            changeEl.className = `change ${change >= 0 ? 'positive' : 'negative'}`;
        }

        // 2. Update Overview
        if (data.qualitative && data.qualitative.sentiment) {
            updateSentiment(data.qualitative.sentiment);
        }
        if (data.ratios) {
            updateRatios(data.ratios);
        }
        if (data.priceHistory) {
            renderPriceChart(data.priceHistory);
        }

        // 3. Update Financials
        if (data.financials) {
            renderFinancialChart(data.financials);
        }
        if (data.qualitative && data.qualitative.financialAnalysis) {
            const analysisEl = document.getElementById('financial-analysis');
            if (analysisEl) {
                analysisEl.innerHTML = data.qualitative.financialAnalysis.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            }
        }

        // 4. Update Technicals
        if (data.technicals) {
            updateTechnicalsGrid(data.technicals);
        }
        if (data.priceHistory) {
            renderTechnicalChart(data.priceHistory);
        }

        // 5. Update Moat
        if (data.qualitative && data.qualitative.moat && data.qualitative.management) {
            updateMoat(data.qualitative.moat, data.qualitative.management);
        }

        // 6. Update Deep Research (if container exists)
        if (data.qualitative && data.qualitative.deep_research && typeof renderDeepResearch === 'function') {
            renderDeepResearch(data.qualitative.deep_research);
        }

    } catch (e) {
        console.error("Error loading company data:", e);
    }
}

// --- Helpers ---

function updateSentiment(sentiment) {
    const fill = document.getElementById('sentiment-fill');
    const label = document.getElementById('sentiment-label');
    const text = document.getElementById('sentiment-text');

    fill.style.width = `${sentiment.score}% `;

    // Color based on score
    if (sentiment.score >= 75) fill.style.backgroundColor = 'var(--success-color)';
    else if (sentiment.score >= 45) fill.style.backgroundColor = 'var(--warning-color)';
    else fill.style.backgroundColor = 'var(--danger-color)';

    label.innerText = sentiment.label;
    text.innerText = sentiment.details;
}

function updateRatios(ratios) {
    const grid = document.getElementById('ratios-grid');
    grid.innerHTML = `
        <div class="stat-item">
            <span class="stat-label">Market Cap</span>
            <span class="stat-value">$${(ratios.marketCap / 1e9).toFixed(1)}B</span>
        </div >
        <div class="stat-item">
            <span class="stat-label">P/E (Trailing)</span>
            <span class="stat-value">${ratios.trailingPE?.toFixed(1) || '-'}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">P/E (Forward)</span>
            <span class="stat-value">${ratios.forwardPE?.toFixed(1) || '-'}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Beta</span>
            <span class="stat-value">${ratios.beta?.toFixed(2) || '-'}</span>
        </div>
    `;
}

function updateTechnicalsGrid(tech) {
    const grid = document.getElementById('technicals-grid');
    grid.innerHTML = `
        <div class="stat-item">
            <span class="stat-label">RSI (14)</span>
            <span class="stat-value" style="color: ${tech.rsi > 70 ? 'var(--danger-color)' : tech.rsi < 30 ? 'var(--success-color)' : 'white'}">${tech.rsi.toFixed(1)}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">MACD</span>
            <span class="stat-value">${tech.macd.toFixed(2)}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">SMA 50</span>
            <span class="stat-value">$${tech.sma50.toFixed(2)}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">SMA 200</span>
            <span class="stat-value">$${tech.sma200.toFixed(2)}</span>
        </div>
    `;
}

function updateMoat(moat, management) {
    document.getElementById('moat-score').innerText = moat.score;
    document.getElementById('management-score').innerText = management.score;
    document.getElementById('management-details').innerText = management.details;

    const list = document.getElementById('moat-details');
    list.innerHTML = moat.details.map(detail => {
        // Parse bold markdown
        const html = detail.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        return `<li>${html}</li>`;
    }).join('');
}

function renderDeepResearch(data) {
    renderRatios(data.ratios);
    renderQualitativeDeep(data.qualitative);
    renderTechnicalsDeep(data.technicals);
    renderValuation(data.valuation);
    renderNews(data.news);
}

function renderRatios(ratios) {
    const container = document.getElementById('ratios-container');
    let html = '';

    for (const [category, items] of Object.entries(ratios)) {
        html += `
        <div class="card">
                <h3>${category.charAt(0).toUpperCase() + category.slice(1)} Analysis</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                            <th>Industry</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${items.map(item => `
                            <tr>
                                <td>
                                    <div class="metric-with-tooltip">
                                        ${item.name}
                                        <i class="fa-solid fa-circle-info info-icon" onclick="showExplanation('${item.name}')"></i>
                                    </div>
                                </td>
                                <td class="highlight">${item.value}</td>
                                <td>${item.industry}</td>
                                <td><span class="badge ${item.status.toLowerCase()}">${item.status}</span></td>
                            </tr>
                            <tr class="insight-row">
                                <td colspan="4"><i class="fa-solid fa-lightbulb"></i> ${item.insight}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }
    container.innerHTML = html;
}

function renderQualitativeDeep(qualitative) {
    const container = document.getElementById('qualitative-container');

    // SWOT
    const swot = qualitative.swot;
    const swotHtml = `
        <div class="card full-width">
            <h3>SWOT Analysis</h3>
            <div class="swot-grid">
                <div class="swot-box strength"><h4>Strengths</h4><ul>${swot.strengths.map(s => `<li>${s}</li>`).join('')}</ul></div>
                <div class="swot-box weakness"><h4>Weaknesses</h4><ul>${swot.weaknesses.map(s => `<li>${s}</li>`).join('')}</ul></div>
                <div class="swot-box opportunity"><h4>Opportunities</h4><ul>${swot.opportunities.map(s => `<li>${s}</li>`).join('')}</ul></div>
                <div class="swot-box threat"><h4>Threats</h4><ul>${swot.threats.map(s => `<li>${s}</li>`).join('')}</ul></div>
            </div>
        </div>
        `;

    // PESTEL
    const pestel = qualitative.pestel;
    const pestelHtml = `
        <div class="card">
            <h3>PESTEL Analysis</h3>
            <ul class="details-list">
                ${Object.entries(pestel).map(([k, v]) => `<li><strong>${k.charAt(0).toUpperCase() + k.slice(1)}:</strong> ${v}</li>`).join('')}
            </ul>
        </div >
        `;

    // Porters
    const porters = qualitative.porters;
    const portersHtml = `
        < div class="card" >
            <h3>Porter's 5 Forces</h3>
            <ul class="details-list">
                ${Object.entries(porters).map(([k, v]) => `<li><strong>${k.replace(/_/g, ' ').toUpperCase()}:</strong> ${v}</li>`).join('')}
            </ul>
        </div >
        `;

    container.innerHTML = swotHtml + pestelHtml + portersHtml;
}

function renderTechnicalsDeep(technicals) {
    const container = document.getElementById('technicals-container');
    container.innerHTML = `
        < div class="card" >
            <h3>Summary: ${technicals.summary}</h3>
            <div class="levels-grid">
                <div>
                    <h4>Support Levels</h4>
                    <div class="level-tags">
                        ${technicals.key_levels.support.map(l => `<span class="level-tag support">$${l}</span>`).join('')}
                    </div>
                </div>
                <div>
                    <h4>Resistance Levels</h4>
                    <div class="level-tags">
                        ${technicals.key_levels.resistance.map(l => `<span class="level-tag resistance">$${l}</span>`).join('')}
                    </div>
                </div>
            </div>
        </div >
        <div class="card">
            <h3>Key Indicators</h3>
            <table class="data-table">
                <thead><tr><th>Indicator</th><th>Value</th><th>Signal</th></tr></thead>
                <tbody>
                    ${technicals.indicators.map(i => `
                        <tr>
                            <td>${i.name}</td>
                            <td>${i.value}</td>
                            <td><span class="badge ${i.signal.includes('Buy') || i.signal.includes('Bullish') ? 'success' : i.signal.includes('Sell') || i.signal.includes('Bearish') ? 'danger' : 'warning'}">${i.signal}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

function renderValuation(valuation) {
    const container = document.getElementById('valuation-container');
    const dcf = valuation.dcf;

    container.innerHTML = `
        < div class="card full-width" >
            <h3>DCF Model Output</h3>
            <div class="valuation-summary">
                <div class="val-metric">
                    <span class="label">Intrinsic Value</span>
                    <span class="value">$${dcf.intrinsic_value.toFixed(2)}</span>
                </div>
                <div class="val-metric">
                    <span class="label">Current Price</span>
                    <span class="value">$${dcf.current_price.toFixed(2)}</span>
                </div>
                <div class="val-metric">
                    <span class="label">Upside/Downside</span>
                    <span class="value ${parseFloat(dcf.upside) >= 0 ? 'positive' : 'negative'}">${dcf.upside}</span>
                </div>
            </div>
            <div class="assumptions-box">
                <h4>Key Assumptions</h4>
                <p>WACC: ${dcf.assumptions.wacc} | Terminal Growth: ${dcf.assumptions.terminal_growth} | 5yr Revenue CAGR: ${dcf.assumptions.revenue_cagr_5yr}</p>
            </div>
        </div >
        <div class="card">
            <h3>Relative Valuation</h3>
            <ul class="details-list">
                <li><strong>Forward P/E:</strong> ${valuation.multiples.pe_fwd} (Industry: ${valuation.multiples.industry_pe})</li>
                <li><strong>PEG Ratio:</strong> ${valuation.multiples.peg}</li>
                <li><strong>Verdict:</strong> ${valuation.multiples.verdict}</li>
            </ul>
        </div>
    `;
}

function renderNews(news) {
    const container = document.getElementById('news-container');
    container.innerHTML = news.map(item => `
        < div class="card news-card full-width" >
            <div class="news-header">
                <h4>${item.headline}</h4>
                <span class="news-date">${item.date}</span>
            </div>
            <div class="news-impact">
                <span class="badge ${item.impact.toLowerCase() === 'positive' ? 'success' : 'danger'}">${item.impact} Impact</span>
            </div>
            <p class="news-connection"><i class="fa-solid fa-link"></i> <strong>Connection:</strong> ${item.connection}</p>
        </div >
        `).join('');
}

// --- Charts ---

function renderPriceChart(history) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    if (charts.price) charts.price.destroy();

    const labels = history.map(h => h.date);
    const data = history.map(h => h.close);

    // Gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    charts.price = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Price',
                data: data,
                borderColor: '#3b82f6',
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: { display: false }
            },
            interaction: {
                intersect: false,
                mode: 'index',
            }
        }
    });
}

function renderFinancialChart(financials) {
    const ctx = document.getElementById('financialChart').getContext('2d');

    if (charts.financials) charts.financials.destroy();

    // Reverse to show oldest to newest
    const sorted = [...financials].reverse();
    const labels = sorted.map(f => f.year);
    const revenue = sorted.map(f => f.revenue / 1e9);
    const netIncome = sorted.map(f => f.netIncome / 1e9);

    charts.financials = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Revenue ($B)',
                    data: revenue,
                    backgroundColor: '#3b82f6',
                    borderRadius: 4
                },
                {
                    label: 'Net Income ($B)',
                    data: netIncome,
                    backgroundColor: '#10b981',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#fff' } }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { color: '#a1a1aa' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#a1a1aa' }
                }
            }
        }
    });
}

function renderTechnicalChart(history) {
    const ctx = document.getElementById('technicalChart').getContext('2d');

    if (charts.technicals) charts.technicals.destroy();

    // Calculate RSI manually for chart if needed, but we'll just plot Close vs SMA for now as a proxy for "Technical View"
    // Or we can just plot the Close price again with Bollinger Bands if we had them in history.
    // Since we only have current indicators, let's plot Price vs a simple Moving Average we calculate on the fly for the chart

    const labels = history.map(h => h.date);
    const close = history.map(h => h.close);

    // Simple SMA 20 calculation for chart
    const sma20 = close.map((val, idx, arr) => {
        if (idx < 19) return null;
        const window = arr.slice(idx - 19, idx + 1);
        return window.reduce((a, b) => a + b, 0) / 20;
    });

    charts.technicals = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Price',
                    data: close,
                    borderColor: '#ffffff',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'SMA 20',
                    data: sma20,
                    borderColor: '#f59e0b',
                    borderWidth: 1,
                    pointRadius: 0,
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#fff' } } },
            scales: {
                y: {
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { color: '#a1a1aa' }
                },
                x: { display: false }
            }
        }
    });
}
