import re
from typing import Dict, List, Optional

class XMLProcessor:
    def __init__(self):
        self.xml_tag_pattern = re.compile(r'<([a-zA-Z][a-zA-Z0-9-_]*)[>\s]')
        self.closing_tag_pattern = re.compile(r'</[a-zA-Z][a-zA-Z0-9-_]*>\s*$', re.MULTILINE)
        self.nested_tag_pattern = re.compile(r'<([\w-]+)>([\s\S]*?)</\1>')

    def extract_xml_from_text(self, content: str) -> Optional[str]:
        """Extract XML content from text using regex patterns.

        Args:
            content (str): Text that may contain XML

        Returns:
            Optional[str]: Extracted XML content or None if no valid XML found
        """
        # Find first valid XML tag
        first_match = self.xml_tag_pattern.search(content)
        if not first_match:
            return None

        # Find last closing tag
        last_matches = list(self.closing_tag_pattern.finditer(content))
        if not last_matches:
            return None

        # Extract content between first and last XML tags
        xml_start = first_match.start()
        xml_end = last_matches[-1].end()
        return content[xml_start:xml_end].strip()

    def extract_tags(self, content: str) -> List[Dict]:
        """Extract all XML tags and their content.

        Args:
            content (str): XML content to parse

        Returns:
            List[Dict]: List of dictionaries containing tag info
        """
        tags = []
        matches = self.nested_tag_pattern.finditer(content)

        for match in matches:
            tag_name = match.group(1)
            tag_content = match.group(2).strip()

            # Check for nested tags
            nested_content = self.extract_tags(tag_content) if '<' in tag_content else None

            tags.append({
                'tag': tag_name,
                'content': tag_content if not nested_content else None,
                'nested': nested_content
            })

        return tags

    def format_tag_output(self, tags: List[Dict], indent: int = 0) -> None:
        """Print tags in a readable hierarchical format.

        Args:
            tags (List[Dict]): List of tag dictionaries
            indent (int): Current indentation level
        """
        for tag in tags:
            print(f"{'  ' * indent}<{tag['tag']}>")
            if tag['nested']:
                self.format_tag_output(tag['nested'], indent + 1)
            elif tag['content']:
                print(f"{'  ' * (indent + 1)}{tag['content']}")
            print(f"{'  ' * indent}</{tag['tag']}>")

    def process_file(self, file_path: str) -> None:
        """Process a file containing XML content.

        Args:
            file_path (str): Path to the file to process
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            xml_content = self.extract_xml_from_text(content)
            if not xml_content:
                print("No valid XML content found in file")
                return

            print("\nExtracting XML structure:")
            print("=" * 80)
            
            tags = self.extract_tags(xml_content)
            self.format_tag_output(tags)
            
            print("=" * 80)

        except Exception as e:
            print(f"Error processing file: {e}")

def main():
    processor = XMLProcessor()
    
    # Example usage
    file_path = r'C:\Users\ktrua\anthropic_test\job-tracking-system\llama_outputs\llama_output_20241213_121121.txt'
    processor.process_file(file_path)

if __name__ == '__main__':
    main()