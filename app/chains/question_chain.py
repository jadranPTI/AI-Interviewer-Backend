import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.prompts.prompts import QUESTION_GENERATION_PROMPT


def generate_questions(job_description: str, api_key: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=api_key,
        temperature=0.7
    )

    prompt = PromptTemplate(
        input_variables=["job_description"],
        template=QUESTION_GENERATION_PROMPT
    )

    chain = prompt | llm

    response = chain.invoke({"job_description": job_description})
    raw_text = response.content

    return parse_questions(raw_text)


def parse_questions(raw_text: str) -> dict:
    categories = {
        "Technical": [],
        "Behavioral": [],
        "Situational": []
    }

    current_category = None

    for line in raw_text.strip().split("\n"):
        line = line.strip()

        if not line:
            continue

        # Category headers detect karo
        if "TECHNICAL" in line.upper() and ":" in line and not line[0].isdigit():
            current_category = "Technical"
            continue
        elif "BEHAVIORAL" in line.upper() and ":" in line and not line[0].isdigit():
            current_category = "Behavioral"
            continue
        elif "SITUATIONAL" in line.upper() and ":" in line and not line[0].isdigit():
            current_category = "Situational"
            continue

        # Question lines detect karo
        if current_category and line[0].isdigit() and "." in line:
            # Number aur dot hata do
            question_with_tag = line.split(".", 1)[1].strip()

            # Question type detect karo
            if question_with_tag.startswith("[PROGRAMMATIC]"):
                question_text = question_with_tag.replace("[PROGRAMMATIC]", "").strip()
                q_type = "programmatic"
            elif question_with_tag.startswith("[TEXTUAL]"):
                question_text = question_with_tag.replace("[TEXTUAL]", "").strip()
                q_type = "textual"
            else:
                # Koi tag nahi — default textual
                question_text = question_with_tag
                q_type = "textual"

            if question_text:
                categories[current_category].append({
                    "question": question_text,
                    "question_type": q_type   # "textual" ya "programmatic"
                })

    return categories









