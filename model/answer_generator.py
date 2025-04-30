from model.llm_service import LLMService
from typing import Any

class AnswerGenerator:
    """Class to generate natural language answers from SQL results"""
    
    def __init__(self, llm_service: LLMService):
        """
        Initialize answer generator
        
        Args:
            llm_service: LLM service instance
        """
        self.llm_service = llm_service
    
    def generate_answer(self, question: str, sql_query: str, result: Any) -> str:
        """
        Generate a natural language answer based on SQL results
        
        Args:
            question: Original natural language question
            sql_query: Executed SQL query
            result: SQL query results (as string or other format)
            
        Returns:
            str: Natural language answer
        """
        # Convert result to string if it's not already
        result_str = str(result)
        
        # Create prompt
        prompt = f"""Based on the following SQL query and its results, provide a short, direct answer to the question.
        
Question: {question}
SQL Query: {sql_query}
SQL Result: {result_str}

Short Answer (just the facts, no explanation or SQL):"""
        
        # Generate answer
        response = self.llm_service.invoke(prompt)
        return response.strip()