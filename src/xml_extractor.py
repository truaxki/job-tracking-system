import re
from typing import Dict, List, Tuple

class XMLExtractor:
    def __init__(self):
        self.tag_pattern = r'<([^/>]+)>([^<]*)</\1>|<([^/>]+)/>'

    def extract_all_tags(self, content: str) -> List[Dict]:
        """Extract all XML tags and their content from text.
        
        Args:
            content (str): Text containing XML tags
            
        Returns:
            List[Dict]: List of dictionaries containing tag names and their content
        """
        tags = []
        # First clean up newlines and extra spaces to make parsing easier
        content = ' '.join(content.split())
        
        # Find all tags with their content
        matches = re.finditer(self.tag_pattern, content)
        for match in matches:
            if match.group(1) and match.group(2):  # Full tag with content
                tags.append({
                    'tag': match.group(1).strip(),
                    'content': match.group(2).strip()
                })
            elif match.group(3):  # Self-closing tag
                tags.append({
                    'tag': match.group(3).strip(),
                    'content': None
                })

        return tags

    def extract_nested_tags(self, content: str) -> Dict:
        """Extract nested XML structure.
        
        Args:
            content (str): Text containing XML tags
            
        Returns:
            Dict: Nested dictionary representing XML structure
        """
        def find_matching_end_tag(text: str, start_pos: int, tag: str) -> int:
            """Find the matching end tag position."""
            count = 1
            pos = start_pos
            while count > 0 and pos < len(text):
                next_start = text.find(f'<{tag}>', pos + 1)
                next_end = text.find(f'</{tag}>', pos + 1)
                
                if next_start == -1:
                    next_start = len(text)
                if next_end == -1:
                    next_end = len(text)
                    
                if next_start < next_end and next_start != len(text):
                    count += 1
                    pos = next_start
                else:
                    count -= 1
                    pos = next_end
            return pos

        result = {}
        current_pos = 0
        
        while True:
            # Find next tag start
            tag_start = content.find('<', current_pos)
            if tag_start == -1:
                break
                
            # Find tag name
            tag_end = content.find('>', tag_start)
            if tag_end == -1:
                break
                
            tag_name = content[tag_start + 1:tag_end].strip()
            if tag_name.startswith('/'):
                current_pos = tag_end + 1
                continue
                
            # Find matching end tag
            content_start = tag_end + 1
            content_end = find_matching_end_tag(content, content_start, tag_name)
            
            if content_end == -1:
                break
                
            # Extract content
            tag_content = content[content_start:content_end].strip()
            
            # Add to result
            if tag_name not in result:
                result[tag_name] = []
            result[tag_name].append(tag_content)
            
            current_pos = content_end + len(tag_name) + 3  # +3 for </>
            
        return result

    def print_extracted_tags(self, tags: List[Dict]):
        """Print extracted tags in a readable format."""
        print("\nExtracted XML Tags:")
        print("-" * 40)
        for item in tags:
            print(f"Tag: {item['tag']}")
            if item['content']:
                print(f"Content: {item['content']}")
            print("-" * 40)

    def print_nested_structure(self, structure: Dict, indent: int = 0):
        """Print nested XML structure in a readable format."""
        for tag, contents in structure.items():
            print("  " * indent + f"Tag: {tag}")
            for content in contents:
                if '<' in content:  # Has nested tags
                    print("  " * (indent + 1) + "Nested content:")
                    nested = self.extract_nested_tags(content)
                    self.print_nested_structure(nested, indent + 2)
                else:
                    print("  " * (indent + 1) + f"Content: {content}")

def main():
    # Example usage
    test_xml = """
    <experience>
        <role>
            <company>Creating Coding Careers</company>
            <title>Software Development Apprentice</title>
            <dates>February 2024 - August 2024</dates>
        </role>
    </experience>
    """
    
    extractor = XMLExtractor()
    
    print("\nFlat tag extraction:")
    tags = extractor.extract_all_tags(test_xml)
    extractor.print_extracted_tags(tags)
    
    print("\nNested structure extraction:")
    nested = extractor.extract_nested_tags(test_xml)
    extractor.print_nested_structure(nested)

if __name__ == '__main__':
    main()