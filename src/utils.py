"""
Utility functions for data processing and analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data."""
    return pd.read_csv(filepath)


def calculate_expected_loss(portfolio: pd.DataFrame) -> Dict:
    """
    Calculate Expected Loss (EL) for portfolio.
    EL = PD * LGD * EAD
    """
    portfolio['pd'] = portfolio['is_default'].rolling(window=30, min_periods=1).mean()  # Proxy for PD
    portfolio['lgd'] = 0.45  # Loss Given Default (45% assumed)
    portfolio['ead'] = portfolio['loan_amount']  # Exposure at Default
    portfolio['expected_loss'] = portfolio['pd'] * portfolio['lgd'] * portfolio['ead']
    
    return {
        'total_expected_loss': portfolio['expected_loss'].sum(),
        'avg_expected_loss_per_loan': portfolio['expected_loss'].mean(),
    }


def calculate_risk_adjusted_return(portfolio: pd.DataFrame) -> Dict:
    """
    Calculate Risk-Adjusted Return on Capital (RAROC).
    """
    portfolio['interest_income'] = portfolio['loan_amount'] * (portfolio['interest_rate'] / 100)
    portfolio['expected_loss'] = portfolio['loan_amount'] * portfolio['is_default'].mean() * 0.45
    portfolio['net_income'] = portfolio['interest_income'] - portfolio['expected_loss']
    
    return {
        'total_interest_income': portfolio['interest_income'].sum(),
        'total_expected_loss': portfolio['expected_loss'].sum(),
        'net_portfolio_income': portfolio['net_income'].sum(),
        'raroc': (portfolio['net_income'].sum() / portfolio['loan_amount'].sum() * 100) if portfolio['loan_amount'].sum() > 0 else 0,
    }


def format_currency(value: float, prefix: str = '$') -> str:
    """Format value as currency."""
    return f"{prefix}{value:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage."""
    return f"{value * 100:.{decimals}f}%"


if __name__ == '__main__':
    print("Utility functions loaded successfully.")
