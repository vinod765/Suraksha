# 🛡️ Fraud Type Definitions - Comprehensive Guide

**Suraksha's 9 UPI Fraud Types Based on RBI Annual Report 2023**

This document provides detailed definitions, real-world examples, detection logic, and prevention measures for each fraud type detected by Suraksha.

---

## 📋 Table of Contents

* [Overview](#overview)
* [Behavior-Based Fraud Types](#behavior-based-fraud-types)
  * [1. Velocity Fraud](#1-velocity-fraud)
  * [2. Mule Account](#2-mule-account)
  * [3. SIM Swap Attack](#3-sim-swap-attack)
  * [4. Device Takeover](#4-device-takeover)
  * [5. Beneficiary Manipulation](#5-beneficiary-manipulation)
* [Pattern-Based Fraud Types](#pattern-based-fraud-types)
  * [6. Amount Anomaly](#6-amount-anomaly)
  * [7. Temporal Anomaly](#7-temporal-anomaly)
  * [8. Merchant Fraud](#8-merchant-fraud)
  * [9. Failed-Then-Success Pattern](#9-failed-then-success-pattern)
* [Class 0: Legitimate Transactions](#class-0-legitimate-transactions)
* [Feature Requirements Summary](#feature-requirements-summary)
* [RBI Guidelines Reference](#rbi-guidelines-reference)

---

## 🎯 Overview

Suraksha detects **9 types of UPI fraud** using a dual-model architecture:

* **Advanced Model** (Behavior-Based): Requires user tracking data, detects 5 complex fraud types
* **Baseline Model** (Pattern-Based): Works without user history, detects 4 statistical anomalies

**Total Classes:** 10 (9 fraud types + 1 legitimate)

**Detection Approach:**
* **Multiclass XGBoost Classifier** - Simultaneously predicts all 10 classes
* **Confidence Scoring** - Provides probability for each fraud type
* **RAG-Enhanced Explanations** - Retrieves relevant RBI guidelines for each detection

---

## 🔴 Behavior-Based Fraud Types

**Requires:** User tracking data (transaction history, device info, SIM status)  
**Model:** Advanced Model only  
**Features:** 38 engineered features with PySpark Window functions

---

### 1. Velocity Fraud

**Definition:**  
Rapid-fire transactions from the same sender account within a very short time window, indicating automated bot attacks or card testing.

**How It Works:**
1. Attacker compromises UPI credentials or payment app
2. Automated script initiates multiple transactions within seconds
3. Goal: Transfer maximum funds before account is frozen
4. Often uses different beneficiaries to avoid single-transaction limits

**Real-World Example:**
```
Victim: Ramesh Kumar (ramesh@upi)
Attack Timeline:
  14:23:05 - ₹5,000 to merchant1@upi
  14:23:12 - ₹5,000 to merchant2@upi  
  14:23:18 - ₹5,000 to merchant3@upi
  14:23:25 - ₹5,000 to merchant4@upi
  14:23:31 - ₹5,000 to merchant5@upi

Total Loss: ₹25,000 in 26 seconds
```

**Key Indicators:**
* ✅ **5+ transactions in 1 minute** (primary indicator)
* ✅ **Time since last transaction < 10 seconds**
* ✅ **Total velocity amount > ₹10,000**
* ✅ Round amounts (₹5,000, ₹10,000)
* ✅ Multiple unique beneficiaries
* ✅ Normal hour of day (not 2-5 AM)

**Features Used:**
```python
# PySpark Window Function (1-minute window)
Window.partitionBy("sender_upi") \
      .orderBy("timestamp") \
      .rangeBetween(-60, 0)

Features:
- txn_count_1min           # Transactions in last 1 minute
- txn_count_5min           # Transactions in last 5 minutes
- velocity_amount_1min     # Total amount in last 1 minute
- time_since_last_txn      # Seconds since previous transaction
- unique_receivers_1min    # Distinct beneficiaries
```

**Detection Logic:**
```python
if txn_count_1min >= 5 and velocity_amount_1min >= 10000:
    fraud_type = "velocity_fraud"
    risk_level = "HIGH"
```

**RBI Reference:**
* **Source:** RBI Annual Report 2023, Chapter 7
* **Statistic:** 18% of UPI fraud cases
* **Guideline:** "Banks should implement transaction velocity checks at customer and merchant level"

**Prevention Measures:**
1. **Velocity Limits:** Max 5 transactions per minute
2. **Cooldown Period:** 30-second wait after 3 rapid transactions
3. **Daily Limits:** ₹1,00,000 for P2P, ₹50,000 for P2M
4. **SMS Alerts:** Real-time notification for each transaction
5. **Auto-Freeze:** Temporarily block account after detection

**Prevalence:**
* 18% of all UPI fraud cases (RBI 2023)
* Average loss: ₹15,000-₹30,000 per incident
* Peak hours: 2-4 PM (afternoon rush)

---

### 2. Mule Account

**Definition:**  
Bank accounts used by money launderers to receive and quickly redistribute stolen funds, creating complex transaction chains to obscure the money trail.

**How It Works:**
1. Fraudster opens multiple accounts (often with fake KYC)
2. Receives stolen funds from fraud victims
3. Immediately transfers to other mule accounts ("layering")
4. Final destination: Cryptocurrency exchange or foreign account
5. Mule receives 10-15% commission

**Real-World Example:**
```
Money Laundering Chain:

Victim → Mule Account 1 (Priya) → Mule Account 2 (Amit) → Mule Account 3 (Sanjay) → Crypto Exchange

Day 1:
  09:15 - Priya receives ₹50,000 from victim1@upi
  09:18 - Priya sends ₹48,000 to Amit
  09:45 - Amit receives ₹48,000 from Priya
  09:50 - Amit sends ₹46,000 to Sanjay
  10:20 - Sanjay receives ₹46,000 from Amit
  10:25 - Sanjay sends ₹45,000 to crypto@upi

Obfuscation: 3 hops in 70 minutes
```

**Key Indicators:**
* ✅ **High inbound transaction count** (10+ per day)
* ✅ **High outbound transaction count** (10+ per day)
* ✅ **Inbound/outbound balance** (~1:1 ratio, quick turnaround)
* ✅ Round amounts (₹10,000, ₹50,000)
* ✅ Multiple unique senders and receivers
* ✅ New account (<30 days old)
* ✅ Low personal consumption (no utility/grocery payments)

**Features Used:**
```python
# PySpark Window Function (30-day window)
Window.partitionBy("sender_upi") \
      .orderBy("timestamp") \
      .rangeBetween(-2592000, 0)  # 30 days in seconds

Features:
- inbound_txn_count_30d     # Received transactions
- outbound_txn_count_30d    # Sent transactions
- unique_senders_30d        # Distinct payers
- unique_receivers_30d      # Distinct payees
- avg_inbound_amount        # Average received
- avg_outbound_amount       # Average sent
- account_age_days          # Days since creation
```

**Detection Logic:**
```python
if (inbound_txn_count_30d >= 20 and 
    outbound_txn_count_30d >= 20 and
    abs(inbound_txn_count_30d - outbound_txn_count_30d) <= 5 and
    account_age_days <= 60):
    fraud_type = "mule_account"
    risk_level = "CRITICAL"
```

**RBI Reference:**
* **Source:** RBI AML/CFT Guidelines 2023 + FATF Report 2024
* **Statistic:** ₹2,400 crores laundered through digital mules in 2023
* **Guideline:** "Enhanced due diligence for accounts with high transaction velocity and low personal expenditure"

**Prevention Measures:**
1. **KYC Verification:** Aadhaar e-KYC for new accounts
2. **Transaction Monitoring:** Flag accounts with >20 txns/day
3. **Cooling Period:** 7-day limit for new accounts (₹10,000/day)
4. **Network Analysis:** Detect layering patterns
5. **Law Enforcement:** Report to Financial Intelligence Unit (FIU)

**Prevalence:**
* ₹2,400+ crores laundered via mule accounts (2023)
* Average mule commission: 10-15% of laundered amount
* Typical mule profile: Age 18-25, unemployed/student

---

### 3. SIM Swap Attack

**Definition:**  
Fraudster convinces telecom provider to transfer victim's mobile number to attacker's SIM card, enabling interception of OTP and complete account takeover.

**How It Works:**
1. Attacker obtains victim's personal info (phishing/data breach)
2. Visits telecom store with fake ID or bribes employee
3. Requests SIM replacement claiming "lost SIM"
4. Victim's SIM deactivated, attacker's SIM activated
5. Attacker now receives all OTPs for UPI/banking
6. Initiates high-value transactions

**Real-World Example:**
```
Victim: Anjali Sharma (9876543210)
Attack Timeline:

Day 1 - 11:00 AM:
  Attacker visits Airtel store with fake Aadhaar
  "I lost my SIM, need replacement for 9876543210"
  Employee issues new SIM to attacker

Day 1 - 11:30 AM:
  Anjali's phone: "No Service"
  Attacker's phone: "SIM activated"

Day 1 - 12:00 PM:
  Attacker opens PhonePe using Anjali's credentials
  Receives OTP on new SIM
  Changes MPIN
  Transaction 1: ₹25,000 to attacker@upi
  Transaction 2: ₹25,000 to attacker2@upi
  Transaction 3: ₹20,000 to attacker3@upi

Total Loss: ₹70,000 in 30 minutes
```

**Key Indicators:**
* ✅ **SIM change in last 24 hours** (critical indicator)
* ✅ **Device change + SIM change** (double red flag)
* ✅ **Multiple MPIN attempts** (attacker trying guesses)
* ✅ High-value transaction (>₹10,000)
* ✅ New beneficiary (no prior transaction history)
* ✅ Round amounts
* ✅ Odd hours (late night)

**Features Used:**
```python
Features:
- sim_change_recent          # 1 if SIM changed in 24 hours
- device_change_recent       # 1 if device changed in 24 hours
- mpin_fail_count           # Failed MPIN attempts
- beneficiary_new           # 1 if never transacted before
- amount_vs_user_avg        # Ratio: current / avg amount
- hour_of_day               # Time of transaction
```

**Detection Logic:**
```python
if (sim_change_recent == 1 and 
    device_change_recent == 1 and
    mpin_fail_count >= 2 and
    amount >= 10000):
    fraud_type = "sim_swap"
    risk_level = "CRITICAL"
```

**RBI Reference:**
* **Source:** NPCI Security Advisory November 2023
* **Statistic:** 34% YoY increase in SIM swap fraud
* **Guideline:** "Immediate freeze on all transactions for 24 hours after SIM change"

**Prevention Measures:**
1. **24-Hour Freeze:** Auto-block UPI after SIM change
2. **Biometric Verification:** Fingerprint required at telecom store
3. **SMS Alert:** Notify alternate number about SIM change
4. **Cooling Period:** ₹5,000 daily limit for 48 hours post-SIM change
5. **Aadhaar OTP:** Mandatory Aadhaar verification for SIM replacement
6. **User Education:** "NEVER share OTP or personal details"

**Prevalence:**
* 34% increase in 2023 (NPCI Advisory)
* Average loss: ₹40,000-₹80,000 per victim
* Most vulnerable: Senior citizens, non-tech-savvy users

---

### 4. Device Takeover

**Definition:**  
Attacker gains unauthorized access to victim's mobile device through malware, remote access trojans (RATs), or physical theft, allowing direct control of payment apps.

**How It Works:**
1. Victim installs malicious app (fake loan app, game, etc.)
2. App requests accessibility permissions
3. Malware captures screen, keystrokes, OTP
4. Attacker remotely controls device (TeamViewer clone)
5. Opens UPI app, bypasses MPIN using keylogger
6. Initiates fraudulent transactions

**Real-World Example:**
```
Victim: Rajesh Patel
Attack Timeline:

Week 1:
  Rajesh receives WhatsApp: "Install this app for ₹5,000 instant loan"
  Downloads APK file "QuickLoan.apk"
  App requests: "Allow accessibility services"
  Malware installed: Remote access trojan

Week 2 - Day 5:
  Attacker activates remote control at 3:00 AM
  Device location changes: Mumbai → Delhi (spoofed)
  Attacker opens Google Pay
  Captures MPIN using keylogger
  
  03:15 - Transfer ₹15,000 to attacker@upi
  03:18 - Transfer ₹15,000 to money-mule@upi
  03:22 - Transfer ₹10,000 to crypto-trader@upi

Rajesh wakes up at 7:00 AM:
  SMS: "₹40,000 debited from your account"
```

**Key Indicators:**
* ✅ **Device change within 7 days**
* ✅ **Location change** (if location services enabled)
* ✅ **Odd hours transaction** (2-5 AM when victim sleeping)
* ✅ **Amount >> user average** (2x or more)
* ✅ New beneficiaries
* ✅ Multiple transactions in sequence
* ✅ No prior device history

**Features Used:**
```python
Features:
- device_change_recent      # 1 if device changed in 7 days
- new_device                # 1 if device never used before
- hour_of_day               # Time (odd hours: 2-5 AM)
- amount_vs_user_avg        # Ratio: current / historical avg
- location_change           # Distance from usual location
- beneficiary_new           # 1 if new recipient
- txn_count_current_device  # Transaction count on this device
```

**Detection Logic:**
```python
if (device_change_recent == 1 and
    hour_of_day >= 2 and hour_of_day <= 5 and
    amount / user_avg_amount >= 2.0 and
    beneficiary_new == 1):
    fraud_type = "device_takeover"
    risk_level = "HIGH"
```

**RBI Reference:**
* **Source:** RBI Fraud Taxonomy and Classification Report 2023
* **Statistic:** Mobile malware fraud doubled in 2022-2023
* **Guideline:** "Step-up authentication required for device change + high-value transaction combination"

**Prevention Measures:**
1. **Device Binding:** Register max 2 devices per UPI ID
2. **Device Change Verification:** OTP to alternate number + email
3. **Behavioral Biometrics:** Detect abnormal usage patterns
4. **Mandatory Lock Screen:** PIN/fingerprint required
5. **Anti-Malware Scanning:** Google Play Protect
6. **User Education:** "Download apps only from official stores"

**Prevalence:**
* Doubled in 2023 (RBI Report)
* Average loss: ₹25,000-₹50,000
* Common vectors: Fake loan apps, game mods, PDF readers

---

### 5. Beneficiary Manipulation

**Definition:**  
Social engineering attack where fraudster tricks victim into voluntarily sending money by impersonating authority figures, creating urgency, or emotional manipulation.

**How It Works:**
1. Attacker impersonates: Bank manager, police, government official, family member
2. Creates panic: "Your account will be blocked!", "Your son is arrested!"
3. Provides fake credentials: Fake ID, uniform, official-looking documents
4. Instructs victim to transfer funds: "For verification", "Pay fine immediately"
5. Victim willingly shares OTP and completes transaction

**Real-World Example:**
```
Victim: Mrs. Lakshmi Devi (65 years old)

Attack Timeline:

Day 1 - 10:30 AM:
  Phone call from +91-11-2345-XXXX (spoofed Delhi number)
  "This is Officer Sharma from CBI Cyber Crime Division"
  "Your Aadhaar is linked to a money laundering case"
  "You must verify your bank account immediately"
  "Transfer ₹50,000 to secure account: officer.cbi@upi"

Victim's Actions:
  Opens Google Pay (device unchanged, her own phone)
  No SIM swap, no device takeover
  Beneficiary: NEW (never transacted before)
  Amount: ₹50,000 (much higher than usual ₹500-₹2,000)
  Multiple MPIN attempts: 3 (nervous, shaking hands)
  Time: 10:45 AM (normal hours, not odd)

Red Flags for Detection:
  ✓ New beneficiary
  ✓ Round amount (₹50,000)
  ✓ Amount >> user average (25x higher)
  ✓ Multiple MPIN attempts
  ✓ Device unchanged BUT recent activity suspicious
  ✓ No sender-receiver transaction history
```

**Key Indicators:**
* ✅ **New beneficiary** (no prior transaction history)
* ✅ **Round amounts** (₹10,000, ₹50,000, ₹1,00,000)
* ✅ **Amount >> user average** (3x or more)
* ✅ **Multiple MPIN attempts** (victim nervous)
* ✅ May have SIM/device change (if remote access involved)
* ✅ Urgent timing (immediate transaction after call)
* ✅ Odd merchant category (if P2M instead of P2P)

**Features Used:**
```python
Features:
- beneficiary_new               # 1 if never transacted before
- sender_receiver_history       # Count of prior transactions
- amount_vs_user_avg           # Ratio: current / avg
- round_amount                 # 1 if amount ends in 000
- mpin_fail_count              # Failed attempts
- device_change_recent         # May or may not be present
- sim_change_recent            # May or may not be present
```

**Detection Logic:**
```python
if (beneficiary_new == 1 and
    sender_receiver_history == 0 and
    amount / user_avg_amount >= 3.0 and
    round_amount == 1 and
    mpin_fail_count >= 2):
    fraud_type = "beneficiary_manipulation"
    risk_level = "HIGH"
```

**RBI Reference:**
* **Source:** RBI Consumer Advisory August 2024
* **Statistic:** 23% YoY increase in social engineering fraud
* **Guideline:** "Banks should display prominent warnings for new beneficiary + high-value transaction combinations"

**Common Impersonation Types:**
1. **Bank/KYC Update:** "Your KYC is expiring, pay ₹500 to update"
2. **Law Enforcement:** "You're under investigation, pay fine"
3. **Family Emergency:** "Your son had accident, send ₹50,000"
4. **Prize/Lottery:** "You won ₹10 lakhs, pay ₹5,000 processing fee"
5. **Fake Job Offer:** "Pay ₹20,000 registration fee for government job"

**Prevention Measures:**
1. **New Beneficiary Warning:** "⚠️ First time sending to this UPI ID. Verify identity."
2. **Cool-Off Period:** 10-minute wait for new beneficiary + high amount
3. **Video KYC:** Optional video call verification for >₹50,000
4. **User Education:** "Bank NEVER asks for payment to verify account"
5. **Transaction Reversal Window:** 30-minute window to cancel/freeze
6. **Family Verification:** Call family member before large transfer

**Prevalence:**
* 23% increase in 2024 (RBI Advisory)
* Average loss: ₹30,000-₹1,50,000
* Most vulnerable: Senior citizens, rural users, first-time UPI users

---

## 🟡 Pattern-Based Fraud Types

**Requires:** Only transaction metadata (amount, time, merchant)  
**Model:** Both Advanced and Baseline models  
**Features:** Statistical analysis without user history

---

### 6. Amount Anomaly

**Definition:**  
Transaction amount significantly deviates from statistical norms, indicating potential fraud or account compromise.

**Key Indicators:**
* Z-score > 3 (3 standard deviations from mean)
* Amount percentile > 95th
* Round amounts (₹50,000, ₹1,00,000)

**Detection Logic:**
```python
amount_zscore = (amount - mean_amount) / std_amount
if amount_zscore > 3.0 and amount_percentile > 95:
    fraud_type = "amount_anomaly"
```

---

### 7. Temporal Anomaly

**Definition:**  
Transactions at unusual times (2-5 AM) when most users are asleep.

**Key Indicators:**
* Hour between 2-5 AM
* Weekend + late night
* High amount during odd hours

**Detection Logic:**
```python
if hour_of_day >= 2 and hour_of_day <= 5 and amount >= 10000:
    fraud_type = "temporal_anomaly"
```

---

### 8. Merchant Fraud

**Definition:**  
High-risk merchant categories or compromised merchant accounts.

**Key Indicators:**
* High-risk categories: Electronics, Jewelry, Travel
* Merchant with high fraud rate history
* Amount mismatch (₹50,000 for grocery)

---

### 9. Failed-Then-Success Pattern

**Definition:**  
Card testing behavior - multiple failed attempts followed by success.

**Key Indicators:**
* 2+ failed transactions
* Success immediately after failures
* Round amounts
* Same beneficiary for all attempts

---

## ✅ Class 0: Legitimate Transactions

**Definition:**  
Normal transaction patterns with no fraud indicators.

**Characteristics:**
* Amount within normal range (₹100-₹5,000)
* Known beneficiaries (repeated transactions)
* Normal hours (9 AM - 10 PM)
* No device/SIM changes
* Low velocity (1-3 transactions per day)

---

## 📊 Feature Requirements Summary

| Fraud Type | User History Required | Min Features | Key Features |
|------------|----------------------|--------------|--------------|
| Velocity Fraud | ✅ Yes | 38 | txn_count_1min, velocity_amount |
| Mule Account | ✅ Yes | 38 | inbound/outbound counts |
| SIM Swap | ✅ Yes | 38 | sim_change, device_change |
| Device Takeover | ✅ Yes | 38 | device_change, location |
| Beneficiary Manip | ✅ Yes | 38 | beneficiary_new, amount_ratio |
| Amount Anomaly | ❌ No | 9 | amount, zscore |
| Temporal Anomaly | ❌ No | 9 | hour_of_day, weekend |
| Merchant Fraud | ❌ No | 9 | merchant_category |
| Failed-Then-Success | ❌ No | 9 | failed_count |

---

## 📚 RBI Guidelines Reference

**Sources:**
1. RBI Annual Report 2023 - Chapter 7: Digital Payment Fraud
2. NPCI Security Advisory November 2023 - SIM Swap Prevention
3. RBI AML/CFT Guidelines 2023 - Mule Account Detection
4. RBI Consumer Advisory August 2024 - Social Engineering Fraud
5. FATF Report 2024 - Digital Payment Money Laundering

**Key Statistics:**
* Total UPI fraud in India (2023): ₹1,200 crores
* Velocity fraud: 18% of cases
* SIM swap: 34% YoY increase
* Mule accounts: ₹2,400 crores laundered
* Social engineering: 23% YoY increase

---

**For implementation details, see:**
* Setup Guide: `docs/setup_guide.md`
* Main README: `README.md`
* Demo Playbook: `JUDGE_DEMO_PLAYBOOK.md`
