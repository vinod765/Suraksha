"""
Feature Engineering Utility
Converts transaction input into model-ready features
"""

import numpy as np
import pandas as pd
from datetime import datetime


def engineer_baseline_features(input_dict):
    """
    Engineer pattern-based features for baseline model.
    No user tracking - only transaction-level patterns.
    
    Args:
        input_dict: Dictionary with transaction details
        
    Returns:
        numpy array or DataFrame with engineered features
    """
    
    # Extract base fields
    amount = input_dict.get('amount_inr', 0)
    hour = input_dict.get('hour', 12)
    merchant_category = input_dict.get('merchant_category', 'Shopping')
    failed_txn_count = input_dict.get('failed_txn_count', 0)
    
    # Temporal features
    is_odd_hours = 1 if hour < 6 or hour >= 23 else 0
    is_late_night = 1 if 2 <= hour < 5 else 0
    is_business_hours = 1 if 9 <= hour < 17 else 0
    is_weekend = 0  # Simplified
    day_of_week = input_dict.get('timestamp', datetime.now()).weekday()
    month = input_dict.get('timestamp', datetime.now()).month
    
    # Amount features
    amount_zscore = (amount - 1311.76) / 1848.06  # Based on dataset stats
    is_high_amount = 1 if amount >= 4685 else 0
    is_very_high_amount = 1 if amount >= 8987 else 0
    is_round_amount = 1 if amount % 1000 == 0 else 0
    
    # Merchant risk features
    high_risk_categories = ['Entertainment', 'Electronics', 'Jewelry', 'Gambling', 'Adult']
    medium_risk_categories = ['Shopping', 'Travel', 'Luxury']
    
    is_high_risk_merchant = 1 if merchant_category in high_risk_categories else 0
    merchant_risk_score = 3 if is_high_risk_merchant else (2 if merchant_category in medium_risk_categories else 1)
    
    # Pattern features
    failed_txn = 1 if failed_txn_count > 0 else 0
    large_round_amount = 1 if is_round_amount and is_high_amount else 0
    odd_hour_high_amount = 1 if is_odd_hours and is_high_amount else 0
    weekend_high_amount = 1 if is_weekend and is_high_amount else 0
    
    # Composite risk scores
    temporal_risk = (is_odd_hours * 2) + (is_late_night * 3) + (1 - is_business_hours)
    amount_risk = (is_high_amount * 3) + (is_very_high_amount * 3) + (is_round_amount * 2) + min(int(amount_zscore), 1)
    pattern_risk = (is_high_risk_merchant * 3) + (failed_txn * 4) + (large_round_amount * 2) + (odd_hour_high_amount * 2)
    total_risk_score = temporal_risk + amount_risk + pattern_risk
    
    # Create feature array (25 features matching training)
    features = np.array([[
        hour, day_of_week, month,
        is_odd_hours, is_weekend, is_late_night, is_business_hours,
        amount, amount_zscore,
        is_high_amount, is_very_high_amount, is_round_amount,
        is_high_risk_merchant, merchant_risk_score,
        failed_txn, large_round_amount, odd_hour_high_amount, weekend_high_amount,
        temporal_risk, amount_risk, pattern_risk, total_risk_score,
        0, 0, 0  # Padding to match 25 features
    ]])
    
    return features


def engineer_advanced_features(input_dict):
    """
    Engineer advanced features including user behavior patterns.
    Includes device tracking, velocity features, and behavioral analytics.
    
    Args:
        input_dict: Dictionary with transaction details
        
    Returns:
        numpy array or DataFrame with engineered features
    """
    
    # Start with baseline features
    baseline_features = engineer_baseline_features(input_dict)
    
    # Extract advanced fields
    device_id = input_dict.get('device_id', 'UNKNOWN')
    is_new_device = input_dict.get('is_new_device', 0)
    sim_changed = input_dict.get('sim_changed', 0)
    recent_txn_count = input_dict.get('recent_txn_count', 0)
    
    # Device features
    device_risk_score = 0
    if is_new_device:
        device_risk_score += 3
    if sim_changed:
        device_risk_score += 5
    
    # Velocity features
    velocity_risk = 0
    if recent_txn_count > 10:
        velocity_risk = 3
    elif recent_txn_count > 5:
        velocity_risk = 2
    elif recent_txn_count > 2:
        velocity_risk = 1
    
    # Behavioral anomaly score
    behavioral_risk = device_risk_score + velocity_risk
    
    # Additional advanced features
    is_device_anomaly = 1 if device_risk_score >= 3 else 0
    is_velocity_anomaly = 1 if velocity_risk >= 2 else 0
    is_sim_swap_pattern = sim_changed
    is_high_frequency = 1 if recent_txn_count > 10 else 0
    
    # Combine with baseline features
    advanced_features_array = np.array([[
        is_new_device,
        sim_changed,
        recent_txn_count,
        device_risk_score,
        velocity_risk,
        behavioral_risk,
        is_device_anomaly,
        is_velocity_anomaly,
        is_sim_swap_pattern,
        is_high_frequency
    ]])
    
    # Concatenate baseline + advanced features
    combined_features = np.concatenate([baseline_features, advanced_features_array], axis=1)
    
    return combined_features


def prepare_features_dataframe(features, feature_names=None):
    """
    Convert feature array to pandas DataFrame with column names.
    Useful for model explanation and debugging.
    
    Args:
        features: numpy array of features
        feature_names: list of feature column names
        
    Returns:
        pandas DataFrame
    """
    if feature_names is None:
        feature_names = [f'feature_{i}' for i in range(features.shape[1])]
    
    return pd.DataFrame(features, columns=feature_names)
