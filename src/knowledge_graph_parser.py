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
        """Save LLaMA prompt and response to a timestamped file.
        
        Args:
            prompt (str): The prompt sent to LLaMA
            response (str): LLaMA's response
            
        Returns:
            str: Path to the saved file
        """
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

    # ... [rest of the class remains the same] ...
