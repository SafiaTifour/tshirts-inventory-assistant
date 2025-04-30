import streamlit as st
import pandas as pd
from config.settings import load_settings
from database.db_connector import DatabaseConnector
from model.llm_service import LLMService
from model.vector_store import VectorStore
from model.query_generator import QueryGenerator
from model.answer_generator import AnswerGenerator

def main():
    # App title and description
    st.title("AtliQ T-Shirts SQL Assistant")
    st.markdown("""
    This app lets you query the AtliQ T-Shirts database using natural language.
    Simply type your question about inventory, sales, or products, and get the answer!
    """)
    
    # Load settings
    settings = load_settings()
    
    # Initialize components
    try:
        # Database connection
        db_connector = DatabaseConnector(
            user=settings['database']['user'],
            password=settings['database']['password'],
            host=settings['database']['host'],
            database=settings['database']['name']
        )
        
        # Initialize LLM service
        llm_service = LLMService(api_key=settings['api']['key'])
        
        # Initialize vector store with examples
        vector_store = VectorStore(settings['examples'])
        
        # Initialize generators
        query_generator = QueryGenerator(llm_service, vector_store, db_connector)
        answer_generator = AnswerGenerator(llm_service)
        
        # User input
        user_question = st.text_input("Enter your question about t-shirts inventory:", 
                                    placeholder="E.g., How many white Levi's t-shirts do we have?")
        
        if user_question:
            with st.spinner("Processing your question..."):
                # Show similar examples if available
                st.subheader("Similar Examples")
                similar_examples = vector_store.find_similar_examples(user_question, k=2)
                
                for i, example in enumerate(similar_examples):
                    with st.expander(f"Example {i+1}: {example['question']}"):
                        st.code(example['sql_query'], language="sql")
                
                # Generate and execute SQL query
                try:
                    schema = db_connector.get_schema()
                    sql_query = query_generator.generate_sql_query(schema, user_question)
                    
                    # Display the SQL query
                    st.subheader("Generated SQL Query")
                    st.code(sql_query, language="sql")
                    
                    # Execute query and show results
                    result = db_connector.execute_query(sql_query)
                    st.subheader("Query Results")
                    st.dataframe(result)
                    
                    # Generate natural language answer
                    answer = answer_generator.generate_answer(user_question, sql_query, result)
                    st.subheader("Answer")
                    st.success(answer)
                    
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
        
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.warning("Please check your configuration settings in config.yaml")

if __name__ == "__main__":
    main()