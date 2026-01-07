import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import json

def download_nltk_data():
    required_data = ['punkt', 'stopwords', 'wordnet']
    for data in required_data:
        try:
            nltk.data.find(f'tokenizers/{data}' if data == 'punkt' else f'corpora/{data}')
        except LookupError:
            print(f"Downloading {data}...")
            nltk.download(data, quiet=True)

download_nltk_data()


class FAQChatbot:    
    def __init__(self, faq_data, similarity_threshold=0.3):
       
        self.faq_data = faq_data
        self.similarity_threshold = similarity_threshold
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        self.questions = [faq['question'] for faq in faq_data]
        self.answers = [faq['answer'] for faq in faq_data]
        
        print("Preprocessing FAQ data...")
        self.preprocessed_questions = [self.preprocess_text(q) for q in self.questions]
        
        print("Creating TF-IDF vectors...")
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.preprocessed_questions)
        print("Chatbot ready!\n")
        
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
                "Sorry, I don't understand your question. Please try rephrasing or type 'help' for assistance.",
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
    return [
        {
            "question": "What is your return policy?",
            "answer": "We offer a 30-day return policy for all products. Items must be in original condition with all packaging and accessories."
        },
        {
            "question": "How long does shipping take?",
            "answer": "Standard shipping takes 5-7 business days. Express shipping (2-3 days) and overnight options are available."
        },
        {
            "question": "Do you ship internationally?",
            "answer": "Yes, we ship to over 50 countries worldwide. International shipping typically takes 10-15 business days."
        },
        {
            "question": "How can I track my order?",
            "answer": "You'll receive a tracking number via email once your order ships. You can also track through your account dashboard."
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept all major credit cards, PayPal, Apple Pay, Google Pay, and bank transfers."
        },
        {
            "question": "How do I cancel my order?",
            "answer": "Orders can be cancelled within 2 hours of placement through your account dashboard or by contacting support."
        },
        {
            "question": "Is there a warranty on products?",
            "answer": "All products come with a manufacturer's warranty (1-2 years). Extended warranties are available at checkout."
        },
        {
            "question": "How do I reset my password?",
            "answer": "Click 'Forgot Password' on the login page. You'll receive a reset link via email within 5 minutes."
        },
        {
            "question": "Can I change my shipping address?",
            "answer": "Shipping addresses can be changed before the order ships. Contact support immediately for assistance."
        },
        {
            "question": "Do you offer student discounts?",
            "answer": "Yes! Students receive 10% off all purchases after verifying student status through our partner service."
        },
        {
            "question": "How do I contact customer support?",
            "answer": "Email: support@example.com | Phone: 1-800-TECH-HELP (Mon-Fri 9AM-6PM EST) | Live chat on website."
        },
        {
            "question": "Are the products genuine?",
            "answer": "Yes, all products are 100% authentic and sourced directly from manufacturers or authorized distributors."
        },
        {
            "question": "What if I receive a damaged product?",
            "answer": "Contact us within 48 hours with photos. We'll arrange a free return and send a replacement or issue a refund."
        },
        {
            "question": "Can I modify my order after placing it?",
            "answer": "Order modifications are possible within 2 hours. Contact customer support immediately."
        },
        {
            "question": "Do you have a loyalty program?",
            "answer": "Yes! Earn 5 points per dollar spent. Redeem for discounts and free shipping. Join free through your account."
        }
    ]


def print_header():
    print("=" * 70)
    print("🤖  AI-POWERED FAQ CHATBOT  🤖")
    print("E-commerce Customer Support Assistant")
    print("=" * 70)
    print("\nCommands:")
    print("  - Type your question to get an answer")
    print("  - Type 'help' to see example questions")
    print("  - Type 'quit' or 'exit' to end the conversation")
    print("=" * 70)


def print_help():
    print("\n" + "=" * 70)
    print("EXAMPLE QUESTIONS:")
    print("=" * 70)
    examples = [
        "What is your return policy?",
        "How can I track my order?",
        "Do you ship internationally?",
        "What payment methods do you accept?",
        "How do I reset my password?"
    ]
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    print("=" * 70 + "\n")


def display_response(response):
    print("\n" + "-" * 70)
    print("BOT:", response['answer'])
    print("-" * 70)
    
    # Display confidence with color indicators
    confidence = response['confidence']
    if confidence >= 70:
        status = "HIGH"
        indicator = "✓✓✓"
    elif confidence >= 40:
        status = "MEDIUM"
        indicator = "✓✓"
    else:
        status = "LOW"
        indicator = "✓"
    
    print(f"Confidence: {confidence}% [{indicator} {status}]")
    
    if response['matched_question']:
        print(f"Matched FAQ: \"{response['matched_question']}\"")
    
    print("-" * 70 + "\n")


def main():
    print_header()
    
    faq_data = load_faq_data()
    chatbot = FAQChatbot(faq_data, similarity_threshold=0.3)
    
    while True:
        user_input = input("YOU: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Thank you for using our FAQ Chatbot! Goodbye!\n")
            break
        
        if user_input.lower() in ['help', '?']:
            print_help()
            continue
        
        if not user_input:
            print("⚠️  Please enter a question.\n")
            continue
        
        response = chatbot.get_response(user_input)
        display_response(response)


if __name__ == "__main__":
    main()