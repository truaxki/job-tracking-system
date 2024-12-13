import os
# PDFProcessor: Input: PDF file path (str) -> Output: List[str] of LLaMA responses with XML tags
from pdf_processor import PDFProcessor
# XMLProcessor: Input: LLaMA response text (str) -> Output: List[Dict] of structured tag data
from xml_processor import XMLProcessor

def process_resume(pdf_path: str, save_images: bool = False) -> None:
    """Process a resume PDF and extract structured information.

    Args:
        pdf_path (str): Path to the PDF file
        save_images (bool): Whether to save intermediate images
    """
    try:
        # Initialize processors
        pdf_processor = PDFProcessor()
        xml_processor = XMLProcessor()
        
        # Process PDF and get LLaMA output
        print("Processing PDF...")
        results = pdf_processor.process_pdf(pdf_path, save_images)
        
        # Process each page's XML content
        for i, content in enumerate(results, 1):
            print(f"\nAnalyzing page {i}:")
            xml_content = xml_processor.extract_xml_from_text(content)
            
            if xml_content:
                tags = xml_processor.extract_tags(xml_content)
                xml_processor.format_tag_output(tags)
            else:
                print("No valid XML content found in LLaMA output")
                
    except Exception as e:
        print(f'Error processing resume: {e}')

def main():
    # Example usage
    pdf_path = r'C:\Users\ktrua\anthropic_test\temp files\20241106 Kirk Truax Palantir.pdf'
    process_resume(pdf_path, save_images=True)

if __name__ == '__main__':
    main()