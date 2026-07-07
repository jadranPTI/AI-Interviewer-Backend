from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List
import os
from dotenv import load_dotenv

from app.chains.question_chain import generate_questions
from app.chains.evaluation_chain import evaluate_interview, evaluate_terminated

load_dotenv()

app = FastAPI(
    title="AI Interview Coach API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# =========================
# Request Models
# =========================

class GenerateQuestionsRequest(BaseModel):
    job_description: str

    @field_validator("job_description")
    @classmethod
    def must_not_be_empty(cls, value, info):
        if not value.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return value.strip()


class QAPair(BaseModel):
    category: str
    question: str
    answer: str


class EvaluateInterviewRequest(BaseModel):
    job_description: str
    qa_pairs: List[QAPair]

    @field_validator("qa_pairs")
    @classmethod
    def must_have_answers(cls, value):
        if not value:
            raise ValueError("qa_pairs cannot be empty")
        return value


class EvaluateTerminatedRequest(BaseModel):
    job_description: str
    termination_reason: str


# =========================
# Health Check
# =========================

@app.get("/")
def home():
    return {"message": "Welcome to the AI Interview Coach API."}


@app.get("/health")
def health():
    return {"status": "healthy"}


# =========================
# Generate Questions
# =========================

@app.post("/generate-questions")
def generate_questions_api(request: GenerateQuestionsRequest):

    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=400, detail="Google API key not configured on server.")

    try:
        questions = generate_questions(
            job_description=request.job_description,
            api_key=GOOGLE_API_KEY
        )

        total = sum(len(q) for q in questions.values())

        if total == 0:
            raise HTTPException(status_code=400, detail="Failed to generate questions. Please try again.")

        return {
            "success": True,
            "job_description": request.job_description,
            "total_questions": total,
            "questions": questions
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Question generation failed: {str(e)}")


# =============================
# Evaluate Completed Interview
# =============================

@app.post("/evaluate")
def evaluate_interview_api(request: EvaluateInterviewRequest):

    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=400, detail="Google API key not configured on server.")

    try:
        report = evaluate_interview(
            job_description=request.job_description,
            qa_pairs=[qa.model_dump() for qa in request.qa_pairs],
            api_key=GOOGLE_API_KEY
        )

        return {
            "success": True,
            "job_description": request.job_description,
            "total_answered": len(request.qa_pairs),
            "evaluation_report": report
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Evaluation failed: {str(e)}")


# ==============================
# Evaluate Terminated Interview
# ==============================

@app.post("/evaluate-terminated")
def evaluate_terminated_api(request: EvaluateTerminatedRequest):

    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=400, detail="Google API key not configured.")

    try:
        report = evaluate_terminated(
            job_description=request.job_description,
            termination_reason=request.termination_reason,
            api_key=GOOGLE_API_KEY
        )
        return {
            "success": True,
            "evaluation_report": report
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Evaluation failed: {str(e)}")

