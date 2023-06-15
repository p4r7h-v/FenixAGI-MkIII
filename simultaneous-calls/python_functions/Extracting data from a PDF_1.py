import PyPDF2

def extract_data_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        # Create a PDF object and read the file
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        
        # Initialize the extracted data as an empty string
        extracted_data = ""
        
        # Iterate through the pages of the PDF
        for page_num in range(pdf_reader.getNumPages()):
            # Extract the text from the current page
            text = pdf_reader.getPage(page_num).extractText()
            extracted_data += text
    
    return extracted_data

# Example usage:
file_path = "example.pdf"
data = extract_data_from_pdf(file_path)
print(data)