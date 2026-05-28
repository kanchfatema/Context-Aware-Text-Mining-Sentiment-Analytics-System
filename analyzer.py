import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def initialize_vader_resource():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except (LookupError, AttributeError):
        nltk.download('vader_lexicon', quiet=True)

initialize_vader_resource()

class ContextSentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        
        # Aggressive negative weights to drop the compound math instantly
        self.vader.lexicon.update({
            'cut': -4.5,
            'managed': -1.5,
            'delayed': -2.0,
            'rude': -2.5
        })

    def analyze_review(self, text):
        if not text or not isinstance(text, str) or text.strip() == "":
            return {"sentiment": "Neutral", "score": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
            
        scores = self.vader.polarity_scores(text)
        compound = scores['compound']
        
        # Widened thresholds to capture mixed reviews securely
        if compound >= 0.30:
            sentiment = "Positive"
        elif compound <= -0.30:
            sentiment = "Negative"
        else:
            sentiment = "Mixed / Neutral"
            
        return {
            "sentiment": sentiment,
            "score": round(compound, 4),
            "pos": round(scores['pos'], 3),
            "neu": round(scores['neu'], 3),
            "neg": round(scores['neg'], 3)
        }