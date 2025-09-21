# Language Test Generator

A desktop application built with **Python** and **PyQt5** that generates, evaluates, and manages language learning tests.  
It leverages **Groq LLM API** for creating vocabulary lists, generating questions, and evaluating free-text answers.

---

## ✨ Features

- **Start Menu**  
  Choose between creating a new test or importing an existing one from a JSON file.

- **Custom Test Creation**  
  - Select a topic, language, level (A1–C2), and test size (10–30 questions).  
  - Automatically generates a balanced set of **light, medium, and hard** questions.  
  - Multiple-choice and translation-based tasks.

- **Evaluation**  
  - Uses **Groq API** to evaluate open-ended answers (hard questions).  
  - Provides a final score (0–100%).

- **Import/Export**  
  - Import existing tests from JSON.  
  - Save generated tests for reuse.

- **Dark Themed UI**  
  Consistent Fusion style with dark palette.

---

## 🛠️ Requirements

- Python **3.9+**
- Dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Suggested `requirements.txt`
```txt
PyQt5
python-dotenv
groq
```

---

## 🚀 Usage

1. Clone the repository and install dependencies.
   ```bash
   git clone <your-repo-url>
   cd <your-repo>
   pip install -r requirements.txt
   ```

2. Add your **Groq API key** in `api_keys.env`:
   ```env
   GROQ_API_KEY="your_api_key_here"
   ```

3. Run the app:
   ```bash
   python main.py
   ```

---

## 📂 Project Structure

```
├── app.py              # QApplication subclass with dark theme
├── core.py             # Core logic: test generation & evaluation via Groq API
├── main.py             # Application entry point
├── main_window.py      # Main GUI: navigation, test handling, dialogs
├── screens/            # UI pages (welcome, question, results, etc.)
├── styles/             # Centralized stylesheet definitions
├── resources/          # Icons and images
└── api_keys.env        # Environment file (not tracked in Git)
```

---

## 📖 How It Works

1. **Start Page** → Choose new test or import JSON.  
2. **Setup** → Select topic, language, level, size.  
3. **Generation** → `Core` requests Groq API to create questions.  
4. **Testing** → User answers multiple-choice and open-ended questions.  
5. **Evaluation** → Automatic scoring + explanation.  
6. **Results** → Display score and option to save or retry.

---

## ⚠️ Notes

- Requires a valid **Groq API key** to function.  
- Generated tests depend on topic/level combinations — if insufficient words or questions are found, an error is shown.  
- Exported test format: standard JSON.

---

## 📌 Example JSON Test Structure

```json
{
  "1": {
    "type": "light",
    "question": "Translate 'dog' into Spanish.",
    "right_answer": "perro",
    "answers": ["perro", "gato", "casa", "árbol"]
  },
  "2": {
    "type": "hard",
    "question": "Translate the sentence into German: 'I like reading books.'",
    "right_answer": "Ich lese gern Bücher.",
    "answers": []
  }
}
```

---

## 🧑‍💻 Author

Developed with ❤️ using Python, PyQt5, and Groq LLMs.
