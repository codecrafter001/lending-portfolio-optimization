"""
Synthetic Lending Data Generator

Generates realistic digital lending portfolio data with:
- Customer profiles (geography, income, employment)
- Loan products (personal, BNPL, SME working capital)
- Repayment behavior and delinquency patterns
- Behavioral signals (cash flow, spending volatility)
- Acquisition channel data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

class SyntheticLendingDataGenerator:
    """Generate synthetic lending portfolio data."""
    
    def __init__(self, n_customers=10000):
        self.n_customers = n_customers
        self.start_date = datetime(2022, 1, 1)
        self.end_date = datetime(2024, 6, 30)
        
    def generate_customer_profiles(self):
        """Generate customer profile data."""
        geographies = ['Urban_Metro', 'Urban_Tier2', 'Semi_Urban', 'Rural']
        employment_types = ['Salaried', 'Self_Employed', 'Gig_Worker', 'Unemployed']
        channels = ['App', 'Web', 'Partner', 'Branch', 'SMS_Campaign']
        
        customers = pd.DataFrame({
            'customer_id': [f'CUST_{i:06d}' for i in range(self.n_customers)],
            'geography': np.random.choice(geographies, self.n_customers, p=[0.35, 0.30, 0.25, 0.10]),
            'employment_type': np.random.choice(employment_types, self.n_customers, p=[0.50, 0.25, 0.15, 0.10]),
            'monthly_income': np.random.gamma(shape=2, scale=15000, size=self.n_customers),
            'credit_score_proxy': np.random.normal(650, 100, self.n_customers),
            'acquisition_channel': np.random.choice(channels, self.n_customers, p=[0.35, 0.25, 0.20, 0.10, 0.10]),
            'acquisition_cost': np.random.gamma(shape=2, scale=200, size=self.n_customers),
            'onboarding_date': [self.start_date + timedelta(days=int(x)) for x in np.random.uniform(0, 900, self.n_customers)],
        })
        
        customers['credit_score_proxy'] = customers['credit_score_proxy'].clip(300, 900)
        customers['monthly_income'] = customers['monthly_income'].clip(10000, 500000)
        
        return customers
    
    def generate_loan_data(self, customers):
        """Generate loan product and origination data."""
        products = ['Personal_Loan', 'BNPL', 'SME_Working_Capital']
        product_probs = [0.50, 0.35, 0.15]
        
        loans = pd.DataFrame({
            'loan_id': [f'LOAN_{i:08d}' for i in range(self.n_customers)],
            'customer_id': customers['customer_id'].values,
            'product_type': np.random.choice(products, self.n_customers, p=product_probs),
            'loan_amount': np.random.gamma(shape=2, scale=25000, size=self.n_customers),
            'tenure_months': np.random.choice([12, 24, 36, 48, 60], self.n_customers),
            'interest_rate': np.random.uniform(12, 36, self.n_customers),
            'origination_date': customers['onboarding_date'].values,
            'origination_risk_grade': np.random.choice(['A', 'B', 'C', 'D'], self.n_customers, p=[0.30, 0.35, 0.25, 0.10]),
        })
        
        loans['loan_amount'] = loans['loan_amount'].clip(5000, 500000)
        loans['approval_turnaround_hours'] = np.random.gamma(shape=2, scale=8, size=self.n_customers)
        
        return loans
    
    def generate_repayment_behavior(self, loans):
        """Generate repayment behavior and delinquency data."""
        n_loans = len(loans)
        
        # Base default rate influenced by risk grade
        risk_grade_default_rate = {'A': 0.05, 'B': 0.12, 'C': 0.25, 'D': 0.40}
        default_probability = loans['origination_risk_grade'].map(risk_grade_default_rate)
        
        repayments = pd.DataFrame({
            'loan_id': loans['loan_id'].values,
            'customer_id': loans['customer_id'].values,
            'total_payments_made': np.random.randint(1, 60, n_loans),
            'on_time_payments': np.random.randint(0, 60, n_loans),
            'missed_payments': np.random.randint(0, 10, n_loans),
            'partial_payments_count': np.random.randint(0, 5, n_loans),
            'days_past_due': np.random.gamma(shape=1.5, scale=15, size=n_loans),
            'delinquency_status': np.random.choice(['Current', 'DPD_1-30', 'DPD_31-60', 'DPD_60+', 'Default'], 
                                                   n_loans, p=[0.75, 0.10, 0.07, 0.05, 0.03]),
        })
        
        # Simulate default based on risk grade
        repayments['is_default'] = np.random.binomial(1, default_probability)
        repayments['days_past_due'] = repayments['days_past_due'].clip(0, 120)
        
        return repayments
    
    def generate_behavioral_signals(self, customers):
        """Generate cash flow and behavioral signals."""
        n_customers = len(customers)
        
        behavioral = pd.DataFrame({
            'customer_id': customers['customer_id'].values,
            'avg_monthly_balance': np.random.gamma(shape=2, scale=20000, size=n_customers),
            'balance_volatility': np.random.gamma(shape=2, scale=0.3, size=n_customers),
            'avg_monthly_spending': np.random.gamma(shape=2, scale=15000, size=n_customers),
            'spending_volatility': np.random.gamma(shape=2, scale=0.4, size=n_customers),
            'transaction_frequency': np.random.poisson(50, n_customers),
            'cash_flow_consistency_score': np.random.uniform(0, 100, n_customers),
            'savings_rate': np.random.uniform(-50, 50, n_customers),
        })
        
        behavioral['avg_monthly_balance'] = behavioral['avg_monthly_balance'].clip(0, 1000000)
        behavioral['balance_volatility'] = behavioral['balance_volatility'].clip(0, 2)
        behavioral['cash_flow_consistency_score'] = behavioral['cash_flow_consistency_score'].clip(0, 100)
        
        return behavioral
    
    def generate_full_dataset(self):
        """Generate complete synthetic lending dataset."""
        print("Generating customer profiles...")
        customers = self.generate_customer_profiles()
        
        print("Generating loan data...")
        loans = self.generate_loan_data(customers)
        
        print("Generating repayment behavior...")
        repayments = self.generate_repayment_behavior(loans)
        
        print("Generating behavioral signals...")
        behavioral = self.generate_behavioral_signals(customers)
        
        # Merge all datasets
        print("Merging datasets...")
        full_data = loans.merge(customers, on='customer_id', how='left')
        full_data = full_data.merge(repayments, on=['loan_id', 'customer_id'], how='left')
        full_data = full_data.merge(behavioral, on='customer_id', how='left')
        
        return full_data
    
    def save_dataset(self, data, output_path='data/raw/synthetic_lending_data.csv'):
        """Save generated dataset to CSV."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        data.to_csv(output_path, index=False)
        print(f"Dataset saved to {output_path}")
        return output_path


if __name__ == '__main__':
    generator = SyntheticLendingDataGenerator(n_customers=10000)
    dataset = generator.generate_full_dataset()
    generator.save_dataset(dataset)
    print(f"\nDataset shape: {dataset.shape}")
    print(f"\nDataset columns:\n{dataset.columns.tolist()}")
    print(f"\nFirst few rows:\n{dataset.head()}")
