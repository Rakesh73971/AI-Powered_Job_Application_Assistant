from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

gap_analysis_prompt = PromptTemplate.from_template("""
You are a resume expert. Analyze the resume against the job description.

Resume: {resume_context}
Job Description: {jd_context}

Return ONLY valid JSON:
{{
  "match_score": <0-100>,
  "missing_skills": ["skill1", "skill2"],
  "weak_sections": ["section1"],
  "suggestions": ["suggestion1"]
}}
""")

cover_letter_prompt = PromptTemplate.from_template("""
Write a {tone} cover letter based on:
Resume: {resume_context}
Job Description: {jd_context}
Return only the cover letter text.
""")

gap_chain = gap_analysis_prompt | llm | JsonOutputParser()
cover_chain = cover_letter_prompt | llm