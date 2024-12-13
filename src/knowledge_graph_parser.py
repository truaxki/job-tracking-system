import os
import xml.etree.ElementTree as ET
import ollama
from typing import Dict, List, Tuple

class KnowledgeGraphParser:
    def __init__(self, model_name: str = 'llama3.2-vision'):
        self.model_name = model_name
        
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
            
            return response['message']['content']
            
        except Exception as e:
            print(f'Error analyzing XML with LLaMA: {e}')
            raise

    def extract_entities_and_relations(self, llama_analysis: str) -> Tuple[List[Dict], List[Dict]]:
        """Extract entities and relations from LLaMA's analysis"""
        # This is a placeholder - we'll need to implement proper parsing of LLaMA's output
        entities = []
        relations = []
        
        # Here we'll add logic to parse LLaMA's output into structured entities and relations
        # For now, returning empty lists
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
        <!-- Example XML content here -->
    </resume>
    """
    
    parser = KnowledgeGraphParser()
    
    try:
        entities, relations = parser.create_knowledge_graph(xml_content)
        print("\nExtracted Entities:")
        for entity in entities:
            print(entity)
        
        print("\nExtracted Relations:")
        for relation in relations:
            print(relation)
    
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == '__main__':
    main()