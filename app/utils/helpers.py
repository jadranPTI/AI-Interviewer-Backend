def print_separator(char="=", length=60):
    print(char * length)


def print_header(text: str):
    print_separator()
    print(f"  {text}")
    print_separator()


def print_category_header(category: str, number: int):
    print(f"\n{'─' * 60}")
    print(f"  📋 {category.upper()} QUESTIONS")
    print(f"{'─' * 60}")


def print_question(question_number: int, total: int, category: str, question: str):
    print(f"\n[Question {question_number}/{total}] — {category}")
    print(f"❓ {question}")
    print()


def print_evaluation_report(report: str):
    print_separator("=", 60)
    print("  📊 INTERVIEW EVALUATION REPORT")
    print_separator("=", 60)
    print(report)
    print_separator("=", 60)


def get_user_input(prompt_text: str) -> str:
    """
    Gets input from user and makes sure it's not empty.
    """
    while True:
        answer = input(prompt_text).strip()
        if answer:
            return answer
        print("  ⚠️  Please enter an answer before continuing.\n")


def format_qa_pairs(qa_pairs: list) -> str:
    formatted = ""
    for i, qa in enumerate(qa_pairs, 1):
        formatted += f"\nQ{i} [{qa['category']}]: {qa['question']}\n"
        formatted += f"Answer: {qa['answer']}\n"
        formatted += "-" * 50 + "\n"
    return formatted



# def parse_questions(raw_text: str) -> dict:
#     categories = {
#         "Technical": [],
#         "Behavioral": [],
#         "Situational": []
#     }

#     current_category = None

#     for line in raw_text.strip().split("\n"):
#         line = line.strip()

#         if not line:
#             continue

#         if "TECHNICAL" in line.upper() and ":" in line:
#             current_category = "Technical"
#         elif "BEHAVIORAL" in line.upper() and ":" in line:
#             current_category = "Behavioral"
#         elif "SITUATIONAL" in line.upper() and ":" in line:
#             current_category = "Situational"
#         elif current_category and line[0].isdigit() and "." in line:
#             question = line.split(".", 1)[1].strip()
#             if question:
#                 categories[current_category].append(question)

#     return categories