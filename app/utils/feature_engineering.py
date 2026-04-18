"""
Feature Engineering for Suraksha
Generates features for both Advanced and Baseline models
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import configuration
from config import config  # FIXED: was 'from app.config import config'

def engineer_advanced_features(df):
    """
    Engineer features for Advanced 9-class fraud detection
    
    Takes raw transaction data and generates 38 features including:
    - Basic transaction attributes
    - Velocity features (transaction counts)
    - Device/SIM change indicators
    - Amount statistics
    - Temporal features
    
    Args:
        df: DataFrame with raw transaction data
    
    Returns:
        DataFrame with engineered features ready for model input
    """
    
    df = df.copy()
    
    # Encode categorical variables
    df['device_type'] = df['device_type'].map(config.device_map).fillna(0)
    df['network_type'] = df['network_type'].map(config.network_map).fillna(1)
    df['merchant_category'] = df['merchant_category'].map(config.merchant_map).fillna(8)
    df['txn_type'] = df['txn_type'].map(config.txn_type_map).fillna(0)
    
    # Amount features
    df['amount_zscore'] = (df['amount_inr'] - config.amount_mean) / config.amount_std
    df['amount_percentile'] = df['amount_inr'].rank(pct=True)
    df['amount_is_round'] = (df['amount_inr'] % 1000 == 0).astype(int)
    
    # Amount categories
    df['amount_zscore_category'] = pd.cut(df['amount_zscore'], 
                                           bins=[-np.inf, -1, 1, 3, np.inf], 
                                           labels=[0, 1, 2, 3]).astype(int)
    df['amount_percentile_category'] = pd.cut(df['amount_percentile'],
                                               bins=[0, 0.5, 0.9, 0.99, 1.0],
                                               labels=[0, 1, 2, 3]).astype(int)
    
    # Temporal features
    df['hour_of_day'] = df.get('hour_of_day', 12)
    df['is_odd_hours'] = df['hour_of_day'].apply(lambda x: 1 if x < 6 or x > 23 else 0)
    df['day_of_week'] = 1  # Default to Monday
    df['is_weekend'] = 0
    
    # Velocity features (defaults for demo)
    df['sender_txn_count_1min'] = df.get('sender_txn_count_1min', 1)
    df['sender_txn_count_1hour'] = df.get('sender_txn_count_1hour', 1)
    df['sender_txn_count_24h'] = df.get('sender_txn_count_24h', 5)
    df['time_since_last_txn_sec'] = df.get('time_since_last_txn_sec', 300)
    
    # Device/SIM features
    df['device_changed_flag'] = df.get('device_changed_flag', False).astype(int)
    df['sim_change_recent'] = df.get('sim_change_recent', False).astype(int)
    df['sim_age_days'] = df.get('sim_age_days', 365)
    df['location_changed_flag'] = df.get('location_changed_flag', False).astype(int)
    df['mpin_attempts'] = df.get('mpin_attempts', 0)
    
    # Transaction status
    df['txn_status'] = df.get('txn_status', 'SUCCESS')
    df['txn_status'] = (df['txn_status'] == 'SUCCESS').astype(int)
    
    # Relationship features
    df['sender_receiver_history'] = df.get('sender_receiver_history', 0)
    df['receiver_inbound_count_1h'] = df.get('receiver_inbound_count_1h', 1)
    df['receiver_outbound_count_1h'] = df.get('receiver_outbound_count_1h', 0)
    
    # Merchant features
    df['high_risk_merchant'] = df['merchant_category'].isin([1, 3, 8]).astype(int)  # Shopping, Entertainment, Other
    df['merchant_amount_mismatch'] = ((df['merchant_category'] == 0) & (df['amount_inr'] > 5000)).astype(int)
    
    # Composite features
    df['weekend_large_txn'] = (df['is_weekend'] & (df['amount_inr'] > 10000)).astype(int)
    df['failed_count_before'] = df.get('failed_count_before', 0)
    df['failed_then_success'] = ((df['failed_count_before'] > 0) & (df['txn_status'] == 1)).astype(int)
    
    # Bank and state encoding (simplified)
    df['sender_bank'] = 0  # Default
    df['sender_state'] = 0
    df['sender_age_group'] = 1  # Default to 25-35
    df['receiver_bank'] = 0
    df['receiver_state'] = 0
    df['receiver_age_group'] = 1
    
    # Select required features in the correct order
    feature_cols = [
        'sender_bank', 'sender_state', 'sender_age_group', 'device_type', 'network_type',
        'txn_type', 'amount_inr', 'txn_status', 'mpin_attempts', 'device_changed_flag',
        'sim_change_recent', 'sim_age_days', 'location_changed_flag', 'receiver_bank',
        'receiver_state', 'receiver_age_group', 'merchant_category', 'high_risk_merchant',
        'hour_of_day', 'day_of_week', 'is_weekend', 'is_odd_hours', 'amount_is_round',
        'sender_txn_count_1min', 'sender_txn_count_1hour', 'sender_txn_count_24h',
        'time_since_last_txn_sec', 'sender_receiver_history', 'receiver_inbound_count_1h',
        'receiver_outbound_count_1h', 'amount_zscore', 'amount_percentile',
        'amount_zscore_category', 'amount_percentile_category', 'weekend_large_txn',
        'merchant_amount_mismatch', 'failed_count_before', 'failed_then_success'
    ]
    
    return df[feature_cols]

def engineer_baseline_features(df):
    """
    Engineer features for Baseline pattern-based detection
    
    Simpler feature set focused on:
    - Amount thresholds
    - Time of day patterns
    - Merchant risk
    - Basic velocity
    
    Args:
        df: DataFrame with raw transaction data
    
    Returns:
        DataFrame with baseline features
    """
    
    df = df.copy()
    
    # Basic encoding
    df['device_type'] = df['device_type'].map(config.device_map).fillna(0)
    df['network_type'] = df['network_type'].map(config.network_map).fillna(1)
    df['merchant_category'] = df['merchant_category'].map(config.merchant_map).fillna(8)
    
    # Amount features
    df['amount_inr'] = df['amount_inr']
    df['amount_high'] = (df['amount_inr'] > 50000).astype(int)
    df['amount_very_high'] = (df['amount_inr'] > 100000).astype(int)
    
    # Temporal
    df['hour_of_day'] = df.get('hour_of_day', 12)
    df['is_odd_hours'] = df['hour_of_day'].apply(lambda x: 1 if x < 6 or x > 23 else 0)
    
    # Merchant risk
    df['high_risk_merchant'] = df['merchant_category'].isin([1, 3, 8]).astype(int)
    
    # Velocity (simplified)
    df['txn_count_1min'] = df.get('sender_txn_count_1min', 1)
    df['high_velocity'] = (df['txn_count_1min'] >= 5).astype(int)
    
    # Select baseline features
    feature_cols = [
        'amount_inr', 'amount_high', 'amount_very_high', 'hour_of_day', 
        'is_odd_hours', 'device_type', 'network_type', 'merchant_category',
        'high_risk_merchant', 'high_velocity'
    ]
    
    return df[feature_cols]
