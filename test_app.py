import pytest
from app import parse_quiz


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_quiz(q="What is X?", opts=("Option A", "Option B", "Option C", "Option D"), answer="A"):
    """Build a properly formatted quiz string for a single question."""
    return (
        f"Q1: {q}\n"
        f"A) {opts[0]}\n"
        f"B) {opts[1]}\n"
        f"C) {opts[2]}\n"
        f"D) {opts[3]}\n"
        f"Answer: {answer}\n"
    )


# ── Happy Path ────────────────────────────────────────────────────────────────

class TestParseQuizHappyPath:

    def test_parses_single_question(self):
        quiz = make_quiz()
        result = parse_quiz(quiz)
        assert len(result) == 1

    def test_parses_three_questions(self):
        quiz = (
            "Q1: What is a binary tree?\n"
            "A) A tree with one child\nB) A tree with at most two children\n"
            "C) A tree with exactly two children\nD) A tree with no children\n"
            "Answer: B\n\n"
            "Q2: What is a stack?\n"
            "A) FIFO structure\nB) LIFO structure\nC) Random access\nD) Sorted list\n"
            "Answer: B\n\n"
            "Q3: What does CPU stand for?\n"
            "A) Central Process Unit\nB) Core Processing Unit\n"
            "C) Central Processing Unit\nD) Computer Processing Unit\n"
            "Answer: C\n"
        )
        result = parse_quiz(quiz)
        assert len(result) == 3

    def test_question_text_is_correct(self):
        quiz = make_quiz(q="What is backpropagation?")
        result = parse_quiz(quiz)
        assert result[0]["question"] == "What is backpropagation?"

    def test_answer_is_correct(self):
        quiz = make_quiz(answer="C")
        result = parse_quiz(quiz)
        assert result[0]["answer"] == "C"

    def test_all_four_options_present(self):
        quiz = make_quiz(opts=("Alpha", "Beta", "Gamma", "Delta"))
        result = parse_quiz(quiz)
        assert result[0]["options"] == {"A": "Alpha", "B": "Beta", "C": "Gamma", "D": "Delta"}

    def test_answer_uppercase_normalized(self):
        """Answer letter should always be uppercase."""
        quiz = make_quiz(answer="b")
        result = parse_quiz(quiz)
        assert result[0]["answer"] == "B"

    def test_answer_with_extra_text(self):
        """Answer: B) Some text — should extract just the letter."""
        quiz = (
            "Q1: What is X?\n"
            "A) One\nB) Two\nC) Three\nD) Four\n"
            "Answer: B) Two\n"
        )
        result = parse_quiz(quiz)
        assert result[0]["answer"] == "B"


# ── Edge Cases ────────────────────────────────────────────────────────────────

class TestParseQuizEdgeCases:

    def test_empty_string_returns_empty_list(self):
        result = parse_quiz("")
        assert result == []

    def test_missing_answer_line_excluded(self):
        """Questions without an Answer: line should be excluded."""
        quiz = (
            "Q1: What is X?\n"
            "A) One\nB) Two\nC) Three\nD) Four\n"
            # No Answer: line
        )
        result = parse_quiz(quiz)
        assert len(result) == 0

    def test_missing_options_excluded(self):
        """Questions with fewer than 4 options should be excluded."""
        quiz = (
            "Q1: What is X?\n"
            "A) One\nB) Two\n"
            "Answer: A\n"
        )
        result = parse_quiz(quiz)
        assert len(result) == 0

    def test_extra_whitespace_in_answer(self):
        """Answer: ' A ' should still parse correctly."""
        quiz = (
            "Q1: What is X?\n"
            "A) One\nB) Two\nC) Three\nD) Four\n"
            "Answer:   A   \n"
        )
        result = parse_quiz(quiz)
        assert result[0]["answer"] == "A"

    def test_mixed_valid_and_invalid_questions(self):
        """Only valid questions should be returned."""
        quiz = (
            "Q1: Valid question?\n"
            "A) One\nB) Two\nC) Three\nD) Four\n"
            "Answer: A\n\n"
            "Q2: Incomplete question?\n"
            "A) Only one option\n"
            "Answer: A\n"
        )
        result = parse_quiz(quiz)
        assert len(result) == 1
        assert result[0]["question"] == "Valid question?"

    def test_does_not_crash_on_garbage_input(self):
        """Random text should not raise an exception."""
        result = parse_quiz("asdkjhaskdjh 1234 !@#$")
        assert result == []

    def test_does_not_crash_on_whitespace_only(self):
        result = parse_quiz("     \n\n\t  ")
        assert result == []
