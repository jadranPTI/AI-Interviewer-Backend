QUESTION_GENERATION_PROMPT = """
You are an expert technical interviewer.

Generate exactly 15 interview questions based on the following job description:

{job_description}

IMPORTANT RULES:
- Technical section must have exactly 7 questions:
  - First 2 must be TEXTUAL (theoretical/conceptual questions)
  - Last 5 must be PROGRAMMATIC (coding problems to solve)
- Behavioral section must have exactly 4 questions (all textual)
- Situational section must have exactly 4 questions (all textual)
- Behavioral questions must start with "Tell me about a time..."
- Situational questions must start with "What would you do if..."
- For PROGRAMMATIC questions, give a clear coding problem to solve
- Generate questions relevant to the job description

Generate in this EXACT format — nothing else, no extra text:

TECHNICAL:
1. [TEXTUAL] question here
2. [TEXTUAL] question here
3. [PROGRAMMATIC] coding problem here
4. [PROGRAMMATIC] coding problem here
5. [PROGRAMMATIC] coding problem here
6. [PROGRAMMATIC] coding problem here
7. [PROGRAMMATIC] coding problem here

BEHAVIORAL:
1. [TEXTUAL] question here
2. [TEXTUAL] question here
3. [TEXTUAL] question here
4. [TEXTUAL] question here

SITUATIONAL:
1. [TEXTUAL] question here
2. [TEXTUAL] question here
3. [TEXTUAL] question here
4. [TEXTUAL] question here
"""


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


TERMINATION_EVALUATION_PROMPT = """
You are a strict interview evaluator.

A candidate was taking an interview for the following role:
- Job Description: {job_description}

The interview was terminated early due to:
{termination_reason}

Give overall_score of 0 and reflect termination in summary.

You MUST respond with ONLY a valid JSON object. No markdown, no backticks.

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








