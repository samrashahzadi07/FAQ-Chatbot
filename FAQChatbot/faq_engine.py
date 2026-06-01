"""
faq_engine.py — NLP-powered FAQ matching engine
Uses TF-IDF vectorization + cosine similarity to find the best FAQ match.
"""

import re
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from faq_data import faqs

# Ensure NLTK data is available
for resource in ['punkt', 'stopwords', 'wordnet', 'punkt_tab']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)


class FAQEngine:
    def __init__(self, confidence_threshold: float = 0.15):
        self.faqs = faqs
        self.threshold = confidence_threshold
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

        # Preprocess all FAQ questions
        self.processed_questions = [self._preprocess(f["question"]) for f in self.faqs]

        # Fit TF-IDF vectorizer on FAQ questions
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),   # unigrams + bigrams
            min_df=1,
            analyzer='word',
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_questions)

    def _preprocess(self, text: str) -> str:
        """Lowercase, remove punctuation, remove stopwords, lemmatize."""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        tokens = text.split()
        tokens = [
            self.lemmatizer.lemmatize(t)
            for t in tokens
            if t not in self.stop_words and len(t) > 1
        ]
        return ' '.join(tokens)

    def get_response(self, user_query: str) -> dict:
        """
        Find the best matching FAQ for the user query.
        Returns dict with: answer, matched_question, confidence, status
        """
        processed_query = self._preprocess(user_query)

        if not processed_query.strip():
            return {
                "answer": "Please type a question and I'll do my best to help!",
                "matched_question": None,
                "confidence": 0.0,
                "status": "empty",
            }

        # Vectorize the user query
        try:
            query_vec = self.vectorizer.transform([processed_query])
        except Exception:
            return {
                "answer": "Sorry, I couldn't process your question. Please try rephrasing.",
                "matched_question": None,
                "confidence": 0.0,
                "status": "error",
            }

        # Compute cosine similarities against all FAQ questions
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score < self.threshold:
            return {
                "answer": (
                    "I'm not sure I have an answer for that. "
                    "Try asking about CodeAlpha internship, Python, AI/ML concepts, "
                    "Streamlit, YOLO, NLTK, or other tech topics."
                ),
                "matched_question": None,
                "confidence": best_score,
                "status": "low_confidence",
            }

        return {
            "answer": self.faqs[best_idx]["answer"],
            "matched_question": self.faqs[best_idx]["question"],
            "confidence": best_score,
            "status": "ok",
        }

    def get_all_questions(self) -> list[str]:
        """Return all FAQ questions for display."""
        return [f["question"] for f in self.faqs]

    def get_topic_groups(self) -> dict:
        """Return questions grouped by broad topic."""
        groups = {
            "🎓 CodeAlpha Internship": [],
            "🐍 Python & Tools":       [],
            "🤖 AI / ML Concepts":     [],
            "🎵 Music & Vision":       [],
        }
        for f in self.faqs:
            q = f["question"]
            if any(k in q for k in ["CodeAlpha", "internship", "task", "certificate", "submit", "GitHub", "contact"]):
                groups["🎓 CodeAlpha Internship"].append(q)
            elif any(k in q for k in ["Python", "pip", "virtual", "Streamlit", "scikit", "NLTK", "OpenCV"]):
                groups["🐍 Python & Tools"].append(q)
            elif any(k in q for k in ["machine learning", "deep learning", "NLP", "neural", "TF-IDF", "cosine",
                                       "chatbot", "TensorFlow", "PyTorch", "dataset", "overfitting", "AI", "LSTM"]):
                groups["🤖 AI / ML Concepts"].append(q)
            else:
                groups["🎵 Music & Vision"].append(q)
        return groups