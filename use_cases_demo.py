import sys
import os
import time

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from canton_client import CantonClient


def government_bond_trading_example():
    """Use case: Trading government gilts/bonds"""
    client = CantonClient()

    gilt_trade = {
        'side': 'buy',
        'isin': 'GB00B24FF097',  # UK 10-Year Gilt
        'quantity': 1000000,  # 1 million face value
        'price': 98.75,  # 98.75% of face value
        'expiration': '2024-12-31'
    }

    proposal = client.create_dvp_proposal(gilt_trade)
    print(f"🎯 Gilt trade proposed: {proposal['contractId']}")

    settlement = client.execute_trade(proposal['contractId'])
    print(f"✅ Gilt trade settled: {settlement['tradeId']}")
    return settlement


def corporate_bond_settlement():
    """Use case: Corporate bond trading"""
    client = CantonClient()

    trade = {
        'side': 'sell',
        'isin': 'XS1987882917',  # Corporate bond ISIN
        'quantity': 500000,  # $500,000 face value
        'price': 101.25,  # 101.25% of face value
        'expiration': '2024-06-30'
    }

    proposal = client.create_dvp_proposal(trade)
    settlement = client.execute_trade(proposal['contractId'])
    print(f"🏢 Corporate bond settled: {settlement['details']['quantity']} units")
    return settlement


def basket_trading_example():
    """Use case: Trading multiple securities as a basket"""
    client = CantonClient()

    basket_trades = [
        {'isin': 'US0378331005', 'side': 'buy', 'quantity': 100, 'price': 175.25, 'expiration': '2024-12-31'},
        {'isin': 'US0231351067', 'side': 'buy', 'quantity': 50, 'price': 340.50, 'expiration': '2024-12-31'},
    ]

    for i, trade in enumerate(basket_trades):
        proposal = client.create_dvp_proposal(trade)
        settlement = client.execute_trade(proposal['contractId'])
        print(f"📊 Basket trade {i + 1} settled: {settlement['details']['isin']}")


def run_all_use_cases():
    """Run all use case demonstrations"""
    print("🚀 Starting Canton DvP Use Cases Demo...\n")

    print("1. Government Bond Trading")
    government_bond_trading_example()

    print("\n2. Corporate Bond Settlement")
    corporate_bond_settlement()

    print("\n3. Basket Trading")
    basket_trading_example()

    print("\n✅ All use cases completed successfully!")


if __name__ == "__main__":
    run_all_use_cases()