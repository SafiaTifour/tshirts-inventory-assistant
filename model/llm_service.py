from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional

class LLMService:
    """Service class for interacting with the LLM API"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        """
        Initialize LLM service
        
        Args:
            api_key: API key for Google Generative AI
            model: Model name to use (default: gemini-1.5-flash)
        """
        self.api_key = api_key
        self.model = model
        try:
            self.llm = ChatGoogleGenerativeAI(model=self.model, api_key=self.api_key)
        except Exception as e:
            raise Exception(f"Failed to initialize LLM service: {str(e)}")
    
    def invoke(self, prompt: str) -> str:
        """
        Invoke the LLM with a prompt
        
        Args:
            prompt: Prompt to send to the LLM
            
        Returns:
            str: LLM response content
        """
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            raise Exception(f"LLM invocation failed: {str(e)}")