from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pricing_engine import AIPricingEngine
from canton_client import CantonClient
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="AI Liquidity Provider API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files - FIXED PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "../frontend")

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))


# Initialize components
pricing_engine = AIPricingEngine()
canton_client = CantonClient()


# Request models
class QuoteRequest(BaseModel):
    isin: str
    side: str  # 'buy' or 'sell'
    quantity: int = 1


class TradeRequest(BaseModel):
    isin: str
    side: str
    quantity: int
    price: float


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "AI Liquidity Provider"}


@app.post("/api/request-quote")
def request_quote(request: QuoteRequest):
    """Get an AI-powered quote for a gilt"""
    try:
        quote = pricing_engine.generate_quote(request.isin, request.side, request.quantity)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/execute-trade")
def execute_trade(request: TradeRequest):
    """Execute a trade with AI-provided price"""
    try:
        # Create DvP proposal on Canton
        proposal_data = {
            "isin": request.isin,
            "side": request.side,
            "quantity": request.quantity,
            "price": request.price,
            "expiration": None  # Will be set in the function
        }

        proposal_result = canton_client.create_dvp_proposal(proposal_data)

        # Execute the trade
        trade_result = canton_client.execute_trade(proposal_result['contractId'])

        return trade_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)