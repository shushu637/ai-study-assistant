import streamlit as st
import re

st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="centered")
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with st.sidebar:
    st.header("How to use")
    st.write("1. Pick your subject")
    st.write("2. Type a concept")
    st.write("3. Click Explain")
    st.write("4. Read the explanation")
    st.write("5. Take the quiz")
    st.markdown("---")
    st.write("Built with Python + Streamlit + Groq")

st.title("AI Study Assistant")
st.write("Learn any CS concept — explained simply, then tested.")

subject = st.selectbox(
    "Choose a subject:",
    [
        "Deep Learning",
        "Machine Learning",
        "Computer Vision",
        "Data Structures & Algorithms",
        "Programming in AI",
        "Computer Graphics",
        "General CS",
    ],
)

concept = st.text_input(
    "What concept do you want to learn?",
    placeholder="e.g. backpropagation, binary trees",
)


def parse_quiz(quiz_text):
    """Parse quiz text into structured list of questions."""
    questions = []
    # Split into blocks by Q1:, Q2:, Q3:
    blocks = re.split(r"\n?Q\d+:", quiz_text)
    blocks = [b.strip() for b in blocks if b.strip()]

    for block in blocks:
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue

        question = lines[0]
        options = {}
        answer = None

        for line in lines[1:]:
            m = re.match(r"^([A-D])[).]\s+(.*)", line)
            if m:
                options[m.group(1)] = m.group(2)
            elif line.startswith("Answer:"):
                answer = line.replace("Answer:", "").strip().upper()
                if answer and len(answer) > 1:
                    answer = answer[0]

        if question and len(options) == 4 and answer:
            questions.append(
                {"question": question, "options": options, "answer": answer}
            )

    return questions


if st.button("Explain it to me"):
    if concept:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a CS tutor for {subject}. Explain: 1) Simple analogy, 2) Definition, 3) How it works, 4) Why it matters.",
                    },
                    {"role": "user", "content": f"Explain: {concept}"},
                ],
            )
            explanation = response.choices[0].message.content
            st.session_state["explanation"] = explanation

            quiz_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Generate exactly 3 multiple choice questions. "
                            "Format EXACTLY like this, each on its own line:\n\n"
                            "Q1: [question text]\n"
                            "A) [option]\n"
                            "B) [option]\n"
                            "C) [option]\n"
                            "D) [option]\n"
                            "Answer: [correct letter only, e.g. A]\n\n"
                            "Q2: ...\n\n"
                            "CRITICAL: Each question and each option MUST be on its own separate line. "
                            "Never put options on the same line as the question. "
                            "Do not reveal the answer in the options."
                        ),
                    },
                    {"role": "user", "content": f"Quiz about: {concept} in {subject}"},
                ],
            )
            quiz_text = quiz_response.choices[0].message.content
            questions = parse_quiz(quiz_text)
            st.session_state["questions"] = questions
            st.session_state["answers"] = {}
            st.session_state["submitted"] = False
    else:
        st.warning("Please enter a concept first.")

# Show explanation
if "explanation" in st.session_state:
    st.markdown("### Explanation")
    st.write(st.session_state["explanation"])
    st.markdown("---")

# Show interactive quiz
if "questions" in st.session_state and st.session_state["questions"]:
    st.markdown("### Quick Quiz")
    st.write("Select your answers, then click Submit:")

    questions = st.session_state["questions"]

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        options_list = [f"{k}) {v}" for k, v in q["options"].items()]
        choice = st.radio(
            label=f"q{i}",
            options=options_list,
            index=None,
            label_visibility="collapsed",
            key=f"radio_{i}",
        )
        if choice:
            st.session_state["answers"][i] = choice[0]  # just the letter
        st.markdown("")

    if st.button("Submit Answers"):
        st.session_state["submitted"] = True

    if st.session_state.get("submitted"):
        st.markdown("### Results")
        score = 0
        for i, q in enumerate(questions):
            user_ans = st.session_state["answers"].get(i)
            correct = q["answer"]
            if user_ans == correct:
                st.success(f"Q{i+1}: ✅ Correct! (Answer: {correct})")
                score += 1
            elif user_ans:
                st.error(
                    f"Q{i+1}: ❌ You chose {user_ans}, correct answer is {correct}"
                )
            else:
                st.warning(f"Q{i+1}: ⚠️ Not answered — correct answer is {correct}")

        st.markdown(f"### Score: {score} / {len(questions)}")
        if score == len(questions):
            st.balloons()
            st.success("Perfect score! 🎉")
        elif score >= 2:
            st.info("Good job! Almost there.")
        else:
            st.warning("Keep studying — you'll get it!")
