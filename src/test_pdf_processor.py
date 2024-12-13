import os
from pdf_processor import PDFProcessor

def test_resume_parsing():
    # Path to your resume
    resume_path = r"C:\Users\ktrua\anthropic_test\temp files\20241106 Kirk Truax Palantir.pdf"
    
    # Initialize processor
    print("Initializing PDF Processor...")
    try:
        processor = PDFProcessor()
    except Exception as e:
        print(f"Error initializing processor: {e}")
        return
    
    # Process the PDF
    print(f"\nProcessing PDF: {resume_path}")
    try:
        # Create a directory for the processed files
        base_dir = os.path.dirname(resume_path)
        output_dir = os.path.join(base_dir, 'processed_resume')
        os.makedirs(output_dir, exist_ok=True)
        
        # Process PDF and save images
        results = processor.process_pdf(resume_path, save_images=True)
        
        # Print results
        print("\nProcessing Results:")
        for i, text in enumerate(results, 1):
            print(f"\nPage {i} Content:")
            print("-" * 50)
            print(text)
            print("-" * 50)
            
        print("\nProcessing completed successfully!")
        
    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == '__main__':
    print("Starting Resume Parser Test...")
    test_resume_parsing()
