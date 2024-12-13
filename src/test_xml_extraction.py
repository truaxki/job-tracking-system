from xml_extractor import XMLExtractor
import re

def test_llama_output(file_path: str):
    # Read the LLaMA output file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first XML tag and last closing tag
    # Look for the first '<' that's followed by a valid XML tag name
    xml_pattern = re.compile(r'<([a-zA-Z][a-zA-Z0-9-_]*)[>\s]')
    first_match = xml_pattern.search(content)
    
    if not first_match:
        print("No valid XML tags found")
        return
        
    # Find the last closing tag
    last_tag_pattern = re.compile(r'</[a-zA-Z][a-zA-Z0-9-_]*>\s*$', re.MULTILINE)
    last_matches = list(last_tag_pattern.finditer(content))
    
    if not last_matches:
        print("No valid closing tags found")
        return
    
    # Extract content between first and last XML tags
    xml_start = first_match.start()
    xml_end = last_matches[-1].end()
    xml_content = content[xml_start:xml_end].strip()
    
    # Create extractor
    extractor = XMLExtractor()
    
    print("\n1. Flat tag extraction:")
    tags = extractor.extract_all_tags(xml_content)
    extractor.print_extracted_tags(tags)
    
    print("\n2. Nested structure extraction:")
    nested = extractor.extract_nested_tags(xml_content)
    extractor.print_nested_structure(nested)

def main():
    # Path to your LLaMA output file
    file_path = r'C:\Users\ktrua\anthropic_test\job-tracking-system\llama_outputs\llama_output_20241213_121121.txt'
    
    print("Starting XML extraction from LLaMA output...")
    test_llama_output(file_path)

if __name__ == '__main__':
    main()