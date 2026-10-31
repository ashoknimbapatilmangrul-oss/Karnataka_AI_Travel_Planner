PHRASES = [
    {"category": "Greetings", "english": "Hello", "kannada": "ನಮಸ್ಕಾರ", "say": "Namaskara"},
    {"category": "Greetings", "english": "Thank you", "kannada": "ಧನ್ಯವಾದಗಳು", "say": "Dhanyavadagalu"},
    {"category": "Greetings", "english": "Yes", "kannada": "ಹೌದು", "say": "Houdu"},
    {"category": "Greetings", "english": "No", "kannada": "ಇಲ್ಲ", "say": "Illa"},
    {"category": "Greetings", "english": "Please speak slowly", "kannada": "ದಯವಿಟ್ಟು ನಿಧಾನವಾಗಿ ಮಾತನಾಡಿ", "say": "Dayavittu nidhanavagi maatanadi"},
    {"category": "Travel", "english": "Where is the bus stand?", "kannada": "ಬಸ್ ನಿಲ್ದಾಣ ಎಲ್ಲಿದೆ?", "say": "Bus nildana ellide?"},
    {"category": "Travel", "english": "Is it far?", "kannada": "ಇದು ದೂರವೇ?", "say": "Idu doorave?"},
    {"category": "Travel", "english": "Where is the toilet?", "kannada": "ಶೌಚಾಲಯ ಎಲ್ಲಿದೆ?", "say": "Shouchalaya ellide?"},
    {"category": "Shopping", "english": "How much is this?", "kannada": "ಇದರ ಬೆಲೆ ಎಷ್ಟು?", "say": "Idara bele eshtu?"},
    {"category": "Shopping", "english": "Please reduce the price", "kannada": "ದಯವಿಟ್ಟು ಬೆಲೆ ಕಡಿಮೆ ಮಾಡಿ", "say": "Dayavittu bele kadime maadi"},
    {"category": "Food", "english": "Water, please", "kannada": "ದಯವಿಟ್ಟು ನೀರು ಕೊಡಿ", "say": "Dayavittu neeru kodi"},
    {"category": "Food", "english": "One coffee, please", "kannada": "ಒಂದು ಕಾಫಿ ಕೊಡಿ", "say": "Ondu coffee kodi"},
    {"category": "Food", "english": "The food is very tasty", "kannada": "ಊಟ ತುಂಬಾ ರುಚಿಯಾಗಿದೆ", "say": "Oota tumba ruchiyagide"},
    {"category": "Emergency", "english": "Please help me", "kannada": "ದಯವಿಟ್ಟು ಸಹಾಯ ಮಾಡಿ", "say": "Dayavittu sahaya maadi"},
    {"category": "Emergency", "english": "I need a doctor", "kannada": "ನನಗೆ ವೈದ್ಯರು ಬೇಕು", "say": "Nanage vaidyaru beku"},
]


def categories():
    return sorted({p["category"] for p in PHRASES})