import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def initialize_nltk_resources():
    resources = {
        'tokenizers/punkt_tab': 'tokenizers/punkt_tab',
        'corpora/stopwords': 'stopwords',
        'taggers/averaged_perceptron_tagger_eng': 'averaged_perceptron_tagger_eng'
    }
    for path, download_name in resources.items():
        try:
            nltk.data.find(path)
        except (LookupError, AttributeError):
            nltk.download(download_name, quiet=True)

initialize_nltk_resources()

class TextProcessor:
    def __init__(self):
        # Base stop words for phrase filtering
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        # Clean whitespaces but preserve casing/structure for accurate grammar tagging
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_features(self, text, n=2):
        """
        Linguistically accurate phrase extractor that tags grammar structures BEFORE 
        filtering to prevent false keyword linkages across sentence boundaries.
        """
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return []

        # Step 1: Tokenize raw string to keep genuine structural layout
        tokens = word_tokenize(cleaned_text)
        
        # Step 2: Tag Parts of Speech immediately on the real sentence
        tagged_words = nltk.pos_tag(tokens)
        
        # Step 3: Generate bi-grams from authentic adjacent word flows
        generated_ngrams = list(ngrams(tagged_words, n))
        
        filtered_phrases = []
        for gram in generated_ngrams:
            word1, tag1 = gram[0]
            word2, tag2 = gram[1]
            
            # Lowercase for uniform validation matching
            w1_clean = re.sub(r'[^a-zA-Z]', '', word1).lower()
            w2_clean = re.sub(r'[^a-zA-Z]', '', word2).lower()
            
            if not w1_clean or not w2_clean:
                continue
                
            # Discard structural linkages built out of basic helper articles/prepositions
            if w1_clean in self.stop_words or w2_clean in self.stop_words:
                continue

            # Step 4: Enforce Context Grammar Rules (Adjective+Noun OR Noun+Noun)
            if (tag1.startswith('JJ') and tag2.startswith('NN')) or (tag1.startswith('NN') and tag2.startswith('NN')):
                filtered_phrases.append(f"{w1_clean} {w2_clean}")
                
        return filtered_phrases