from langchain_core.prompts import PromptTemplate

gap_analysis_prompt = PromptTemplate.from_template("""
You are an expert resume reviewer and career coach.
Carefully analyze the resume against the job description provided.

Resume:
{resume_context}

Job Description:
{jd_context}

Return ONLY valid JSON with this exact structure:
{{
  "match_score": <integer 0-100>,
  "missing_skills": ["skill1", "skill2"],
  "weak_sections": ["section1", "section2"],
  "suggestions": ["suggestion1", "suggestion2"]
}}
""")
