QUESTION_GENERATION_PROMPT = """
You are an expert technical interviewer.

Generate exactly 15 interview questions for a candidate with the following profile:

- Job Description: {job_description}

Generate questions in this exact format — nothing else, no extra text:

TECHNICAL:
1. [question]
2. [question]
3. [question]
4. [question]
5. [question]

BEHAVIORAL:
1. [question]
2. [question]
3. [question]
4. [question]
5. [question]

SITUATIONAL:
1. [question]
2. [question]
3. [question]
4. [question]
5. [question]

Make questions relevant to the domain and appropriate for the experience level.
"""

# Technical questions should test real knowledge.
# Behavioral questions should start with "Tell me about a time..."
# Situational questions should start with "What would you do if..."


# - Domain/Role: {domain}
# - Experience Level: {experience}

EVALUATION_PROMPT = """
You are a strict but fair interview evaluator.

Candidate Profile:
- Job Description: {job_description}

Below are the interview questions and the candidate's answers:

{qa_pairs}

Note: If any answer says "TIME_EXPIRED", that question was not answered in time — give it a score of 0.

You MUST respond with ONLY a valid JSON object.
Do NOT include any text before or after the JSON.
Do NOT use markdown, backticks, or code fences.
Start your response directly with {{ and end with }}

Use this exact JSON structure:

{{
  "overall_score": 75,
  "grade": "B+",
  "summary": "One paragraph summary of overall performance.",
  "category_scores": {{
    "technical": 70,
    "behavioral": 80,
    "situational": 75
  }},
  "strengths": [
    "Strength one",
    "Strength two",
    "Strength three"
  ],
  "improvements": [
    "Area to improve one",
    "Area to improve two",
    "Area to improve three"
  ],
  "best_practices": [
    {{"tip": "Tip title", "reason": "Why this matters"}},
    {{"tip": "Tip title", "reason": "Why this matters"}},
    {{"tip": "Tip title", "reason": "Why this matters"}}
  ],
  "question_feedback": [
    {{
      "question_id": 1,
      "question": "The question text",
      "your_answer": "What the candidate said",
      "score": 70,
      "feedback": "Specific feedback on this answer"
    }}
  ]
}}
"""


# - Domain/Role: {domain}
# - Experience Level: {experience}

TERMINATION_EVALUATION_PROMPT = """
You are a strict interview evaluator.

A candidate was taking an interview for the following role:

- Job Description: {job_description}

However, the interview was terminated early due to the following reason:
{termination_reason}

Based ONLY on this termination reason, evaluate the candidate.
Do NOT make up scores for questions that were never answered.
Give an overall score of 0 and reflect the termination in your summary.

You MUST respond with ONLY a valid JSON object.
Do NOT include any text before or after the JSON.
Do NOT use markdown, backticks, or code fences.
Start your response directly with {{ and end with }}

{{
  "overall_score": 0,
  "grade": "F",
  "summary": "Explain why the interview was terminated and what it means.",
  "category_scores": {{
    "technical": 0,
    "behavioral": 0,
    "situational": 0
  }},
  "strengths": [],
  "improvements": [
    "Do not switch tabs during an interview",
    "Always remain in fullscreen mode",
    "Do not use other applications during the interview"
  ],
  "best_practices": [
    {{"tip": "Maintain focus", "reason": "Switching tabs or apps signals dishonesty to interviewers."}}
  ],
  "question_feedback": []
}}
"""




















