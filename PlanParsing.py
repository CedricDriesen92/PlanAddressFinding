import os
import fitz  # PyMuPDF
import shutil

def find_and_highlight_pdfs_with_text(folder_path, search_string):
    matching_pdfs = []
    
    # Ensure folder path exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return matching_pdfs
    
    # Create output folder structure
    output_base = "Output"
    search_folder = search_string.replace(" ", "")
    output_path = os.path.join(output_base, search_folder)
    os.makedirs(output_path, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    # Normalize the search string (remove spaces and convert to lowercase)
    normalized_search = search_string.lower().replace(" ", "")
    
    for pdf_file in pdf_files:
        input_path = os.path.join(folder_path, pdf_file)
        output_file = os.path.join(output_path, pdf_file)
        
        try:
            # First copy the original file to the output directory
            shutil.copy2(input_path, output_file)
            
            # Now work with the copied file
            with fitz.open(output_file) as pdf:
                modified = False
                for page in pdf:
                    # Extract annotations (comments)
                    for annot in page.annots():
                        if annot:
                            annot_text = annot.info.get("content", "")
                            normalized_annot_text = annot_text.lower().replace(" ", "")
                            if normalized_search in normalized_annot_text:
                                # Highlight the annotation
                                rect = annot.rect
                                highlight = page.add_highlight_annot(rect)
                                highlight.update()
                                modified = True
                                if pdf_file not in matching_pdfs:
                                    matching_pdfs.append(pdf_file)
                                # Removed break statement to continue searching for more matches
                
                if modified:
                    pdf.save(output_file, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
                else:
                    # If no modifications were made, remove the copied file
                    os.remove(output_file)
                        
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            # Clean up the output file if there was an error
            if os.path.exists(output_file):
                os.remove(output_file)
    
    return matching_pdfs

def main():
    folder_path = "Input"
    search_string = "rue felix wodon"
    
    matching_files = find_and_highlight_pdfs_with_text(folder_path, search_string)
    
    if matching_files:
        print("\nPDFs containing the search string have been highlighted and saved to the Output folder:")
        for pdf in matching_files:
            print(f"- {pdf}")
    else:
        print("\nNo PDFs found containing the search string.")

if __name__ == "__main__":
    main()
