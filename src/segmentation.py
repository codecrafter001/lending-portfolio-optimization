"""
Customer Segmentation Module

Provides:
- Risk-based customer segmentation
- Behavioral clustering
- Early warning signal identification
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from typing import Tuple


class CustomerSegmentation:
    """Segment customers based on risk and behavioral patterns."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.segments = None
        
    def prepare_segmentation_features(self) -> Tuple[pd.DataFrame, list]:
        """Prepare features for segmentation."""
        # Select features for clustering
        feature_cols = [
            'credit_score_proxy',
            'monthly_income',
            'interest_rate',
            'acquisition_cost',
            'days_past_due',
            'balance_volatility',
            'spending_volatility',
            'cash_flow_consistency_score',
            'on_time_payments',
        ]
        
        features = self.data[feature_cols].fillna(0)
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        return pd.DataFrame(features_scaled, columns=feature_cols), feature_cols
    
    def segment_customers(self, n_segments=4) -> pd.DataFrame:
        """Segment customers into risk tiers using K-means."""
        features_scaled, _ = self.prepare_segmentation_features()
        
        kmeans = KMeans(n_clusters=n_segments, random_state=42, n_init=10)
        self.data['risk_segment'] = kmeans.fit_predict(features_scaled)
        
        # Label segments based on default rate
        segment_default_rates = self.data.groupby('risk_segment')['is_default'].mean()
        segment_ranking = segment_default_rates.rank()
        segment_labels = {i: f'Tier_{int(segment_ranking[i])}' for i in range(n_segments)}
        self.data['risk_tier'] = self.data['risk_segment'].map(segment_labels)
        
        return self.data[['customer_id', 'risk_segment', 'risk_tier']]
    
    def identify_early_warning_signals(self) -> pd.DataFrame:
        """Identify customers showing signs of financial stress."""
        early_warnings = pd.DataFrame()
        early_warnings['customer_id'] = self.data['customer_id']
        early_warnings['loan_id'] = self.data['loan_id']
        
        # Define warning signals
        early_warnings['high_days_past_due'] = (self.data['days_past_due'] > 30).astype(int)
        early_warnings['high_spending_volatility'] = (self.data['spending_volatility'] > self.data['spending_volatility'].quantile(0.75)).astype(int)
        early_warnings['low_cash_flow_consistency'] = (self.data['cash_flow_consistency_score'] < self.data['cash_flow_consistency_score'].quantile(0.25)).astype(int)
        early_warnings['declining_balance'] = (self.data['balance_volatility'] > self.data['balance_volatility'].quantile(0.75)).astype(int)
        early_warnings['high_missed_payments'] = (self.data['missed_payments'] > 2).astype(int)
        
        # Calculate risk score
        early_warnings['warning_score'] = (
            early_warnings['high_days_past_due'] * 3 +
            early_warnings['high_spending_volatility'] * 2 +
            early_warnings['low_cash_flow_consistency'] * 2 +
            early_warnings['declining_balance'] * 1.5 +
            early_warnings['high_missed_payments'] * 2.5
        )
        
        early_warnings['warning_level'] = pd.cut(
            early_warnings['warning_score'],
            bins=[-1, 0, 3, 7, 100],
            labels=['No_Risk', 'Low_Risk', 'Medium_Risk', 'High_Risk']
        )
        
        return early_warnings
    
    def segment_profile(self) -> pd.DataFrame:
        """Generate detailed profile for each segment."""
        if self.data['risk_tier'].isna().all():
            self.segment_customers()
        
        profile = self.data.groupby('risk_tier').agg({
            'customer_id': 'count',
            'monthly_income': 'mean',
            'credit_score_proxy': 'mean',
            'loan_amount': 'mean',
            'interest_rate': 'mean',
            'is_default': 'mean',
            'days_past_due': 'mean',
            'cash_flow_consistency_score': 'mean',
            'on_time_payments': 'mean',
        }).round(2)
        
        profile.columns = [
            'Customer_Count',
            'Avg_Monthly_Income',
            'Avg_Credit_Score',
            'Avg_Loan_Amount',
            'Avg_Interest_Rate',
            'Default_Rate',
            'Avg_DPD',
            'Cash_Flow_Consistency',
            'Avg_On_Time_Payments'
        ]
        
        return profile


if __name__ == '__main__':
    # Example usage
    data = pd.read_csv('data/raw/synthetic_lending_data.csv')
    segmenter = CustomerSegmentation(data)
    
    print("\n=== CUSTOMER SEGMENTATION ===")
    segments = segmenter.segment_customers()
    print(segments.head(10))
    
    print("\n=== SEGMENT PROFILE ===")
    print(segmenter.segment_profile())
    
    print("\n=== EARLY WARNING SIGNALS ===")
    warnings = segmenter.identify_early_warning_signals()
    print(warnings[warnings['warning_level'] == 'High_Risk'].head())
