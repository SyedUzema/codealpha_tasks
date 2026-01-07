# 🚀 Quick Start Guide - FAQ Chatbot

Get your chatbot running in **5 minutes**!

---

## ⚡ Fast Setup (3 Steps)

### 1️⃣ Create Project Folder
```bash
mkdir faq-chatbot
cd faq-chatbot
```

### 2️⃣ Create Files

Create these 4 essential files in your project folder:

**File 1: `requirements.txt`**
```text
nltk==3.8.1
scikit-learn==1.3.2
numpy==1.24.3
pandas==2.0.3
streamlit==1.28.1
regex==2023.10.3
```

**File 2: `app.py`** (Copy from the artifact "FAQ Chatbot - Main Application")

**File 3: `chatbot_cli.py`** (Copy from the artifact "FAQ Chatbot - CLI Version")

**File 4: `test_chatbot.py`** (Copy from the artifact "Testing Script")

### 3️⃣ Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run web version (recommended)
streamlit run app.py

# OR run CLI version
python chatbot_cli.py

# OR run tests
python test_chatbot.py
```

---

## 🎯 What Each File Does

| File | Purpose | Use When |
|------|---------|----------|
| `app.py` | Web interface with Streamlit | You want a nice UI for demos |
| `chatbot_cli.py` | Command-line chatbot | You prefer terminal/want simplicity |
| `test_chatbot.py` | Testing and validation | You want to test accuracy |
| `requirements.txt` | Python dependencies | Initial setup |

---

## 📱 Usage Examples

### Web Interface (Streamlit)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- 💬 Interactive chat interface
- 📊 Confidence scores with color coding
- 📜 Chat history
- 💡 Example questions
- ℹ️ Information sidebar

**Try These Questions:**
- "What is your return policy?"
- "How long does shipping take?"
- "Can I track my order?"
- "Do you offer discounts?"

---

### Command-Line Interface

```bash
python chatbot_cli.py
```

**Commands:**
- Type your question → Get answer
- `help` → See example questions
- `quit` or `exit` → Close chatbot

**Example Session:**
```
YOU: How do I return my product?
BOT: We offer a 30-day return policy...
Confidence: 87.5% [✓✓✓ HIGH]
```

---

### Testing Script

```bash
python test_chatbot.py
```

**What It Tests:**
- Exact matches
- Paraphrased questions
- Different phrasings
- Out-of-scope questions
- Preprocessing pipeline
- Similarity thresholds

**Output:**
- Overall accuracy
- Performance by test type
- Recommendations

---

## 🛠️ Customization (5 Minutes)

### Add Your Own FAQs

**Option 1: Edit Directly in Code**

In `app.py` or `chatbot_cli.py`, find the `load_faq_data()` function:

```python
def load_faq_data():
    return [
        {
            "question": "Your question here?",
            "answer": "Your answer here."
        },
        # Add more...
    ]
```

**Option 2: Use JSON File**

Create `data/faqs.json`:
```json
[
  {
    "question": "What is your return policy?",
    "answer": "We offer a 30-day return policy."
  }
]
```

Update `load_faq_data()`:
```python
import json

def load_faq_data():
    with open('data/faqs.json', 'r') as f:
        return json.load(f)
```

---

### Adjust Similarity Threshold

Lower threshold = More answers (but less accurate)  
Higher threshold = Fewer answers (but more accurate)

In both files, find:
```python
chatbot = FAQChatbot(faq_data, similarity_threshold=0.3)
```

**Recommended Values:**
- `0.2` - Very lenient (answers almost everything)
- `0.3` - Balanced (default)
- `0.4` - Conservative (only high-confidence matches)
- `0.5` - Very strict (only very similar questions)

---

### Change Domain/Topic

To change from e-commerce to another domain:

1. **Replace FAQ data** with domain-specific questions
2. **Update UI text**:
   - In `app.py`: Change "E-commerce Customer Support"
   - Update page title and descriptions
3. **Adjust examples** in the sidebar
4. **Test** with domain-specific questions

**Example Domains:**
- University helpdesk
- Healthcare FAQs
- Government services
- Tech support
- Banking queries

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError

**Problem:** Python can't find required modules

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Issue: NLTK Data Not Found

**Problem:** Error about missing punkt, stopwords, or wordnet

**Solution:**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

### Issue: Streamlit Won't Start

**Problem:** `streamlit: command not found`

**Solution:**
```bash
pip install streamlit
# OR
python -m streamlit run app.py
```

---

### Issue: Low Accuracy

**Problem:** Chatbot gives wrong answers

**Solutions:**
1. Lower similarity threshold (0.3 → 0.2)
2. Add more FAQ examples
3. Check preprocessing (run `test_chatbot.py`)
4. Add synonyms to questions

---

### Issue: Too Many False Positives

**Problem:** Chatbot answers unrelated questions

**Solutions:**
1. Raise similarity threshold (0.3 → 0.4)
2. Improve FAQ question clarity
3. Add more diverse FAQs

---

## 📊 Project Structure

```
faq-chatbot/
│
├── app.py                 # Streamlit web UI
├── chatbot_cli.py         # Command-line interface
├── test_chatbot.py        # Testing script
├── requirements.txt       # Dependencies
│
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
│
└── data/                 # Optional
    └── faqs.json         # FAQ data file
```

---

## 🎓 Learning Path

### Beginner (Day 1)
1. ✓ Run the chatbot (CLI version)
2. ✓ Ask sample questions
3. ✓ Read the code comments
4. ✓ Understand the flow

### Intermediate (Day 2-3)
1. ✓ Add your own FAQs
2. ✓ Run the web version
3. ✓ Run tests
4. ✓ Adjust threshold
5. ✓ Read README sections

### Advanced (Day 4-7)
1. ✓ Modify preprocessing
2. ✓ Change domain
3. ✓ Add features (categories, logging)
4. ✓ Improve accuracy
5. ✓ Read Technical Explanation

---

## 💡 Quick Tips

1. **Start with CLI** - It's simpler to understand
2. **Test thoroughly** - Run `test_chatbot.py` after changes
3. **Use example questions** - They're designed to work well
4. **Read error messages** - They usually tell you what's wrong
5. **Experiment** - Change threshold, add FAQs, modify code

---

## 🎯 Next Steps

After getting it running:

1. **Understand the code** - Read through main functions
2. **Customize** - Add your own FAQs
3. **Test** - Try different questions
4. **Improve** - Adjust threshold, add features
5. **Document** - Add comments for your changes
6. **Share** - Show it to friends/add to portfolio

---

## 📚 Key Files to Study

| Priority | File | Why |
|----------|------|-----|
| 🔴 High | `chatbot_cli.py` | Simplest, easiest to understand |
| 🟡 Medium | `app.py` | Full-featured web version |
| 🟢 Low | `test_chatbot.py` | Learn testing practices |

---

## ✅ Success Checklist

- [ ] Installed dependencies
- [ ] Ran CLI version successfully
- [ ] Asked at least 5 questions
- [ ] Ran web version (Streamlit)
- [ ] Understood the flow diagram
- [ ] Ran tests
- [ ] Added one custom FAQ
- [ ] Read code comments
- [ ] Understood preprocessing steps
- [ ] Know how similarity works

---

## 🎉 You're Ready!

You now have a fully functional AI chatbot. Great job!

**What's Next?**
- Read the full README for deep understanding
- Check Technical Explanation for theory
- Customize for your needs
- Add to your portfolio

**Need Help?**
- Read error messages carefully
- Check Troubleshooting section
- Review code comments
- Test with `test_chatbot.py`
