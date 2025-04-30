import re
from typing import List, Dict, Any
from model.llm_service import LLMService
from model.vector_store import VectorStore
from database.db_connector import DatabaseConnector

class QueryGenerator:
    """Class to generate SQL queries from natural language questions"""
    
    def __init__(self, llm_service: LLMService, vector_store: VectorStore, db_connector: DatabaseConnector):
        """
        Initialize query generator
        
        Args:
            llm_service: LLM service instance
            vector_store: Vector store instance
            db_connector: Database connector instance
        """
        self.llm_service = llm_service
        self.vector_store = vector_store
        self.db_connector = db_connector
    
    def clean_sql_query(self, sql_query: str) -> str:
        """
        Remove any markdown formatting or code blocks from the SQL query
        
        Args:
            sql_query: SQL query string potentially with markdown
            
        Returns:
            str: Cleaned SQL query
        """
        # Remove ```sql and ``` patterns
        clean_query = re.sub(r'```sql|```', '', sql_query)
        # Remove any additional markdown formatting
        clean_query = re.sub(r'SQLQuery:|SQL Query:', '', clean_query)
        # Strip whitespace
        clean_query = clean_query.strip()
        return clean_query
    
    def generate_sql_query(self, schema: str, question: str) -> str:
        """
        Generate SQL query from natural language question
        
        Args:
            schema: Database schema information
            question: Natural language question
            
        Returns:
            str: Generated SQL query
        """
        # Get similar examples
        similar_examples = self.vector_store.find_similar_examples(question, k=2)
        
        # Format examples as text
        examples_text = ""
        for i, example in enumerate(similar_examples):
            examples_text += f"Example {i+1}:\nQuestion: {example['question']}\nSQL: {example['sql_query']}\n\n"
        
        # Create prompt
        prompt = f"""You are a MySQL expert. Given the question and schema below, write ONLY a MySQL query with no explanations.
        
Here are some examples of questions and their correct SQL queries:

{examples_text}

Schema:
{schema}

Question: {question}

SQL Query (write ONLY the exact MySQL query with no markdown, no code blocks, no explanation):"""
        
        # Generate query
        response = self.llm_service.invoke(prompt)
        sql_query = self.clean_sql_query(response)
        return sql_query