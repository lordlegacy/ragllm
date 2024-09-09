import math
from PyPDF2 import PdfReader

def chunk_text(text, chunk_size=500):
    """
    Chunks the text into smaller pieces based on the given chunk size.
    
    Parameters:
    - text (str): The input text to chunk.
    - chunk_size (int): The number of characters per chunk. Default is 500.
    
    Returns:
    - List of text chunks.
    """
    # Split the text into chunks
    text_length = len(text)
    chunks = [text[i:i+chunk_size] for i in range(0, text_length, chunk_size)]
    
    return chunks

def extract_pdf_text(pdf_file_path):
    """
    Extracts text from a PDF file.
    
    Parameters:
    - pdf_file_path (str): The path to the PDF file to extract text from.
    
    Returns:
    - str: The extracted text from the PDF.
    """
    reader = PdfReader(pdf_file_path)
    extracted_text = ""
    
    # Iterate through each page and extract text
    for page in reader.pages:
        extracted_text += page.extract_text()

    return extracted_text

def chunk_pdf(pdf_file_path, chunk_size=500):
    text = extract_pdf_text(pdf_file_path)
    chunks = chunk_text(text, chunk_size)   
    return chunks
