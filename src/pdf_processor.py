import os
from pathlib import Path
from typing import List
import ollama
import fitz  # PyMuPDF
from PIL import Image

class PDFProcessor:
    def __init__(self, model_name: str = 'llama3.2-vision'):
        """Initialize the PDF processor with Ollama model name.
        
        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name

    def pdf_to_images(self, pdf_path: str, output_dir: str = None) -> List[str]:
        """Convert PDF pages to images.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str, optional): Directory to save images
            
        Returns:
            List[str]: List of paths to generated images
        """
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        image_paths = []
        try:
            # Open PDF
            doc = fitz.open(pdf_path)
            
            # Convert each page
            for page_num, page in enumerate(doc):
                # Get page as image
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                
                # Save image
                img_path = os.path.join(output_dir if output_dir else os.path.dirname(pdf_path),
                                       f'page_{page_num + 1}.png')
                pix.save(img_path)
                image_paths.append(img_path)
                    
            return image_paths
            
        except Exception as e:
            print(f'Error converting PDF to images: {e}')
            raise

    def process_image(self, image_path: str, prompt: str = None) -> str:
        """Process a single image through Ollama's LLaMA model.
        
        Args:
            image_path (str): Path to the image file
            prompt (str): Optional custom prompt
            
        Returns:
            str: Generated text from the image
        """
        try:
            if prompt is None:
                prompt = """Please analyze this resume image and provide the information in the following XML format. Include all dates, skills, and experiences you can find:'

<?xml version="1.0" encoding="UTF-8"?>
<resume>
    <personalInfo>
        <name></name>
        <title></title>
        <contact></contact>
        <location></location>
    </personalInfo>
    
    <skills>
        <technicalSkills>
            <skill name="" proficiency="" yearsExperience=""/>
        </technicalSkills>
        <softSkills>
            <skill name="" context=""/>
        </softSkills>
        <domainExpertise>
            <domain name="" yearsExperience=""/>
        </domainExpertise>
    </skills>
    
    <experience>
        <position>
            <company></company>
            <title></title>
            <duration></duration>
            <responsibilities></responsibilities>
            <technologiesUsed>
                <tech name="" context=""/>
            </technologiesUsed>
            <achievements></achievements>
        </position>
    </experience>
    
    <education>
        <degree>
            <institution></institution>
            <major></major>
            <minor></minor>
            <graduation></graduation>
            <relevantCourses></relevantCourses>
        </degree>
    </education>
    
    <certifications>
        <certification>
            <name></name>
            <issuer></issuer>
            <date></date>
        </certification>
    </certifications>
</resume>

Please fill in all relevant fields based on the resume image, maintaining the XML structure."""

            # Process through Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [image_path]
                }]
            )
            
            return response['message']['content']
            
        except Exception as e:
            print(f'Error processing image through Ollama: {e}')
            raise

    def process_images(self, image_paths: List[str]) -> List[str]:
        """Process multiple images through Ollama's LLaMA model.
        
        Args:
            image_paths (List[str]): List of paths to images
            
        Returns:
            List[str]: Generated text for each image
        """
        results = []
        
        try:
            for img_path in image_paths:
                text = self.process_image(img_path)
                results.append(text)
                
            return results
            
        except Exception as e:
            print(f'Error processing images through Ollama: {e}')
            raise

    def process_pdf(self, pdf_path: str, save_images: bool = False) -> List[str]:
        """Process entire PDF through the pipeline.
        
        Args:
            pdf_path (str): Path to PDF file
            save_images (bool): Whether to save intermediate images
            
        Returns:
            List[str]: Generated text for each page
        """
        try:
            # Create output directory if saving images
            output_dir = None
            if save_images:
                output_dir = os.path.join(os.path.dirname(pdf_path), 'processed_images')

            # Convert PDF to images
            images = self.pdf_to_images(pdf_path, output_dir)

            # Process images through Ollama
            results = self.process_images(images)

            return results

        except Exception as e:
            print(f'Error processing PDF: {e}')
            raise

def main():
    # Example usage
    pdf_path = r'C:\Users\ktrua\anthropic_test\temp files\20241106 Kirk Truax Palantir.pdf'
    processor = PDFProcessor()
    
    try:
        results = processor.process_pdf(pdf_path, save_images=True)
        for i, text in enumerate(results, 1):
            print(f'\nPage {i} Content:')
            print(text)
    
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == '__main__':
    main()