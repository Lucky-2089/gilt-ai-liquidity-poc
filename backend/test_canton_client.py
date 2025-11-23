import pytest
import time
import sys
import os

# Import the CantonClient from the same directory
from canton_client import CantonClient


def test_canton_client_initialization():
    """Test client initialization"""
    client = CantonClient()
    assert client.ledger == []
    assert "AI_Liquidity_Provider" in client.parties


def test_create_dvp_proposal_sell():
    """Test creating a sell DvP proposal"""
    client = CantonClient()
    proposal_data = {
        'side': 'sell',
        'isin': 'US0378331005',
        'quantity': 100,
        'price': 150.50,
        'expiration': '2024-12-31'
    }

    response = client.create_dvp_proposal(proposal_data)
    assert response['status'] == 'success'
    assert len(client.ledger) == 1


def test_execute_trade_success():
    """Test successful trade execution"""
    client = CantonClient()

    proposal_data = {
        'side': 'sell',
        'isin': 'US0378331005',
        'quantity': 100,
        'price': 150.50,
        'expiration': '2024-12-31'
    }
    create_response = client.create_dvp_proposal(proposal_data)

    execute_response = client.execute_trade(create_response['contractId'])
    assert execute_response['status'] == 'success'
    assert execute_response['details']['status'] == 'settled'


def test_execute_trade_contract_not_found():
    """Test trade execution with non-existent contract"""
    client = CantonClient()
    response = client.execute_trade('non-existent-id')
    assert response['status'] == 'error'


def test_end_to_end_trade_flow():
    """Test complete trade flow from proposal to settlement"""
    client = CantonClient()

    proposal_data = {
        'side': 'sell',
        'isin': 'US0378331005',
        'quantity': 150,
        'price': 175.25,
        'expiration': '2024-12-31'
    }

    proposal_response = client.create_dvp_proposal(proposal_data)
    trade_response = client.execute_trade(proposal_response['contractId'])

    assert proposal_response['status'] == 'success'
    assert trade_response['status'] == 'success'
    assert trade_response['details']['quantity'] == 150


if __name__ == "__main__":
    # Run tests when file is executed directly
    pytest.main([__file__, "-v"])