from xml_extractor import XMLExtractor

def test_llama_output(file_path: str):
    # Read the LLaMA output file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the response section
    response_section = content.split('=== Response ===')[-1].strip()
    
    # Create extractor
    extractor = XMLExtractor()
    
    print("\n1. Flat tag extraction:")
    tags = extractor.extract_all_tags(response_section)
    extractor.print_extracted_tags(tags)
    
    print("\n2. Nested structure extraction:")
    nested = extractor.extract_nested_tags(response_section)
    extractor.print_nested_structure(nested)

def main():
    # Path to your LLaMA output file
    file_path = r'C:\Users\ktrua\anthropic_test\job-tracking-system\llama_outputs\llama_output_20241213_120645.txt'
    
    print("Starting XML extraction from LLaMA output...")
    test_llama_output(file_path)

if __name__ == '__main__':
    main()