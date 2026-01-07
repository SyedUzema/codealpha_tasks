import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def download_nltk_data():
    """Download required NLTK datasets."""
    required_data = ['punkt', 'stopwords', 'wordnet']
    for data in required_data:
        try:
            nltk.data.find(f'tokenizers/{data}' if data == 'punkt' else f'corpora/{data}')
        except LookupError:
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
        self.categories = [faq.get('category', 'general') for faq in faq_data]
        
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
                self.questions[best_match_idx],
                self.categories[best_match_idx]
            )
        else:
            return (None, best_similarity, None, None)
    
    def get_response(self, user_question):
        answer, confidence, matched_q, category = self.find_best_match(user_question)
        return {
            'answer': answer,
            'confidence': round(confidence * 100, 2),
            'matched_question': matched_q,
            'category': category
        }


def load_faq_data():
    return [
        {
            "question": "What is your return policy?",
            "answer": "We offer a 30-day return policy.",
            "category": "returns"
        },
        {
            "question": "How long does shipping take?",
            "answer": "Standard shipping takes 5-7 business days.",
            "category": "shipping"
        },
        {
            "question": "Do you ship internationally?",
            "answer": "Yes, we ship to over 50 countries worldwide.",
            "category": "shipping"
        },
        {
            "question": "How can I track my order?",
            "answer": "You'll receive a tracking number via email.",
            "category": "tracking"
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept all major credit cards and PayPal.",
            "category": "payment"
        },
        {
            "question": "How do I cancel my order?",
            "answer": "Orders can be cancelled within 2 hours.",
            "category": "orders"
        },
        {
            "question": "Is there a warranty on products?",
            "answer": "All products come with a manufacturer's warranty.",
            "category": "warranty"
        },
        {
            "question": "How do I reset my password?",
            "answer": "Click 'Forgot Password' on the login page.",
            "category": "account"
        },
        {
            "question": "Can I change my shipping address?",
            "answer": "Shipping addresses can be changed before the order ships.",
            "category": "shipping"
        },
        {
            "question": "Do you offer student discounts?",
            "answer": "Yes! Students receive 10% off all purchases.",
            "category": "discounts"
        }
    ]


