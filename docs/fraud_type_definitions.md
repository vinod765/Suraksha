# Fraud Type Definitions

## Behavior-Based Fraud Types (Advanced Mode)

### 1. Velocity Fraud
**Definition:** Multiple transactions from the same sender within a very short time window
**Indicators:** 5+ transactions in 1 minute, time since last transaction < 60 seconds
**RBI Reference:** RBI Annual Report 2023 (18% of UPI fraud)

### 2. Mule Account
**Definition:** Accounts used to layer and move stolen funds
**Indicators:** High inbound and outbound transaction counts, round amounts
**RBI Reference:** RBI AML Guidelines + FATF 2024

### 3. SIM Swap Attack
**Definition:** Attacker replaces victim's SIM to intercept OTPs
**Indicators:** Recent SIM change + device change + multiple transactions
**RBI Reference:** NPCI Advisory Nov 2023 (34% YoY increase)

### 4. Device Takeover
**Definition:** Attacker gains control of victim's device
**Indicators:** Device change + location change + amount > user average * 2
**RBI Reference:** RBI Fraud Taxonomy 2023

### 5. Beneficiary Manipulation
**Definition:** Social engineering to trick victims into sending money to fraudsters
**Indicators:** No sender-receiver history + odd hours + MPIN attempts + round amounts
**RBI Reference:** RBI Consumer Advisory Aug 2024

## Pattern-Based Fraud Types (Baseline Mode)

### 6. Amount Anomaly
**Definition:** Transaction amount significantly deviates from normal patterns
**Indicators:** Z-score > 3, amount percentile > 95%
**RBI Reference:** RBI Statistical Analysis

### 7. Temporal Anomaly
**Definition:** Transactions at unusual times
**Indicators:** Odd hours (2-5 AM), weekend large transactions
**RBI Reference:** NPCI Time-based Fraud Report

### 8. Merchant Fraud
**Definition:** Fraudulent or compromised merchant accounts
**Indicators:** High-risk merchant category, amount mismatch
**RBI Reference:** RBI Merchant Risk Report

### 9. Failed-Then-Success Pattern
**Definition:** Card testing behavior (multiple failures followed by success)
**Indicators:** 2+ failed attempts before success, round amounts
**RBI Reference:** Card Testing Advisory

## Legitimate Transactions (Class 0)
Normal transaction patterns with no fraud indicators
