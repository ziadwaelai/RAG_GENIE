from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from docs.utils import text_splitter,embedding_function
import os
from markitdown import MarkItDown


def cv_parser(file_path):
    md = MarkItDown()
    result = md.convert(file_path)
    return result

def save_doc_to_vector_store():
    try:
        # Directory containing PDF files
        pdf_directory = os.path.join(os.path.dirname(__file__), 'pdfs')

        # List all PDF files in the directory
        pdf_files = [f for f in os.listdir(
            pdf_directory) if f.endswith('.pdf')]

        if not pdf_files:
            print("No PDF files found in the directory.")
            return None

        # Initialize an empty list to store all chunks
        all_chunks = []

        # Process each PDF file
        for pdf_file in pdf_files:
            file_path = os.path.join(pdf_directory, pdf_file)
            #loader = PyPDFLoader(file_path)
            loader = PyPDFLoader(file_path)

            # Load and split the current PDF
            docs = loader.load_and_split()

            # Extract the first line of the document (assumed to be the name)
            first_line = None
            if docs:
                first_line = docs[0].page_content.split('\n')[0].strip()

            # Include metadata for each doc
            for doc in docs:
                doc.metadata['file_name'] = pdf_file

            # Split the documents into chunks
            chunks = text_splitter.split_documents(docs)
            

            # Add the first line to each chunk
            for chunk in chunks:
                if first_line:
                    chunk.page_content = f"{first_line}\n\n{chunk.page_content}"
                    #print('/n',chunk)

            # Add chunks from this PDF to the list of all chunks
            all_chunks.extend(chunks)

        # Save all chunks to vector store
        persist_directory = os.path.join(
            os.path.dirname(__file__), os.pardir, 'db')
        """
        # Create vector store
        vector_store = Chroma.from_documents(
            documents=all_chunks,
            embedding=embedding_function,
            persist_directory=persist_directory
        )
        """
        vector_store = Chroma.from_documents(
            documents=all_chunks,
            embedding=embedding_function,  
            persist_directory=persist_directory
        )
        print("Vector store saved successfully.")
        return vector_store

        

        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
