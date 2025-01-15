from langchain_community.document_loaders import PyPDFLoader
from markitdown import MarkItDown

def display_pdf_output(pdf_path):
    """
    Display the output of PyPDFLoader from a PDF file and append the first line to each chunk.

    Args:
        pdf_path (str): The path to the PDF file.
    """
    
    try:
        # Initialize the PyPDFLoader with the PDF file path
        loader = PyPDFLoader(pdf_path)
        
        # Load and split the document
        documents = loader.load_and_split()

        if not documents:
            print("No chunks found in the document.")
            return

        # Extract the first line from the first chunk
        first_line = documents[0].page_content.splitlines()[0] if documents[0].page_content else "Unknown"

        print(f"Number of chunks created: {len(documents)}")
        for i, doc in enumerate(documents):
            # Prepend the first line to each chunk
            doc.page_content = f"{first_line}\n\n{doc.page_content}"

            print(f"\nChunk {i + 1}:")
            print("-" * 40)
            print(doc.page_content)
            print("-" * 40)
            print(f"Metadata: {doc.metadata}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Test the function
pdf_path = "ME_CV.pdf"  # Replace with your PDF file path
display_pdf_output(pdf_path)

# Function to parse the CV file and return the text content (whatever the CV extension is)
def cv_parser(file_path):
    md = MarkItDown()
    result = md.convert(file_path)
    print("\n\n\n", result.text_content)

cv_parser(pdf_path)