def run_tests():
    
    print("=" * 80)
    print("FAQ CHATBOT - TESTING SUITE")
    print("=" * 80)
    print()
    
    faq_data = load_faq_data()
    chatbot = FAQChatbot(faq_data, similarity_threshold=0.3)
    
    test_cases = [
        ("What is your return policy?", "returns", "exact_match"),
        ("How long does shipping take?", "shipping", "exact_match"),
        
        ("How do I return a product?", "returns", "paraphrase"),
        ("What are the return rules?", "returns", "paraphrase"),
        ("How much time for delivery?", "shipping", "paraphrase"),
        ("When will my order arrive?", "shipping", "paraphrase"),
        
        ("Can I send items back?", "returns", "different_phrasing"),
        ("Do you allow returns?", "returns", "different_phrasing"),
        ("Where is my package?", "tracking", "different_phrasing"),
        ("How to track shipment?", "tracking", "different_phrasing"),
        
        ("payment", "payment", "single_word"),
        ("warranty", "warranty", "single_word"),
        ("discount", "discounts", "single_word"),
        
        ("What's the weather like?", None, "out_of_scope"),
        ("Tell me a joke", None, "out_of_scope"),
        ("What is machine learning?", None, "out_of_scope"),
    ]
    
    results = {
        'total': len(test_cases),
        'correct': 0,
        'incorrect': 0,
        'by_type': {}
    }
    
    print("RUNNING TEST CASES")
    print("-" * 80)
    print()
    
    for i, (question, expected_category, test_type) in enumerate(test_cases, 1):
        response = chatbot.get_response(question)
        
        if test_type not in results['by_type']:
            results['by_type'][test_type] = {'correct': 0, 'total': 0}
        
        results['by_type'][test_type]['total'] += 1
        
        if expected_category is None:
            is_correct = response['answer'] is None
        else:
            is_correct = response['category'] == expected_category
        
        if is_correct:
            results['correct'] += 1
            results['by_type'][test_type]['correct'] += 1
            status = "✓ PASS"
        else:
            results['incorrect'] += 1
            status = "✗ FAIL"
        
        print(f"Test {i}/{len(test_cases)} [{test_type}] {status}")
        print(f"  Question: {question}")
        print(f"  Expected: {expected_category}")
        print(f"  Got: {response['category']}")
        print(f"  Confidence: {response['confidence']}%")
        
        if response['matched_question']:
            print(f"  Matched: {response['matched_question']}")
        
        print()
    
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    
    accuracy = (results['correct'] / results['total']) * 100
    print(f"Overall Accuracy: {accuracy:.1f}% ({results['correct']}/{results['total']})")
    print()
    
    print("Performance by Test Type:")
    print("-" * 80)
    for test_type, stats in sorted(results['by_type'].items()):
        type_accuracy = (stats['correct'] / stats['total']) * 100
        print(f"  {test_type:20s}: {type_accuracy:5.1f}% ({stats['correct']}/{stats['total']})")
    print()
    
    print("=" * 80)
    print("PERFORMANCE ANALYSIS")
    print("=" * 80)
    print()
    
    if accuracy >= 80:
        print("✓ EXCELLENT: Chatbot performs very well!")
    elif accuracy >= 60:
        print("✓ GOOD: Chatbot performs reasonably well.")
    elif accuracy >= 40:
        print("⚠ FAIR: Consider adjusting threshold or improving preprocessing.")
    else:
        print("✗ POOR: Significant improvements needed.")
    
    print()
    
    print("RECOMMENDATIONS:")
    print("-" * 80)
    
    if results['by_type'].get('out_of_scope', {}).get('correct', 0) < results['by_type'].get('out_of_scope', {}).get('total', 1):
        print("• Threshold may be too low - consider increasing to 0.4 or 0.5")
    
    if results['by_type'].get('paraphrase', {}).get('correct', 0) < results['by_type'].get('paraphrase', {}).get('total', 1) * 0.7:
        print("• Consider using word embeddings (Word2Vec/GloVe) for better semantic matching")
    
    if results['by_type'].get('exact_match', {}).get('correct', 0) < results['by_type'].get('exact_match', {}).get('total', 1):
        print("• Check preprocessing pipeline - exact matches should work")
    
    print()


def test_preprocessing():
    print("=" * 80)
    print("PREPROCESSING PIPELINE TEST")
    print("=" * 80)
    print()
    
    chatbot = FAQChatbot(load_faq_data())
    
    test_texts = [
        "How do I return my product?",
        "What's the SHIPPING time for international orders?",
        "Can I get a refund for damaged items???",
        "I forgot my password :(",
    ]
    
    for text in test_texts:
        processed = chatbot.preprocess_text(text)
        print(f"Original:    {text}")
        print(f"Processed:   {processed}")
        print()


def test_similarity_threshold():
    print("=" * 80)
    print("SIMILARITY THRESHOLD ANALYSIS")
    print("=" * 80)
    print()
    
    faq_data = load_faq_data()
    test_question = "How can I send back my order?"
    
    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    
    for threshold in thresholds:
        chatbot = FAQChatbot(faq_data, similarity_threshold=threshold)
        response = chatbot.get_response(test_question)
        
        print(f"Threshold: {threshold:.1f}")
        print(f"  Answer: {'Found' if response['answer'] else 'Not found'}")
        print(f"  Confidence: {response['confidence']}%")
        if response['matched_question']:
            print(f"  Matched: {response['matched_question']}")
        print()


if __name__ == "__main__":
    test_preprocessing()
    print("\n\n")
    run_tests()
    print("\n\n")
    test_similarity_threshold()
    
    print("=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)