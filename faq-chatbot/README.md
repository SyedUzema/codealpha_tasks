# 🤖 AI-Powered FAQ Chatbot

An intelligent FAQ chatbot built with Natural Language Processing (NLP) and Machine Learning to automatically answer customer queries for an e-commerce electronics store.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Technical Details](#technical-details)
- [Customization](#customization)
- [Future Enhancements](#future-enhancements)

## ✨ Features

- **Natural Language Processing**: Preprocesses text using tokenization, stopword removal, and lemmatization
- **TF-IDF Vectorization**: Converts questions into numerical representations
- **Cosine Similarity Matching**: Finds the most relevant FAQ based on semantic similarity
- **Confidence Scoring**: Shows how confident the bot is in its answer
- **Two Interfaces**: 
  - Beautiful web UI using Streamlit
  - Simple command-line interface
- **Fallback Handling**: Gracefully handles questions outside the FAQ scope
- **Real-time Processing**: Fast response times for instant customer support

## 📁 Project Structure

```
faq-chatbot/
│
├── app.py                  # Streamlit web application
├── chatbot_cli.py          # Command-line interface
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
├── data/                  # (Optional) External data folder
│   └── faqs.json         # FAQ data in JSON format
│
└── notebooks/            # (Optional) Jupyter notebooks
    └── experiment.ipynb  # For testing and experimentation
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download the Project
```bash
# Create project directory
mkdir faq-chatbot
cd faq-chatbot
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
The application will automatically download required NLTK data on first run, but you can also do it manually:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

## 💻 Usage

### Option 1: Web Interface (Streamlit)

Run the Streamlit web application:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

**Features of Web Interface:**
- Interactive chat interface
- Visual confidence indicators
- Chat history
- Example questions
- Sidebar with information

### Option 2: Command-Line Interface

Run the CLI version:
```bash
python chatbot_cli.py
```

**CLI Commands:**
- Type your question and press Enter
- Type `help` to see example questions
- Type `quit` or `exit` to close the chatbot

## 🔧 How It Works

### 1. **Data Collection & Structuring**
- 15 pre-defined FAQs covering common e-commerce queries
- Each FAQ has a question-answer pair
- Topics include: returns, shipping, payments, support, etc.

### 2. **Text Preprocessing Pipeline**

```python
User Question → Lowercase → Remove Special Chars → Tokenize → 
Remove Stopwords → Lemmatize → Processed Text
```

**Example:**
- Input: "How do I return my product?"
- After preprocessing: "return product"

### 3. **TF-IDF Vectorization**
- **TF (Term Frequency)**: How often a word appears in a document
- **IDF (Inverse Document Frequency)**: How unique/important a word is
- Converts text into numerical vectors for mathematical comparison

### 4. **Cosine Similarity Calculation**
- Measures the angle between two vectors
- Range: 0 (completely different) to 1 (identical)
- Formula: `similarity = (A · B) / (||A|| × ||B||)`

### 5. **Response Generation**
- If similarity ≥ threshold (0.3): Return matched answer
- If similarity < threshold: Return fallback message
- Include confidence score and matched question

## 📊 Technical Details

### Core Technologies
- **NLTK**: Natural Language Toolkit for text preprocessing
- **scikit-learn**: TF-IDF vectorization and cosine similarity
- **Streamlit**: Web interface framework
- **NumPy**: Numerical computations

### NLP Techniques Used

| Technique | Purpose | Example |
|-----------|---------|---------|
| **Lowercasing** | Normalize text | "Hello" → "hello" |
| **Tokenization** | Split into words | "Hello world" → ["Hello", "world"] |
| **Stopword Removal** | Remove common words | ["I", "am", "happy"] → ["happy"] |
| **Lemmatization** | Reduce to base form | "running" → "run" |

### Similarity Threshold
- **Default**: 0.3 (30% similarity)
- **High confidence**: ≥ 70%
- **Medium confidence**: 40-69%
- **Low confidence**: < 40%

You can adjust the threshold in the code:
```python
chatbot = FAQChatbot(faq_data, similarity_threshold=0.3)
```

## 🎨 Customization

### Adding New FAQs

Edit the `load_faq_data()` function in either file:

```python
faq_data = [
    {
        "question": "Your new question?",
        "answer": "Your detailed answer here."
    },
    # Add more...
]
```

### Changing the Domain

To adapt this chatbot for a different domain (e.g., university, healthcare):

1. Replace FAQ data with domain-specific questions
2. Adjust the similarity threshold if needed
3. Update the UI text and branding
4. Optionally add domain-specific preprocessing

### Modifying Preprocessing

In the `preprocess_text()` method, you can:
- Add custom stopwords
- Use stemming instead of lemmatization
- Add spell correction
- Include synonym expansion

### Using External Data File

Create `data/faqs.json`:
```json
[
  {
    "question": "What is your return policy?",
    "answer": "We offer 30-day returns..."
  }
]
```

Load it in code:
```python
import json

def load_faq_data():
    with open('data/faqs.json', 'r') as f:
        return json.load(f)
```

## 🔮 Future Enhancements

### Short-term
- [ ] Add FAQ categories/tags
- [ ] Implement conversation history persistence
- [ ] Add multi-language support
- [ ] Export chat transcripts

### Medium-term
- [ ] Use word embeddings (Word2Vec, GloVe)
- [ ] Implement intent classification
- [ ] Add entity recognition for products/orders
- [ ] Create admin panel for FAQ management

### Long-term
- [ ] Integrate with actual e-commerce platform
- [ ] Use transformer models (BERT, GPT)
- [ ] Add voice input/output
- [ ] Implement learning from user feedback
- [ ] Multi-turn conversations with context

## 📝 Key Concepts Explained

### Why TF-IDF?
- Simple and effective for short text
- No training required
- Fast computation
- Works well for FAQ matching

### Why Cosine Similarity?
- Scale-independent (works regardless of text length)
- Measures semantic similarity
- Fast to compute
- Standard in information retrieval

### Limitations
- No context awareness (stateless)
- Can't handle complex queries spanning multiple FAQs
- Limited to predefined answers
- May struggle with very creative phrasings

## 🎓 Educational Value

This project demonstrates:
- **NLP fundamentals**: Tokenization, lemmatization, stopwords
- **Feature engineering**: TF-IDF vectorization
- **Similarity metrics**: Cosine similarity
- **Machine Learning pipeline**: Preprocessing → Vectorization → Prediction
- **Software engineering**: Clean code, modular design, UI/UX
- **Python libraries**: NLTK, scikit-learn, Streamlit

## 📚 Learning Resources

- [NLTK Documentation](https://www.nltk.org/)
- [scikit-learn TF-IDF Guide](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)
- [Cosine Similarity Explained](https://en.wikipedia.org/wiki/Cosine_similarity)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 👨‍💻 Author

- Syed Uzema

## 🙏 Acknowledgments

- NLTK team for excellent NLP tools
- scikit-learn for machine learning utilities
- Streamlit for the amazing web framework
