import os
import xml.etree.ElementTree as ET
import ollama
from typing import Dict, List, Tuple
import re

class KnowledgeGraphParser:
    def __init__(self, model_name: str = 'llama3.2-vision'):
        self.model_name = model_name

    # ... [previous methods remain the same] ...

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

    # ... [rest of the class remains the same] ...
