import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import logging


class AIPricingEngine:
    def __init__(self):
        # Load pre-trained model (simplified for demo)
        try:
            with open('models/trained_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except:
            self.model = self._create_dummy_model()

        # Market data parameters
        self.benchmark_yields = {
            'UK5Y': 0.0425,  # Current UK 5-year yield
            'UK10Y': 0.0450,  # Current UK 10-year yield
        }

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _create_dummy_model(self):
        """Create a simple model for demo purposes"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.base import BaseEstimator

        class DummyModel(BaseEstimator):
            def predict(self, X):
                # Simple pricing logic: base_price * (1 + 0.1 * time_to_maturity)
                return np.array([100 * (1 + 0.1 * row[0]) for row in X])

        return DummyModel()

    def calculate_fair_price(self, isin, time_to_maturity, risk_score=0.5):
        """Calculate fair price using AI model"""
        # Prepare features for model
        features = np.array([[time_to_maturity, risk_score,
                              self.benchmark_yields['UK5Y'],
                              self.benchmark_yields['UK10Y']]])

        # Get base prediction
        base_price = self.model.predict(features)[0]

        # Add some random market movement for realism
        market_move = np.random.normal(0, 0.5)  # Small random adjustment
        fair_price = base_price + market_move

        self.logger.info(f"Calculated fair price for {isin}: {fair_price:.2f}")
        return fair_price

    def generate_quote(self, isin, side, quantity=1):
        """Generate bid/ask quotes with AI-powered pricing"""
        # Simulate different gilt characteristics based on ISIN
        if 'GB00B123' in isin:
            time_to_maturity = 5.0  # 5 years
            risk_score = 0.3
        elif 'GB00B456' in isin:
            time_to_maturity = 10.0  # 10 years
            risk_score = 0.5
        else:
            time_to_maturity = 7.0  # Default
            risk_score = 0.4

        # Calculate fair price
        fair_price = self.calculate_fair_price(isin, time_to_maturity, risk_score)

        # Apply spread based on liquidity risk
        spread = 0.02  # 2% spread
        if side == 'buy':
            quote_price = fair_price * (1 - spread / 2)
        else:  # sell
            quote_price = fair_price * (1 + spread / 2)

        # Explain the pricing (for demo purposes)
        explanation = {
            "fair_value": round(fair_price, 2),
            "components": {
                "base_value": 100.0,
                "time_premium": round((time_to_maturity * 0.1 * 100), 2),
                "yield_adjustment": round((self.benchmark_yields['UK5Y'] * 25), 2),
                "risk_adjustment": round((risk_score * 5), 2),
                "market_move": round((quote_price - fair_price), 2)
            },
            "benchmark_yields": self.benchmark_yields
        }

        return {
            "isin": isin,
            "side": side,
            "quantity": quantity,
            "price": round(quote_price, 2),
            "expiration": (datetime.now().timestamp() + 300) * 1000,  # 5 minutes
            "explanation": explanation
        }