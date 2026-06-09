# 📚 AI Study Assistant

An interactive web app that explains Computer Science concepts using AI and tests your understanding with a quiz — all in your browser.

## Features

- **Concept Explainer** — pick a CS subject, type any concept, and get a clear explanation with an analogy, definition, how it works, and why it matters
- **Interactive Quiz** — after each explanation, answer 3 auto-generated multiple choice questions
- **Instant Feedback** — see your score and which answers were correct
- **7 CS Subjects** — Deep Learning, Machine Learning, Computer Vision, Data Structures & Algorithms, Programming in AI, Computer Graphics, General CS

## Demo

![AI Study Assistant Screenshot](screenshot.png)

## Tech Stack

- **Python** — core language
- **Streamlit** — web interface
- **Groq API** — fast LLM inference (Llama 3.3 70B)
- **python-dotenv** — environment variable management

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-study-assistant.git
cd ai-study-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run app.py
```
The app will open at `http://localhost:8501`

## Project Structure

```
ai-study-assistant/
├── app.py           # Main application
├── requirements.txt # Dependencies
├── .env             # API key (not committed)
├── .gitignore       # Ignores .env
└── README.md        # This file
```

## Author

Shahada Alsubhi — [shahadaalsubhi@gmail.com](mailto:shahadaalsubhi@gmail.com)
