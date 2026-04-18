"""
Translator Utility
Simple text translation to Hindi (placeholder implementation)
"""


# Simple English to Hindi translation dictionary
TRANSLATION_DICT = {
    # Fraud Types
    "Legitimate": "वैध लेनदेन",
    "Amount Anomaly": "राशि में असामान्यता",
    "Temporal Anomaly": "समय संबंधी असामान्यता",
    "Merchant Fraud": "व्यापारी धोखाधड़ी",
    "High-Risk Pattern": "उच्च जोखिम पैटर्न",
    "Velocity Fraud": "वेग धोखाधड़ी",
    "SIM Swap Fraud": "सिम स्वैप धोखाधड़ी",
    "Device Fraud": "डिवाइस धोखाधड़ी",
    "Mule Account": "म्यूल खाता",
    "Beneficiary Fraud": "लाभार्थी धोखाधड़ी",
    
    # Common Terms
    "Transaction": "लेनदेन",
    "Fraud": "धोखाधड़ी",
    "Risk": "जोखिम",
    "Amount": "राशि",
    "Account": "खाता",
    "Low": "कम",
    "Medium": "मध्यम",
    "High": "उच्च",
    "Critical": "गंभीर",
    "Description": "विवरण",
    "Recommendation": "सिफारिश",
    "Risk Level": "जोखिम स्तर",
    
    # Action Terms
    "Verify": "सत्यापित करें",
    "Block": "ब्लॉक करें",
    "Alert": "चेतावनी",
    "Freeze": "फ्रीज करें",
    "Report": "रिपोर्ट करें",
    "Monitor": "निगरानी करें",
    "Contact": "संपर्क करें",
    
    # RBI Guidelines
    "RBI Guidelines": "आरबीआई दिशानिर्देश",
    "RBI advises": "आरबीआई सलाह देता है",
    "RBI mandates": "आरबीआई अनिवार्य करता है",
    "RBI requires": "आरबीआई की आवश्यकता है",
    "RBI Alert": "आरबीआई चेतावनी",
    
    # Common Phrases
    "No action required": "कोई कार्रवाई आवश्यक नहीं",
    "Transaction can proceed safely": "लेनदेन सुरक्षित रूप से आगे बढ़ सकता है",
    "Immediate verification required": "तत्काल सत्यापन आवश्यक",
    "Temporary account freeze": "अस्थायी खाता फ्रीज",
    "Enhanced monitoring": "उन्नत निगरानी",
    "Additional authentication": "अतिरिक्त प्रमाणीकरण",
    "Suspicious activity": "संदिग्ध गतिविधि",
    "Customer verification": "ग्राहक सत्यापन",
    
    # Specific fraud descriptions
    "Transaction appears normal": "लेनदेन सामान्य प्रतीत होता है",
    "No suspicious patterns detected": "कोई संदिग्ध पैटर्न नहीं मिला",
    "Unusually high frequency": "असामान्य रूप से उच्च आवृत्ति",
    "Recent SIM card change": "हाल ही में सिम कार्ड बदला गया",
    "New device detected": "नया डिवाइस पाया गया",
    "Multiple risk indicators": "कई जोखिम संकेतक",
    "Unusual time": "असामान्य समय",
    "High-risk merchant": "उच्च जोखिम व्यापारी",
    
    # Banking Terms
    "Bank": "बैंक",
    "UPI": "यूपीआई",
    "Transaction limit": "लेनदेन सीमा",
    "KYC": "केवाईसी",
    "OTP": "ओटीपी",
    "Registered mobile": "पंजीकृत मोबाइल",
    "Account holder": "खाता धारक",
    "Beneficiary": "लाभार्थी",
    "Merchant": "व्यापारी",
    "Payment": "भुगतान"
}


def translate_to_hindi(text):
    """
    Translate English text to Hindi using simple dictionary mapping.
    Falls back to original text if translation not found.
    
    Args:
        text: English text to translate
        
    Returns:
        Translated Hindi text or original text if no translation available
    """
    
    if not text:
        return text
    
    # Convert to string
    text = str(text)
    
    # Check if exact match exists
    if text in TRANSLATION_DICT:
        return TRANSLATION_DICT[text]
    
    # Try to translate word by word for longer phrases
    translated_parts = []
    for word in text.split():
        # Remove punctuation for matching
        clean_word = word.strip('.,!?;:')
        
        if clean_word in TRANSLATION_DICT:
            # Preserve original punctuation
            punctuation = word[len(clean_word):]
            translated_parts.append(TRANSLATION_DICT[clean_word] + punctuation)
        else:
            translated_parts.append(word)
    
    translated_text = ' '.join(translated_parts)
    
    # If translation looks too similar to original (no Hindi characters), 
    # return the original text with a note
    if not any('\u0900' <= c <= '\u097F' for c in translated_text):
        return f"{text} (अनुवाद उपलब्ध नहीं)"
    
    return translated_text


def translate_fraud_explanation(explanation):
    """
    Translate fraud explanation to Hindi.
    Attempts to preserve formatting while translating key terms.
    
    Args:
        explanation: Full fraud explanation text
        
    Returns:
        Translated explanation
    """
    
    # Split by lines and translate each line
    lines = explanation.split('\n')
    translated_lines = []
    
    for line in lines:
        # Preserve empty lines
        if not line.strip():
            translated_lines.append(line)
            continue
        
        # Preserve markdown formatting markers
        if line.startswith('**') or line.startswith('🚨') or line.startswith('*'):
            # Translate the content but keep markers
            translated_lines.append(translate_to_hindi(line))
        else:
            translated_lines.append(translate_to_hindi(line))
    
    return '\n'.join(translated_lines)


def is_hindi(text):
    """
    Check if text contains Hindi characters.
    
    Args:
        text: Text to check
        
    Returns:
        Boolean indicating if Hindi characters are present
    """
    return any('\u0900' <= c <= '\u097F' for c in str(text))


def get_supported_languages():
    """
    Get list of supported languages.
    
    Returns:
        List of supported language codes
    """
    return ['en', 'hi']
