from transformers.pipelines import pipeline
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class IITKChatbot:
    def __init__(self):
        # Load a smaller model for better performance
        self.model = pipeline(
            "question-answering", 
            model="distilbert-base-cased-distilled-squad",
            device=-1  # Use CPU (change to 0 for GPU if available)
        )
        
        # Load sentence transformer for similarity search
        self.sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # Load and prepare data
        self.data = pd.read_csv('iitk_data.csv')
        self.embeddings = self._prepare_embeddings()
    
    def _prepare_embeddings(self):
        """Create embeddings for all content"""
        print("Preparing embeddings... (This may take a few minutes)")
        content = self.data['content'].tolist()
        return self.sentence_model.encode(content)
    
    def find_most_relevant_context(self, question, top_k=3):
        """Find the most relevant context for a question"""
        question_embedding = self.sentence_model.encode(question)
        similarities = cosine_similarity(
            [question_embedding],
            self.embeddings
        )[0]
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        contexts = []
        
        for idx in top_indices:
            contexts.append(self.data.iloc[idx]['content'])
        
        return " ".join(contexts)
    
    def answer_question(self, question):
        """Answer a question about IIT Kanpur"""
        context = self.find_most_relevant_context(question)
        print(f"[DEBUG] Retrieved context: {context[:200]}...")  # Show first 200 chars
        if not context:
            return "I couldn't find relevant information to answer your question."
        result = self.model(question=question, context=context)
        print(f"[DEBUG] Model output: {result}")
        # Handle if result is a list (batch mode)
        if isinstance(result, list) and len(result) > 0:
            result = result[0]
        if isinstance(result, dict) and 'answer' in result:
            return result['answer']
        return "Sorry, I couldn't generate a proper answer. Please try rephrasing your question."

# Example usage
if __name__ == "__main__":
    chatbot = IITKChatbot()
    while True:
        question = input("Ask me about IIT Kanpur (type 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        answer = chatbot.answer_question(question)
        print(f"Answer: {answer}\n")