import os
from pathlib import Path
from typing import List
import requests
import json

import fitz  # PyMuPDF
from PIL import Image
import base64
from io import BytesIO

class PDFProcessor:
    def __init__(self, ollama_url: str = 'http://localhost:11434'):
        """Initialize the PDF processor with Ollama URL.
        
        Args:
            ollama_url (str): URL of the Ollama service
        """
        self.ollama_url = ollama_url

    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def pdf_to_images(self, pdf_path: str, output_dir: str = None) -> List[Path]:
        """Convert PDF pages to images.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str, optional): Directory to save images
            
        Returns:
            List[Path]: List of paths to generated images
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
                
                # Convert to PIL Image
                img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                
                # Save image if output_dir provided
                if output_dir:
                    img_path = Path(output_dir) / f'page_{page_num + 1}.png'
                    img.save(img_path)
                    image_paths.append(img_path)
                else:
                    # Store in memory
                    img_path = img  # Store PIL Image object directly
                    image_paths.append(img_path)
                    
            return image_paths
            
        except Exception as e:
            print(f'Error converting PDF to images: {e}')
            raise

    def process_image_with_ollama(self, image: Image.Image) -> str:
        """Process a single image through Ollama's LLaMA model.
        
        Args:
            image (PIL.Image): Image to process
            
        Returns:
            str: Generated text from the image
        """
        try:
            # Convert image to base64
            base64_image = self.image_to_base64(image)
            
            # Prepare the request to Ollama
            endpoint = f"{self.ollama_url}/api/generate"
            payload = {
                "model": "llama2-32k",  # or whichever model version you're using
                "prompt": "Please analyze this resume image and provide a detailed summary:",
                "stream": False,
                "images": [base64_image]
            }
            
            # Make the request
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            return result.get('response', '')
            
        except Exception as e:
            print(f'Error processing image through Ollama: {e}')
            raise

    def process_images(self, image_paths: List[Path]) -> List[str]:
        """Process images through Ollama's LLaMA model.
        
        Args:
            image_paths (List[Path]): List of paths to images or PIL Image objects
            
        Returns:
            List[str]: Generated text for each image
        """
        results = []
        
        try:
            for img in image_paths:
                if isinstance(img, Path):
                    # Load image from path
                    image = Image.open(img)
                else:
                    # Use PIL Image directly
                    image = img
                    
                # Process through Ollama
                text = self.process_image_with_ollama(image)
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
    pdf_path = 'path/to/your/resume.pdf'
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