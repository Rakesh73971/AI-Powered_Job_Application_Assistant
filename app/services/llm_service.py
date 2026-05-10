from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from app.core.config import settings

# Main LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.google_api_key,
    temperature=0.3
)

streaming_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.google_api_key,
    temperature=0.7,
    streaming=True
)

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

cover_letter_prompt = PromptTemplate.from_template("""
You are a professional cover letter writer.
Write a {tone} cover letter tailored to this specific job opportunity.

Resume:
{resume_context}

Job Description:
{jd_context}

Write a compelling personalized cover letter.
Return only the cover letter text.
""")

gap_chain = gap_analysis_prompt | llm | JsonOutputParser()

cover_chain = cover_letter_prompt | streaming_llm | StrOutputParser()

generate_cover_letter_chain = cover_letter_prompt | llm | StrOutputParser()