import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

class PolicyAgent:
    def __init__(self, data_path="./data"):
        # Load your PoliSci data (PDFs)
        loader = PyPDFDirectoryLoader(data_path)
        docs = loader.load()
        
        # Create the 'Brain' using embeddings
        vectorstore = Chroma.from_documents(
            documents=docs, 
            embedding=OpenAIEmbeddings()
        )
        
        # Set up the Agent logic
        self.llm = ChatOpenAI(model_name="gpt-4o", temperature=0.2)
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm, 
            retriever=vectorstore.as_retriever()
        )

    def run(self, query):
        return self.chain.invoke(query)
