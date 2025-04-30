from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List, Dict, Any

class VectorStore:
    """Class to manage vector embeddings and similarity search"""
    
    def __init__(self, examples: List[Dict[str, str]], model_name: str = 'sentence-transformers/all-miniLM-l6-v2'):
        """
        Initialize vector store with examples
        
        Args:
            examples: List of example dictionaries with 'question' and 'sql_query' keys
            model_name: Name of the HuggingFace embeddings model to use
        """
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
            
            # Prepare texts and metadata
            texts = []
            metadatas = []
            
            for example in examples:
                texts.append(example['question'])
                metadatas.append({
                    'question': example['question'],
                    'sql_query': example['sql_query']
                })
            
            # Create vector store
            self.vectorstore = FAISS.from_texts(texts=texts, embedding=self.embeddings, metadatas=metadatas)
        except Exception as e:
            raise Exception(f"Failed to initialize vector store: {str(e)}")
    
    def find_similar_examples(self, question: str, k: int = 2) -> List[Dict[str, str]]:
        """
        Find similar examples to a question
        
        Args:
            question: Question to find similar examples for
            k: Number of examples to return
            
        Returns:
            List[Dict]: List of similar examples with 'question' and 'sql_query' keys
        """
        try:
            results = self.vectorstore.similarity_search(question, k=k)
            examples = []
            
            for doc in results:
                examples.append({
                    'question': doc.metadata['question'],
                    'sql_query': doc.metadata['sql_query']
                })
            
            return examples
        except Exception as e:
            raise Exception(f"Similarity search failed: {str(e)}")