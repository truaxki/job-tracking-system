import re
from typing import Dict, List, Tuple

class XMLExtractor:
    def __init__(self):
        # Updated pattern to handle multiline content
        self.tag_pattern = re.compile(r'<([\w-]+)>([\s\S]*?)</\1>')

    def extract_all_tags(self, content: str) -> List[Dict]:
        """Extract all XML tags and their content from text."""
        tags = []
        
        # Find outermost tags first
        matches = self.tag_pattern.finditer(content)
        for match in matches:
            tag_name = match.group(1)
            tag_content = match.group(2).strip()
            
            # Add the main tag
            tags.append({
                'tag': tag_name,
                'content': tag_content,
                'nested': self.extract_nested_content(tag_content)
            })
            
        return tags

    def extract_nested_content(self, content: str) -> List[Dict]:
        """Extract nested tags from content."""
        nested_tags = []
        matches = self.tag_pattern.finditer(content)
        
        for match in matches:
            tag_name = match.group(1)
            tag_content = match.group(2).strip()
            
            nested_tags.append({
                'tag': tag_name,
                'content': tag_content,
                'nested': self.extract_nested_content(tag_content)
            })
            
        return nested_tags

    def print_tag_structure(self, tags: List[Dict], indent: int = 0):
        """Print tags in a hierarchical structure."""
        for tag in tags:
            print(f"{'  ' * indent}<{tag['tag']}>")
            if tag['content']:
                # Check if content has nested tags
                if tag['nested']:
                    self.print_tag_structure(tag['nested'], indent + 1)
                else:
                    print(f"{'  ' * (indent + 1)}{tag['content']}")
            print(f"{'  ' * indent}</{tag['tag']}>")

def clean_llama_output(file_path: str) -> str:
    """Extract the XML content from LLaMA output file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract content between Resume Data: and Please provide
    start_marker = "Resume Data:"
    end_marker = "Please provide"
    
    start_idx = content.find(start_marker)
    if start_idx != -1:
        start_idx = content.find('\n', start_idx) + 1
    
    end_idx = content.find(end_marker)
    if end_idx == -1:
        end_idx = None
    
    xml_content = content[start_idx:end_idx].strip()
    return xml_content

def main():
    # Example usage with one of your provided XML snippets
    test_xml = """
    <experience>
        <role>
            <company>Oregon State University</company>
            <title>Laboratory Technician</title>
            <dates>May 2017 - March 2018</dates>
            <responsibilities>
                Modeled spent fuel dry cask storage imaging via muon tomography to support nuclear non-proliferation research.
                Assembled a NaI Scintillation Detector system for model verification.
            </responsibilities>
        </role>
    </experience>
    """
    
    extractor = XMLExtractor()
    print("\nExtracting XML structure:")
    tags = extractor.extract_all_tags(test_xml)
    print("\nPrinting hierarchical structure:")
    extractor.print_tag_structure(tags)

if __name__ == '__main__':
    main()