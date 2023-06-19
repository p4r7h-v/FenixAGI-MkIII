import PyPDF2

def extract_data_from_pdf(pdf_file):
    # Open the PDF file in read-binary mode
    with open(pdf_file, 'rb') as file:        
        # Create a PDF file reader object
        pdf_reader = PyPDF2.PdfFileReader(file)

        # Check if the PDF is encrypted
        if pdf_reader.isEncrypted:
            # Try to decrypt the PDF with an empty password
            try:
                is_decrypted = pdf_reader.decrypt('')
                if not is_decrypted:
                    print("The PDF file is encrypted with a non-empty password.")
                return
            except NotImplementedError:
                print("Error: The PDF encryption is not supported.")
                return

        # Get the total number of pages in the PDF
        num_pages = pdf_reader.numPages

        # Extract the text from each page
        extracted_text = ""
        for i in range(num_pages):
            page_obj = pdf_reader.getPage(i)
            page_text = page_obj.extractText()
            extracted_text += page_text

    return extracted_text


# Example usage
pdf_file = "example.pdf"
extracted_text = extract_data_from_pdf(pdf_file)
print(extracted_text)