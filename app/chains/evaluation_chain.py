import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.prompts.prompts import EVALUATION_PROMPT
from app.utils.helpers import format_qa_pairs

from app.prompts.prompts import TERMINATION_EVALUATION_PROMPT


def evaluate_interview(job_description: str, qa_pairs: list, api_key: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
        google_api_key=api_key,
        temperature=0.3
    )

    prompt = PromptTemplate(
        input_variables=["job_description", "qa_pairs"],
        template=EVALUATION_PROMPT
    )

    chain = prompt | llm

    formatted_qa = format_qa_pairs(qa_pairs)

    response = chain.invoke({
        "job_description": job_description,
        "qa_pairs": formatted_qa
    })

    raw = response.content.strip()

    # Print in terminal so you can see what Gemini returned
    print("\n=== GEMINI RAW RESPONSE ===")
    print(raw[:300])
    print("===========================\n")

    # Remove markdown code fences if Gemini adds them anyway
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    # Extract only the JSON part — find first { and last }
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]

    if not raw:
        raise ValueError("Gemini returned an empty response. Please try again.")

    return json.loads(raw)



def evaluate_terminated(job_description: str, termination_reason: str, api_key: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
        google_api_key=api_key,
        temperature=0.1
    )

    prompt = PromptTemplate(
        input_variables=["job_description", "termination_reason"],
        template=TERMINATION_EVALUATION_PROMPT
    )

    chain = prompt | llm

    response = chain.invoke({
        "job_description": job_description,
        "termination_reason": termination_reason
    })

    raw = response.content.strip()

    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]

    return json.loads(raw)












