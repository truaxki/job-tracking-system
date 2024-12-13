from xml_extractor import XMLExtractor, clean_llama_output

def test_xml_extraction(xml_content: str):
    extractor = XMLExtractor()
    print("\nExtracting XML tags...")
    tags = extractor.extract_all_tags(xml_content)
    
    print("\nFound XML Structure:")
    print("=" * 80)
    extractor.print_tag_structure(tags)
    print("=" * 80)

def main():
    # Test with LLaMA output file
    file_path = r'C:\Users\ktrua\anthropic_test\job-tracking-system\llama_outputs\llama_output_20241213_120645.txt'
    
    # Clean and extract XML content from LLaMA output
    xml_content = clean_llama_output(file_path)
    
    # Test extraction
    test_xml_extraction(xml_content)

if __name__ == '__main__':
    main()