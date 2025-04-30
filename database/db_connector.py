from langchain_community.utilities import SQLDatabase
import pandas as pd
from typing import Dict, List, Any, Union

class DatabaseConnector:
    """Class to handle database connections and queries"""
    
    def __init__(self, user: str, password: str, host: str, database: str):
        """
        Initialize database connector
        
        Args:
            user: Database username
            password: Database password
            host: Database host
            database: Database name
        """
        self.db_uri = f"mysql+pymysql://{user}:{password}@{host}/{database}"
        try:
            self.db = SQLDatabase.from_uri(
                self.db_uri,
                sample_rows_in_table_info=3
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")
    
    def get_schema(self) -> str:
        """
        Get database schema information
        
        Returns:
            str: Database schema information
        """
        try:
            return self.db.get_table_info()
        except Exception as e:
            raise Exception(f"Failed to get schema information: {str(e)}")
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            query: SQL query to execute
            
        Returns:
            pd.DataFrame: Query results as DataFrame
        """
        try:
            result = self.db.run(query)
            
            # Handle different result formats
            if isinstance(result, pd.DataFrame):
                return result
            elif isinstance(result, str):
                # Check if it's a string representation of a list of tuples (common SQL result format)
                if result.strip().startswith('[') and ')' in result and '(' in result:
                    try:
                        # This is a safe approach since we're only using it for display
                        # Extract values from the string representation
                        clean_result = result.strip().replace('[(', '').replace(')]', '').replace('(', '').replace(')', '')
                        values = [v.strip() for v in clean_result.split(',')]
                        
                        # Create a single-row DataFrame
                        if len(values) == 1:
                            return pd.DataFrame({'Result': values})
                        else:
                            # For multiple columns, create column names
                            columns = [f'Column {i+1}' for i in range(len(values))]
                            return pd.DataFrame([values], columns=columns)
                    except Exception:
                        # Fall back to simple DataFrame with the string result
                        return pd.DataFrame({'Result': [result]})
                
                # Try converting tabular string data
                try:
                    lines = result.strip().split('\n')
                    if len(lines) > 1:
                        headers = lines[0].split(',')
                        data = [line.split(',') for line in lines[1:]]
                        return pd.DataFrame(data, columns=headers)
                    else:
                        # Create a single-row DataFrame with the result
                        return pd.DataFrame({'Result': [result]})
                except Exception:
                    # If all else fails, return a simple DataFrame with the string
                    return pd.DataFrame({'Result': [result]})
            else:
                # For any other type (like int, float, etc.), wrap in a DataFrame
                return pd.DataFrame({'Result': [str(result)]})
            
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")