import os
from pathlib import Path
from typing import List
import ollama
import fitz  # PyMuPDF
from PIL import Image

class PDFProcessor:
    def __init__(self, model_name: str = 'llama3.2-vision'):
        """Initialize the PDF processor with Ollama model name."""
        self.model_name = model_name

    def pdf_to_images(self, pdf_path: str, output_dir: str = None) -> List[str]:
        """Convert PDF pages to images."""
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        image_paths = []
        try:
            doc = fitz.open(pdf_path)
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                img_path = os.path.join(output_dir if output_dir else os.path.dirname(pdf_path),
                                       f'page_{page_num + 1}.png')
                pix.save(img_path)
                image_paths.append(img_path)
                    
            return image_paths
            
        except Exception as e:
            print(f'Error converting PDF to images: {e}')
            raise

    def process_image(self, image_path: str, prompt: str = None) -> str:
        """Process a single image through Ollama's LLaMA model."""
        try:
            if prompt is None:
                prompt = """Please analyze this resume in detail and provide the following information in XML format:

1. All experiences (company names, titles, dates, responsibilities)
2. Education details (degrees, institutions, dates)
3. Technical skills and proficiency levels
4. Notable achievements and impact metrics
5. Certifications and dates

Format using XML tags to clearly structure the information. For example:
<experience>
    <role>
        <company>Example Corp</company>
        <title>Software Engineer</title>
        <dates>2020-2022</dates>
    </role>
</experience>

Please capture all relevant details from the resume while maintaining XML structure."""

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
        """Process multiple images through Ollama's LLaMA model."""
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
        """Process entire PDF through the pipeline."""
        try:
            output_dir = None
            if save_images:
                output_dir = os.path.join(os.path.dirname(pdf_path), 'processed_images')

            images = self.pdf_to_images(pdf_path, output_dir)
            results = self.process_images(images)
            return results

        except Exception as e:
            print(f'Error processing PDF: {e}')
            raise