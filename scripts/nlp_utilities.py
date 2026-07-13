"""
Natural Language Processing Utilities
Text processing, tokenization, sentiment analysis, and NLP tasks
"""

import re
import string
from typing import List, Dict, Tuple, Any
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class TextProcessor:
    """Advanced text processing and analysis utilities"""
    
    def __init__(self, lowercase: bool = True, remove_punctuation: bool = True):
        """
        Initialize Text Processor
        
        Args:
            lowercase (bool): Convert to lowercase
            remove_punctuation (bool): Remove punctuation
        """
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
        self.stop_words = self._load_stop_words()
        
    def _load_stop_words(self) -> set:
        """
        Load common English stop words
        
        Returns:
            set: Stop words
        """
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'as', 'if', 'it', 'we', 'you', 'he', 'she', 'they'
        }
        return stop_words
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text
        """
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        if self.lowercase:
            text = text.lower()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text (str): Input text
            
        Returns:
            list: Tokens
        """
        text = self.clean_text(text)
        tokens = text.split()
        return tokens
    
    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """
        Remove stop words from tokens
        
        Args:
            tokens (list): Input tokens
            
        Returns:
            list: Filtered tokens
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def calculate_word_frequency(self, text: str, top_k: int = 10) -> Dict[str, int]:
        """
        Calculate word frequency
        
        Args:
            text (str): Input text
            top_k (int): Top K words
            
        Returns:
            dict: Word frequencies
        """
        tokens = self.tokenize(text)
        tokens = self.remove_stop_words(tokens)
        freq = Counter(tokens)
        return dict(freq.most_common(top_k))
    
    def calculate_tf_idf(self, documents: List[str]) -> np.ndarray:
        """
        Calculate TF-IDF scores
        
        Args:
            documents (list): List of documents
            
        Returns:
            np.ndarray: TF-IDF matrix
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words=list(self.stop_words))
        tfidf_matrix = vectorizer.fit_transform(documents)
        return tfidf_matrix.toarray()
    
    def extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text (str): Input text
            top_k (int): Number of keywords
            
        Returns:
            list: Keywords
        """
        freq = self.calculate_word_frequency(text, top_k=len(self.tokenize(text)))
        return list(dict(sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_k]).keys())
    
    def calculate_text_statistics(self, text: str) -> Dict[str, Any]:
        """
        Calculate text statistics
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Text statistics
        """
        tokens = self.tokenize(text)
        sentences = text.split('.')
        
        return {
            'character_count': len(text),
            'word_count': len(tokens),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'average_word_length': np.mean([len(token) for token in tokens]) if tokens else 0,
            'unique_words': len(set(tokens)),
            'lexical_diversity': len(set(tokens)) / len(tokens) if tokens else 0
        }
    
    def simple_sentiment_score(self, text: str) -> Dict[str, float]:
        """
        Simple sentiment analysis based on word lists
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Sentiment scores
        """
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'positive', 'love', 'best', 'beautiful', 'outstanding', 'perfect'
        }
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'negative',
            'poor', 'ugly', 'disappointing', 'failed', 'wrong'
        }
        
        tokens = self.tokenize(text)
        
        positive_count = sum(1 for token in tokens if token in positive_words)
        negative_count = sum(1 for token in tokens if token in negative_words)
        total_words = len(tokens)
        
        return {
            'positive_score': positive_count / total_words if total_words > 0 else 0,
            'negative_score': negative_count / total_words if total_words > 0 else 0,
            'sentiment': 'positive' if positive_count > negative_count else 'negative' if negative_count > positive_count else 'neutral'
        }


# Example usage
if __name__ == '__main__':
    processor = TextProcessor()
    
    sample_text = """
    This is an amazing and wonderful example text! 
    It contains many great words and excellent ideas.
    Natural language processing is fantastic!
    """
    
    print('Text Statistics:', processor.calculate_text_statistics(sample_text))
    print('Keywords:', processor.extract_keywords(sample_text))
    print('Sentiment:', processor.simple_sentiment_score(sample_text))
    print('Word Frequency:', processor.calculate_word_frequency(sample_text))
