import os
from dotenv import load_dotenv
from app.chains.question_chain import generate_questions
from app.chains.evaluation_chain import evaluate_interview
from app.utils.helpers import (
    print_header,
    print_category_header,
    print_question,
    print_evaluation_report,
    get_user_input
)

# Load .env file
load_dotenv()


def run_interview():
    """
    Main function that runs the full interview in the terminal.
    Simple flow:
    1. Get job_description from user
    2. Generate 15 questions via Gemini
    3. Ask questions one by one, collect answers
    4. Send everything to AI for evaluation
    5. Print the report
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Please set your GOOGLE_API_KEY in the .env file first!")
        return

    # ── Step 1: Get user info ──────────────────────────────────────
    print_header("🤖 AI INTERVIEW BOT — Powered by Gemini + LangChain")

    print("\nWelcome! This bot will conduct a 15-question interview for you.")
    print("You'll get Technical, Behavioral, and Situational questions.\n")

    job_description = get_user_input("Enter your job description: ")

    # ── Step 2: Generate questions ─────────────────────────────────
    print(f"\n⏳ Generating questions for '{job_description}'...")
    print("   Please wait...\n")

    questions_by_category = generate_questions(job_description, api_key)

    # Verify we got questions
    total_questions = sum(len(q) for q in questions_by_category.values())
    if total_questions == 0:
        print("❌ Failed to generate questions. Please check your API key and try again.")
        return

    print(f"✅ Generated {total_questions} questions! Let's begin.\n")

    # ── Step 3: Ask questions one by one ──────────────────────────
    all_qa_pairs = []   # Will store {"category", "question", "answer"}
    question_number = 0

    for category in ["Technical", "Behavioral", "Situational"]:
        questions = questions_by_category.get(category, [])

        if not questions:
            print(f"⚠️  No {category} questions were generated. Skipping...")
            continue

        print_category_header(category, question_number)

        for question in questions:
            question_number += 1

            print_question(question_number, total_questions, category, question)

            answer = get_user_input("Your Answer: ")

            # Save Q&A pair
            all_qa_pairs.append({
                "category": category,
                "question": question,
                "answer": answer
            })

            print(f"\n✅ Answer saved! Moving to next question...\n")

    # ── Step 4: Evaluate ───────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  🔍 All questions answered! Evaluating your performance...")
    print("  Please wait...\n")

    evaluation_report = evaluate_interview(
        job_description=job_description,
        qa_pairs=all_qa_pairs,
        api_key=api_key
    )

    # ── Step 5: Print Report ───────────────────────────────────────
    print_evaluation_report(evaluation_report)

    print("\n🎉 Interview complete! Good luck with your career journey.\n")


if __name__ == "__main__":
    run_interview()