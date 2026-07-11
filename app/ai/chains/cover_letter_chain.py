from langchain_core.output_parsers import StrOutputParser
from app.ai.llm import llm, streaming_llm
from app.ai.prompts.cover_letter import cover_letter_prompt

cover_chain = cover_letter_prompt | streaming_llm | StrOutputParser()
generate_cover_letter_chain = cover_letter_prompt | llm | StrOutputParser()
