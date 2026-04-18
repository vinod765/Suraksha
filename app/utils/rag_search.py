"""
RAG Search Utility
Searches RBI guidelines and fraud explanations
"""


# RBI Guidelines and Fraud Type Explanations
FRAUD_TYPE_GUIDELINES = {
    "Legitimate": {
        "description": "Transaction appears normal with no suspicious patterns detected.",
        "rbi_guideline": "Regular transaction following standard UPI protocols.",
        "recommendation": "No action required. Transaction can proceed safely.",
        "risk_level": "Low"
    },
    
    "Amount Anomaly": {
        "description": "Transaction amount significantly deviates from typical patterns.",
        "rbi_guideline": "RBI advises banks to monitor unusually high-value transactions. "
                        "Transactions above ₹2 lakh require additional verification as per KYC norms.",
        "recommendation": "Verify transaction with customer via registered mobile number. "
                         "Consider implementing transaction limits.",
        "risk_level": "Medium"
    },
    
    "Temporal Anomaly": {
        "description": "Transaction occurring at unusual time (late night/early morning).",
        "rbi_guideline": "RBI guidelines suggest enhanced monitoring for transactions during odd hours (11 PM - 6 AM). "
                        "Banks should implement time-based risk scoring.",
        "recommendation": "Send OTP verification for transactions during odd hours. "
                         "Monitor account for other suspicious activities.",
        "risk_level": "Medium"
    },
    
    "Merchant Fraud": {
        "description": "Transaction with high-risk merchant category or suspicious merchant.",
        "rbi_guideline": "RBI mandates merchant risk categorization and enhanced due diligence for "
                        "high-risk categories like gambling, adult content, and unregistered merchants.",
        "recommendation": "Verify merchant registration and compliance. Block transaction if merchant is flagged. "
                         "Report suspicious merchants to NPCI.",
        "risk_level": "High"
    },
    
    "High-Risk Pattern": {
        "description": "Multiple risk indicators present - combination of suspicious patterns.",
        "rbi_guideline": "RBI requires banks to implement multi-factor authentication and "
                        "transaction monitoring when multiple risk signals are detected.",
        "recommendation": "Immediate verification required. Consider temporary account freeze. "
                         "Contact customer through alternate verified channel.",
        "risk_level": "High"
    },
    
    "Velocity Fraud": {
        "description": "Unusually high frequency of transactions in short time period.",
        "rbi_guideline": "RBI mandates velocity checks - maximum 20 UPI transactions per day with cumulative limit. "
                        "Banks must implement real-time transaction frequency monitoring.",
        "recommendation": "Block further transactions temporarily. Verify recent transactions with customer. "
                         "Check for account compromise or card cloning.",
        "risk_level": "Critical"
    },
    
    "SIM Swap Fraud": {
        "description": "Transaction after recent SIM card change - possible account takeover.",
        "rbi_guideline": "RBI Alert: SIM swap fraud is a growing concern. Banks must implement cooling period "
                        "(24-48 hours) after SIM change before allowing high-value transactions.",
        "recommendation": "IMMEDIATE ACTION: Freeze account temporarily. Verify SIM change with customer "
                         "through alternate contact. Reset all authentication credentials.",
        "risk_level": "Critical"
    },
    
    "Device Fraud": {
        "description": "Transaction from new/unknown device or device takeover detected.",
        "rbi_guideline": "RBI recommends device binding and fingerprinting. New device logins should trigger "
                        "additional authentication and customer notification.",
        "recommendation": "Send alert to registered email and phone. Require device verification. "
                         "Limit transaction amount until device is verified.",
        "risk_level": "High"
    },
    
    "Mule Account": {
        "description": "Account showing patterns of money mule activity - receiving and immediately transferring funds.",
        "rbi_guideline": "RBI/NPCI guidelines mandate identification and blocking of mule accounts used in "
                        "cybercrime. Banks must monitor rapid fund movement patterns.",
        "recommendation": "FREEZE ACCOUNT immediately. Report to cyber crime cell and NPCI. "
                         "Investigate source and destination of funds. File Suspicious Transaction Report (STR).",
        "risk_level": "Critical"
    },
    
    "Beneficiary Fraud": {
        "description": "Transaction to suspicious or newly added beneficiary.",
        "rbi_guideline": "RBI mandates beneficiary verification and cooling period for new beneficiaries. "
                        "Banks should maintain whitelists and blacklists of beneficiaries.",
        "recommendation": "Verify beneficiary details. Implement mandatory cooling period (4-24 hours) for new beneficiaries. "
                         "Check if beneficiary is on fraud/watchlist.",
        "risk_level": "High"
    }
}


def search_rbi_guidelines(fraud_type):
    """
    Search and return RBI guidelines for a specific fraud type.
    
    Args:
        fraud_type: String indicating the type of fraud detected
        
    Returns:
        String with explanation and RBI guidelines
    """
    
    # Normalize fraud type
    fraud_type = str(fraud_type).strip()
    
    # Get guidelines
    guidelines = FRAUD_TYPE_GUIDELINES.get(fraud_type)
    
    if guidelines is None:
        # Fallback for unknown fraud types
        return (
            f"⚠️ Fraud Type: {fraud_type}\n\n"
            "This transaction has been flagged for review. "
            "Please verify transaction details with the customer through registered communication channels.\n\n"
            "RBI Guideline: All suspicious transactions must be investigated and reported as per "
            "RBI Master Direction on Fraud Risk Management."
        )
    
    # Format the response
    explanation = f"""
🚨 **{fraud_type}**

**Description:**
{guidelines['description']}

**RBI Guidelines:**
{guidelines['rbi_guideline']}

**Recommended Actions:**
{guidelines['recommendation']}

**Risk Level:** {guidelines['risk_level']}
"""
    
    return explanation.strip()


def get_all_fraud_types():
    """
    Get list of all supported fraud types.
    
    Returns:
        List of fraud type names
    """
    return list(FRAUD_TYPE_GUIDELINES.keys())


def get_fraud_risk_level(fraud_type):
    """
    Get risk level for a specific fraud type.
    
    Args:
        fraud_type: String indicating the type of fraud
        
    Returns:
        String: Risk level (Low/Medium/High/Critical)
    """
    guidelines = FRAUD_TYPE_GUIDELINES.get(fraud_type)
    if guidelines:
        return guidelines['risk_level']
    return "Unknown"
