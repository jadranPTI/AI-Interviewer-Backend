import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.prompts.prompts import QUESTION_GENERATION_PROMPT
from app.utils.helpers import parse_questions


def generate_questions(job_description:str, api_key: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
        google_api_key=api_key,
        temperature=0.7
    )

    prompt = PromptTemplate(
        input_variables=["job_description"],
        template=QUESTION_GENERATION_PROMPT
    )

    # New LCEL syntax — just pipe prompt into llm
    chain = prompt | llm

    
    response = chain.invoke({"job_description": job_description})
    raw_text = response.content  # .content instead of ["text"]

    return parse_questions(raw_text)















# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from app.prompts.prompts import QUESTION_GENERATION_PROMPT
# from app.utils.helpers import parse_questions


# def generate_questions(domain: str, experience: str, api_key: str) -> dict:
#     llm = ChatGoogleGenerativeAI(
#         model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
#         google_api_key=api_key,
#         temperature=0.7
#     )

#     prompt = PromptTemplate(
#         input_variables=["domain", "experience"],
#         template=QUESTION_GENERATION_PROMPT
#     )

#     # New LCEL syntax — just pipe prompt into llm
#     chain = prompt | llm

#     response = chain.invoke({"domain": domain, "experience": experience})
#     raw_text = response.content  # .content instead of ["text"]

#     return parse_questions(raw_text)






