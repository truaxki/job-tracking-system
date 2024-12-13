import os
import xml.etree.ElementTree as ET
import ollama
from typing import Dict, List, Tuple
import re
from datetime import datetime
import json

class KnowledgeGraphParser:
    def __init__(self, model_name: str = 'llama3.2-vision'):
        self.model_name = model_name
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'llama_outputs')
        os.makedirs(self.output_dir, exist_ok=True)

    def save_llama_output(self, prompt: str, response: str) -> str:
        """Save LLaMA prompt and response to a timestamped file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'llama_output_{timestamp}.txt'
        filepath = os.path.join(self.output_dir, filename)
        
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'response': response
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=== LLaMA Output ===\n")
            f.write(f"Timestamp: {output_data['timestamp']}\n\n")
            f.write("=== Prompt ===\n")
            f.write(f"{output_data['prompt']}\n\n")
            f.write("=== Response ===\n")
            f.write(f"{output_data['response']}\n")
        
        print(f"\nLLaMA output saved to: {filepath}")
        return filepath

    def get_graph_schema(self) -> str:
        """Generate the knowledge graph schema description for LLaMA context"""
        schema = """
        Knowledge Graph Schema for Resume Analysis:

        Entities:
        1. TechnicalSkill
           - Properties: name, proficiency, yearsExperience
           - Examples: Programming languages, frameworks, tools

        2. SoftSkill
           - Properties: name, context
           - Examples: Leadership, communication, project management

        3. WorkExperience
           - Properties: company, title, duration, responsibilities
           - Includes achievements and impact metrics

        4. Project
           - Properties: name, description, technologiesUsed, impact
           - Associated with work experience or education

        5. Education
           - Properties: institution, degree, major, graduation
           - Includes relevant coursework

        Relationships:
        1. WorkExperience --requires--> TechnicalSkill
        2. WorkExperience --demonstrates--> SoftSkill
        3. Project --utilizes--> TechnicalSkill
        4. Education --teaches--> TechnicalSkill
        5. WorkExperience --includes--> Project

        Please categorize the resume information according to these entities and relationships.
        """
        return schema

    def enhance_xml_prompt(self, xml_content: str) -> str:
        """Add knowledge graph context to the XML content for better parsing"""
        schema = self.get_graph_schema()
        prompt = f"""
        Using the following knowledge graph schema:

        {schema}

        Please analyze this XML resume data and identify:
        1. Clear entity instances that match our schema
        2. Relationships between these entities
        3. Any implicit connections that should be made explicit

        Resume Data:
        {xml_content}

        Please provide your analysis in a structured format that identifies:
        1. All entities found (with their properties)
        2. All relationships between entities
        3. Any additional context or implicit connections
        """

        return prompt

    def analyze_xml_with_llama(self, xml_content: str) -> str:
        """Use LLaMA to analyze the XML content with knowledge graph context"""
        prompt = self.enhance_xml_prompt(xml_content)
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            
            content = response['message']['content']
            
            # Save the output
            self.save_llama_output(prompt, content)
            
            # Print raw LLaMA output for debugging
            print("\nRaw LLaMA Output:")
            print("-" * 80)
            print(content)
            print("-" * 80)
            
            return content
            
        except Exception as e:
            print(f'Error analyzing XML with LLaMA: {e}')
            raise

    def extract_entities_and_relations(self, llama_analysis: str) -> Tuple[List[Dict], List[Dict]]:
        """Extract entities and relations from LLaMA's analysis"""
        entities = []
        relations = []

        # Split into sections
        sections = llama_analysis.split('**')
        
        # Extract entities
        entity_section = ""
        for section in sections:
            if section.startswith("Entities and Properties:"):
                entity_section = section
                break

        # Parse entities
        entity_blocks = re.split(r'\d+\.\s+\*\*', entity_section)
        for block in entity_blocks:
            if 'Properties:' in block:
                # Extract entity name
                entity_name = block.split('Properties:')[0].strip()
                if entity_name:
                    # Extract properties and instances
                    properties = {}
                    instance_lines = block.split('Entity instance')[-1].split('\n')
                    for line in instance_lines:
                        if '+' in line:
                            key_value = line.split('+')[-1].split(':')                           
                            if len(key_value) == 2:
                                key = key_value[0].strip()
                                value = key_value[1].strip()
                                properties[key] = value

                    if properties:  # Only add if we found properties
                        entities.append({
                            'type': entity_name.strip(),
                            'properties': properties
                        })

        # Extract relations
        relation_section = ""
        for section in sections:
            if section.startswith("Relationships between Entities:"):
                relation_section = section
                break

        # Parse relations
        relation_lines = relation_section.split('\n')
        for line in relation_lines:
            if '--' in line and '->' in line:
                # Extract from, to, and relation type
                match = re.search(r'\*\*(.+?)\s+--(.+?)-->\s+(.+?)\*\*', line)
                if match:
                    from_entity, relation_type, to_entity = match.groups()
                    relations.append({
                        'from': from_entity.strip(),
                        'to': to_entity.strip(),
                        'type': relation_type.strip()
                    })

        # Print parsed results for verification
        print("\nParsed Entities:")
        for entity in entities:
            print(f"\nEntity Type: {entity['type']}")
            print("Properties:")
            for key, value in entity['properties'].items():
                print(f"  {key}: {value}")

        print("\nParsed Relations:")
        for relation in relations:
            print(f"\n{relation['from']} --{relation['type']}--> {relation['to']}")

        return entities, relations

    def create_knowledge_graph(self, xml_content: str) -> Tuple[List[Dict], List[Dict]]:
        """Create a knowledge graph from XML resume content"""
        try:
            # Get LLaMA's analysis with knowledge graph context
            analysis = self.analyze_xml_with_llama(xml_content)
            
            # Extract entities and relations
            entities, relations = self.extract_entities_and_relations(analysis)
            
            return entities, relations
            
        except Exception as e:
            print(f'Error creating knowledge graph: {e}')
            raise

def main():
    # Example usage
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <resume>
        <personalInfo>
            <name>Kirk F Truax</name>
            <title>Software Development Apprentice</title>
        </personalInfo>
        <experience>
            <position>
                <company>Creating Coding Careers</company>
                <title>Software Development Apprentice</title>
                <duration>February 2024 - August 2024</duration>
            </position>
        </experience>
    </resume>
    """
    
    parser = KnowledgeGraphParser()
    
    try:
        entities, relations = parser.create_knowledge_graph(xml_content)
        
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == '__main__':
    main()