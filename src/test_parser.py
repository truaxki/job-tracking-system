from knowledge_graph_parser import KnowledgeGraphParser

def test_parser():
    # Your actual XML output from the PDF processing
    test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<resume>
    <personalInfo>
        <name>Kirk F Truax</name>
        <title>Software Development Apprentice</title>
    </personalInfo>
    <skills>
        <technicalSkills>
            <skill name="Python" proficiency="Proficient" />
            <skill name="Java" proficiency="Proficient" />
            <skill name="SQL" proficiency="Proficient" />
        </technicalSkills>
    </skills>
    <experience>
        <position>
            <company>Creating Coding Careers</company>
            <title>Software Development Apprentice</title>
            <duration>February 2024 - August 2024</duration>
            <responsibilities>Managed the Radiation Health Department's intake and monitoring</responsibilities>
        </position>
        <position>
            <company>Navy Medicine Readiness and Training Command</company>
            <title>Radiation Health Officer</title>
            <duration>March 2022 - February 2024</duration>
        </position>
    </experience>
</resume>"""

    # Create parser instance
    parser = KnowledgeGraphParser()
    
    # Process the XML
    print("Starting parser test...")
    entities, relations = parser.create_knowledge_graph(test_xml)

if __name__ == '__main__':
    test_parser()
