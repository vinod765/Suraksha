"""
Hindi translation utilities
Uses multiple fallback mechanisms - NO HARDCODED PATHS
"""

from pathlib import Path

# Singleton translator
_translator = None

def get_translator():
    """Load translator model once"""
    global _translator
    if _translator is None:
        try:
            # Try Helsinki-NLP opus-mt model (lightweight)
            from transformers import pipeline
            _translator = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
            print("✅ Loaded translation model: Helsinki-NLP/opus-mt-en-hi")
        except Exception as e:
            print(f"⚠️  Could not load translation model: {e}")
            print("   Using fallback Hindi translations")
            _translator = "fallback"
    return _translator

def translate_to_hindi(text_english):
    """
    Translate English text to Hindi
    
    Args:
        text_english: English text
    
    Returns:
        Hindi translation
    """
    try:
        translator = get_translator()
        
        if translator == "fallback":
            return fallback_hindi_translation(text_english)
        
        # Split long text into chunks (max 512 tokens per chunk)
        max_chunk_length = 400
        chunks = [text_english[i:i+max_chunk_length] 
                  for i in range(0, len(text_english), max_chunk_length)]
        
        translations = []
        for chunk in chunks:
            result = translator(chunk, max_length=512)
            translations.append(result[0]['translation_text'])
        
        return " ".join(translations)
    
    except Exception as e:
        print(f"⚠️  Translation error: {e}")
        return fallback_hindi_translation(text_english)

def fallback_hindi_translation(text_english):
    """
    Fallback Hindi translations for common phrases
    """
    # Key phrase mappings
    translations = {
        "Velocity Fraud": "वेग धोखाधड़ी (Velocity Fraud)",
        "Mule Account": "म्यूल अकाउंट (Mule Account)",
        "SIM Swap": "सिम स्वैप धोखाधड़ी (SIM Swap Fraud)",
        "Device Takeover": "डिवाइस टेकओवर (Device Takeover)",
        "Beneficiary Manipulation": "लाभार्थी हेरफेर (Beneficiary Manipulation)",
        "Amount Anomaly": "राशि असामान्यता (Amount Anomaly)",
        "Temporal Anomaly": "समय असामान्यता (Temporal Anomaly)",
        "Merchant Fraud": "व्यापारी धोखाधड़ी (Merchant Fraud)",
        "Failed-Then-Success": "असफल-फिर-सफल (Failed-Then-Success)",
        "High-Risk Pattern": "उच्च जोखिम पैटर्न (High-Risk Pattern)",
        "Merchant Risk": "व्यापारी जोखिम (Merchant Risk)",
        "FRAUD DETECTED": "धोखाधड़ी का पता चला (FRAUD DETECTED)",
        "Transaction Appears Legitimate": "लेनदेन वैध प्रतीत होता है (Transaction Appears Legitimate)",
        "Confidence": "विश्वास स्तर (Confidence)",
        "Why was this flagged?": "यह क्यों चिह्नित किया गया? (Why was this flagged?)",
        "Key Indicators": "मुख्य संकेतक (Key Indicators)",
        "RBI Guideline Reference": "RBI दिशानिर्देश संदर्भ (RBI Guideline Reference)",
        "Recommended Actions": "अनुशंसित कार्रवाई (Recommended Actions)",
        "Immediate": "तत्काल (Immediate)",
        "Security": "सुरक्षा (Security)",
        "Review": "समीक्षा (Review)",
        "Report": "रिपोर्ट (Report)",
        "Stop transaction and contact your bank": "लेनदेन रोकें और अपने बैंक से संपर्क करें",
        "Change your UPI PIN immediately": "अपना UPI PIN तुरंत बदलें",
        "Check recent transaction history": "हाल के लेनदेन इतिहास की जांच करें",
        "File complaint": "शिकायत दर्ज करें",
        "Your transaction exhibits patterns consistent with": "आपका लेनदेन निम्नलिखित पैटर्न से मेल खाता है:"
    }
    
    result = text_english
    for en, hi in translations.items():
        result = result.replace(en, hi)
    
    return result
