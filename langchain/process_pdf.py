from PyPDF2 import PdfReader

def chunk_pdf(pdf_file_path, chunk_size=500):
    reader = PdfReader(pdf_file_path)
    extracted_text = ""
    
    # Extract text from all pages
    for page in reader.pages:
        extracted_text += page.extract_text()

    # Split text into chunks
    text_length = len(extracted_text)
    chunks = [extracted_text[i:i + chunk_size] for i in range(0, text_length, chunk_size)]
    
    return chunks
