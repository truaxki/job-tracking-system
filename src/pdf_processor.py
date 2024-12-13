import os
from pathlib import Path
from typing import List
import ollama
import fitz  # PyMuPDF

class PDFProcessor:
    def __init__(self, model_name: str = 'llama3.2-vision'):
        """Initialize PDF processor with Ollama model.
        
        Args:
            model_name (str): Name of the LLaMA model to use
        """
        self.model_name = model_name

    def get_structured_prompt(self) -> str:
        """Generate a detailed prompt for LLaMA to extract structured XML."""
        return """
        Analyze this resume and provide information in the following XML structure. Be precise and include all relevant details:

        <resume>
            <header>
                <name></name>
                <title></title>
                <summary></summary>
            </header>

            <skills>
                <technical>
                    <skill>
                        <name></name>
                        <proficiency>expert|advanced|intermediate|beginner</proficiency>
                        <context></context>
                    </skill>
                </technical>
                <soft>
                    <skill>
                        <name></name>
                        <demonstration></demonstration>
                    </skill>
                </soft>
            </skills>

            <experience>
                <position>
                    <company></company>
                    <title></title>
                    <duration>
                        <start></start>
                        <end></end>
                    </duration>
                    <responsibilities>
                        <item></item>
                    </responsibilities>
                    <achievements>
                        <achievement>
                            <description></description>
                            <impact></impact>
                            <technologies_used>
                                <tech></tech>
                            </technologies_used>
                        </achievement>
                    </achievements>
                </position>
            </experience>

            <education>
                <degree>
                    <level>Bachelor|Master|PhD</level>
                    <field></field>
                    <institution></institution>
                    <graduation>
                        <status>completed|ongoing|expected</status>
                        <date></date>
                    </graduation>
                    <relevantCourses>
                        <course></course>
                    </relevantCourses>
                </degree>
            </education>

            <certifications>
                <certification>
                    <name></name>
                    <issuer></issuer>
                    <date></date>
                    <status>active|expired</status>
                </certification>
            </certifications>

            <projects>
                <project>
                    <name></name>
                    <description></description>
                    <technologies>
                        <tech></tech>
                    </technologies>
                    <outcome></outcome>
                </project>
            </projects>
        </resume>

        Important guidelines:
        1. Use complete dates where available (YYYY-MM)
        2. Include specific technologies and tools mentioned
        3. Separate distinct achievements and responsibilities
        4. Add context to skills where mentioned
        5. Note relationships between skills and experiences
        6. Include measurable impacts and metrics
        7. Maintain strict XML structure
        """

    def pdf_to_images(self, pdf_path: str, output_dir: str = None) -> List[str]:
        """Convert PDF pages to images for LLaMA vision processing.
        
        Args:
            pdf_path (str): Path to PDF file
            output_dir (str, optional): Directory to save images
            
        Returns:
            List[str]: Paths to generated images
        """
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

    def process_image(self, image_path: str) -> str:
        """Process a single image through LLaMA vision.
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            str: XML-structured text from LLaMA
        """
        try:
            prompt = self.get_structured_prompt()
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
            print(f'Error processing image through LLaMA: {e}')
            raise

    def process_pdf(self, pdf_path: str, save_images: bool = False) -> List[str]:
        """Process entire PDF through the pipeline.
        
        Args:
            pdf_path (str): Path to PDF file
            save_images (bool): Whether to save intermediate images
            
        Returns:
            List[str]: Generated XML for each page
        """
        try:
            output_dir = None
            if save_images:
                output_dir = os.path.join(os.path.dirname(pdf_path), 'processed_images')

            images = self.pdf_to_images(pdf_path, output_dir)
            results = [self.process_image(img_path) for img_path in images]

            # Save LLaMA outputs
            output_dir = os.path.join(os.path.dirname(pdf_path), 'llama_outputs')
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            for i, content in enumerate(results):
                output_path = os.path.join(output_dir, f'output_page_{i+1}.xml')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)

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
        for i, xml_content in enumerate(results, 1):
            print(f'\nPage {i} XML Output:')
            print(xml_content)
    
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == '__main__':
    main()