from langchain_core.prompts import PromptTemplate

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
