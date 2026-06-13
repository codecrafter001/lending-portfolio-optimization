"""
Portfolio Analysis Module

Provides functions for:
- Portfolio-level metrics
- Risk exposure analysis
- Acquisition channel performance
- Product performance analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class PortfolioAnalyzer:
    """Analyze lending portfolio performance."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        
    def portfolio_summary(self) -> Dict:
        """Generate portfolio-level summary metrics."""
        summary = {
            'total_loans': len(self.data),
            'total_disbursed': self.data['loan_amount'].sum(),
            'avg_loan_size': self.data['loan_amount'].mean(),
            'avg_interest_rate': self.data['interest_rate'].mean(),
            'default_rate': self.data['is_default'].mean(),
            'portfolio_at_risk': (self.data['days_past_due'] > 30).sum() / len(self.data),
        }
        return summary
    
    def risk_by_segment(self, segment_col: str) -> pd.DataFrame:
        """Analyze risk metrics by segment."""
        risk_analysis = self.data.groupby(segment_col).agg({
            'loan_amount': ['count', 'sum', 'mean'],
            'is_default': 'mean',
            'days_past_due': ['mean', 'max'],
            'interest_rate': 'mean',
            'acquisition_cost': 'mean',
        }).round(4)
        
        return risk_analysis
    
    def channel_performance(self) -> pd.DataFrame:
        """Analyze acquisition channel performance."""
        channel_analysis = self.data.groupby('acquisition_channel').agg({
            'loan_id': 'count',
            'loan_amount': 'sum',
            'is_default': 'mean',
            'acquisition_cost': 'mean',
            'days_past_due': 'mean',
            'on_time_payments': 'mean',
        }).rename(columns={'loan_id': 'loan_count'})
        
        # Calculate LTV (Loan-to-Value proxy) and profitability
        channel_analysis['avg_loan_size'] = channel_analysis['loan_amount'] / channel_analysis['loan_count']
        channel_analysis['cac_to_alr'] = channel_analysis['acquisition_cost'] / channel_analysis['avg_loan_size']
        
        return channel_analysis
    
    def product_performance(self) -> pd.DataFrame:
        """Analyze product-level performance."""
        product_analysis = self.data.groupby('product_type').agg({
            'loan_id': 'count',
            'loan_amount': ['sum', 'mean'],
            'tenure_months': 'mean',
            'interest_rate': 'mean',
            'is_default': 'mean',
            'days_past_due': 'mean',
            'on_time_payments': 'mean',
        }).round(4)
        
        return product_analysis
    
    def risk_by_tenure(self) -> pd.DataFrame:
        """Analyze risk by loan tenure."""
        tenure_analysis = self.data.groupby('tenure_months').agg({
            'loan_id': 'count',
            'loan_amount': 'mean',
            'is_default': 'mean',
            'days_past_due': 'mean',
        }).round(4)
        
        return tenure_analysis
    
    def ltv_analysis(self) -> pd.DataFrame:
        """Calculate customer lifetime value proxy."""
        ltv_data = self.data.groupby('customer_id').agg({
            'loan_amount': 'sum',
            'interest_rate': 'mean',
            'is_default': 'sum',
            'on_time_payments': 'sum',
            'acquisition_cost': 'mean',
        }).reset_index()
        
        # Simple LTV = Total Interest Income - Acquisition Cost - Loss from Defaults
        ltv_data['total_interest_income'] = ltv_data['loan_amount'] * (ltv_data['interest_rate'] / 100) * 0.5
        ltv_data['ltv'] = ltv_data['total_interest_income'] - ltv_data['acquisition_cost']
        
        return ltv_data[['customer_id', 'loan_amount', 'ltv', 'is_default']]


if __name__ == '__main__':
    # Example usage
    data = pd.read_csv('data/raw/synthetic_lending_data.csv')
    analyzer = PortfolioAnalyzer(data)
    
    print("\n=== PORTFOLIO SUMMARY ===")
    print(analyzer.portfolio_summary())
    
    print("\n=== RISK BY GEOGRAPHY ===")
    print(analyzer.risk_by_segment('geography'))
    
    print("\n=== CHANNEL PERFORMANCE ===")
    print(analyzer.channel_performance())
    
    print("\n=== PRODUCT PERFORMANCE ===")
    print(analyzer.product_performance())
