import streamlit as st
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class FAQChatbot:

    def __init__(self, faq_data, similarity_threshold=0.3):
        self.faq_data = faq_data
        self.similarity_threshold = similarity_threshold
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

        self.questions = [faq['question'] for faq in faq_data]
        self.answers = [faq['answer'] for faq in faq_data]

        self.preprocessed_questions = [self.preprocess_text(q) for q in self.questions]

        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.preprocessed_questions)

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = word_tokenize(text)
        processed_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]
        return ' '.join(processed_tokens)

    def find_best_match(self, user_question):
        processed_question = self.preprocess_text(user_question)
        user_vector = self.vectorizer.transform([processed_question])
        similarities = cosine_similarity(user_vector, self.question_vectors)

        best_match_idx = np.argmax(similarities[0])
        best_similarity = similarities[0][best_match_idx]

        if best_similarity >= self.similarity_threshold:
            return (
                self.answers[best_match_idx],
                best_similarity,
                self.questions[best_match_idx]
            )
        else:
            return (
                "Sorry, I don't understand your question. Please try rephrasing or contact our support team for assistance.",
                best_similarity,
                None
            )

    def get_response(self, user_question):
        answer, confidence, matched_q = self.find_best_match(user_question)
        return {
            'answer': answer,
            'confidence': round(confidence * 100, 2),
            'matched_question': matched_q
        }


def load_faq_data():
    faq_data = [
        {
            "question": "What is your return policy?",
            "answer": "We offer a 30-day return policy for all products. Items must be in original condition with all packaging and accessories. Please initiate returns through your account dashboard or contact support."
        },
        {
            "question": "How long does shipping take?",
            "answer": "Standard shipping takes 5-7 business days. Express shipping (2-3 days) and overnight shipping options are available at checkout for an additional fee."
        },
        {
            "question": "Do you ship internationally?",
            "answer": "Yes, we ship to over 50 countries worldwide. International shipping times vary by location (typically 10-15 business days). Customs fees may apply depending on your country."
        },
        {
            "question": "How can I track my order?",
            "answer": "Once your order ships, you'll receive a tracking number via email. You can also track your order by logging into your account and viewing order history. Tracking updates may take 24 hours to appear."
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept all major credit cards (Visa, MasterCard, American Express, Discover), PayPal, Apple Pay, Google Pay, and bank transfers. Payment is processed securely through encrypted connections."
        },
        {
            "question": "How do I cancel my order?",
            "answer": "Orders can be cancelled within 2 hours of placement. Log into your account, go to order history, and click 'Cancel Order'. If your order has already shipped, you'll need to initiate a return instead."
        },
        {
            "question": "Is there a warranty on products?",
            "answer": "All products come with a manufacturer's warranty (typically 1-2 years depending on the item). Extended warranty options are available at checkout. Warranty details are included with your product."
        },
        {
            "question": "How do I reset my password?",
            "answer": "Click 'Forgot Password' on the login page and enter your email address. You'll receive a password reset link within 5 minutes. If you don't receive it, check your spam folder or contact support."
        },
        {
            "question": "Can I change my shipping address?",
            "answer": "Shipping addresses can be changed before the order ships. Contact customer support immediately or update it in your order details. Once shipped, the address cannot be changed."
        },
        {
            "question": "Do you offer student discounts?",
            "answer": "Yes! Students receive 10% off all purchases. Verify your student status through our partner verification service. The discount will be automatically applied at checkout once verified."
        },
        {
            "question": "How do I contact customer support?",
            "answer": "You can reach our support team via email at support@example.com, phone at 1-800-TECH-HELP (Mon-Fri 9AM-6PM EST), or live chat on our website. Average response time is under 2 hours."
        },
        {
            "question": "Are the products genuine?",
            "answer": "Yes, all products sold on our platform are 100% authentic and sourced directly from manufacturers or authorized distributors. We guarantee authenticity and provide certificates when applicable."
        },
        {
            "question": "What if I receive a damaged product?",
            "answer": "If you receive a damaged product, please contact us within 48 hours with photos of the damage. We'll arrange a free return and send a replacement immediately or issue a full refund."
        },
        {
            "question": "Can I modify my order after placing it?",
            "answer": "Order modifications are possible within 2 hours of placement. Contact customer support immediately. After this window, orders enter processing and cannot be modified."
        },
        {
            "question": "Do you have a loyalty program?",
            "answer": "Yes! Our rewards program gives you 5 points for every dollar spent. Points can be redeemed for discounts, free shipping, and exclusive products. Join free through your account dashboard."
        }
    ]
    return faq_data


def main():
    st.set_page_config(
        page_title="FAQ Chatbot",
        page_icon="🤖",
        layout="centered"
    )

    st.markdown("""
        <style>
        .main-header { font-size: 2.5rem; color: #1E88E5; text-align: center; }
        .sub-header { text-align: center; color: #666; margin-bottom: 2rem; }
        .confidence-high { color: #4CAF50; font-weight: bold; }
        .confidence-medium { color: #FF9800; font-weight: bold; }
        .confidence-low { color: #F44336; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">🤖 AI FAQ Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">E-commerce Customer Support Assistant</p>', unsafe_allow_html=True)

    if 'chatbot' not in st.session_state:
        faq_data = load_faq_data()
        st.session_state.chatbot = FAQChatbot(faq_data)
        st.session_state.chat_history = []

    with st.sidebar:
        st.header("About")
        st.info("This chatbot uses NLP and machine learning to answer e-commerce questions.")
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['question']}")
            st.markdown(f"**Bot:** {chat['answer']}")
            st.markdown(f"Confidence: {chat['confidence']}%")
            st.divider()

    user_question = st.text_input("Type your question here:")
    if st.button("Send") and user_question.strip():
        response = st.session_state.chatbot.get_response(user_question)
        st.session_state.chat_history.append({
            'question': user_question,
            'answer': response['answer'],
            'confidence': response['confidence'],
            'matched_question': response['matched_question']
        })
        st.rerun()


if __name__ == "__main__":
    main()
