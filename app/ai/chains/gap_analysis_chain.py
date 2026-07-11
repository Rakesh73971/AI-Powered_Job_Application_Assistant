from langchain_core.output_parsers import JsonOutputParser
from app.ai.llm import llm
from app.ai.prompts.gap_analysis import gap_analysis_prompt

gap_chain = gap_analysis_prompt | llm | JsonOutputParser()
