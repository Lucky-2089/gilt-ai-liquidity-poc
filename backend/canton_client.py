import json
import time
import uuid
from datetime import datetime


class CantonClient:
    """Simulated Canton client for demo purposes"""

    def __init__(self):
        self.ledger = []
        self.parties = {
            "AI_Liquidity_Provider": "ai_provider::1234",
            "Customer": "customer::5678"
        }

    def create_dvp_proposal(self, proposal_data):
        """Simulate creating a DvP proposal on Canton"""
        # Simulate network latency
        time.sleep(0.5)

        # Create a simulated contract
        contract_id = str(uuid.uuid4())
        contract = {
            "contractId": contract_id,
            "templateId": "GiltTrading:DvPProposal",
            "argument": {
                "seller": self.parties["AI_Liquidity_Provider"] if proposal_data['side'] == 'sell' else self.parties[
                    "Customer"],
                "buyer": self.parties["Customer"] if proposal_data['side'] == 'sell' else self.parties[
                    "AI_Liquidity_Provider"],
                "isin": proposal_data['isin'],
                "quantity": proposal_data['quantity'],
                "price": proposal_data['price'],
                "expiration": proposal_data['expiration']
            },
            "signatories": [self.parties["AI_Liquidity_Provider"]],
            "observers": [self.parties["Customer"]]
        }

        # "Store" on simulated ledger
        self.ledger.append(contract)

        return {
            "status": "success",
            "contractId": contract_id,
            "message": "DvP proposal created successfully on Canton ledger"
        }

    def execute_trade(self, contract_id):
        """Simulate executing a trade on Canton"""
        time.sleep(1.0)  # Simulate network processing

        # Find the contract
        contract = next((c for c in self.ledger if c['contractId'] == contract_id), None)

        if not contract:
            return {"status": "error", "message": "Contract not found"}

        # Simulate atomic settlement
        trade_id = str(uuid.uuid4())
        trade_record = {
            "tradeId": trade_id,
            "timestamp": datetime.now().isoformat(),
            "isin": contract['argument']['isin'],
            "quantity": contract['argument']['quantity'],
            "price": contract['argument']['price'],
            "buyer": contract['argument']['buyer'],
            "seller": contract['argument']['seller'],
            "status": "settled"
        }

        return {
            "status": "success",
            "tradeId": trade_id,
            "message": "Trade settled atomically on Canton DLT",
            "details": trade_record
        }