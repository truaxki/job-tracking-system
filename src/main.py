from pdf_processor import PDFProcessor
from knowledge_graph_parser import KnowledgeGraphParser

def process_resume(pdf_path: str, save_images: bool = False):
    """Process a resume PDF and create a knowledge graph"""
    try:
        # Initialize processors
        pdf_processor = PDFProcessor()
        graph_parser = KnowledgeGraphParser()
        
        # Process PDF to XML
        print("\nProcessing PDF...")
        xml_results = pdf_processor.process_pdf(pdf_path, save_images)
        
        # Process each page
        all_entities = []
        all_relations = []
        
        for i, xml_content in enumerate(xml_results, 1):
            print(f"\nAnalyzing page {i}...")
            
            # Create knowledge graph
            entities, relations = graph_parser.create_knowledge_graph(xml_content)
            
            # Accumulate results
            all_entities.extend(entities)
            all_relations.extend(relations)
        
        # Print results
        print("\nExtracted Entities:")
        for entity in all_entities:
            print(entity)
        
        print("\nExtracted Relations:")
        for relation in all_relations:
            print(relation)
        
        return all_entities, all_relations
        
    except Exception as e:
        print(f'Error processing resume: {e}')
        raise

def main():
    # Example usage
    pdf_path = r'C:\Users\ktrua\anthropic_test\temp files\20241106 Kirk Truax Palantir.pdf'
    
    try:
        entities, relations = process_resume(pdf_path, save_images=True)
        
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == '__main__':
    main()