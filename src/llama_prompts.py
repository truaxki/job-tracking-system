def get_resume_xml_prompt() -> str:
    """Get the structured XML prompt for resume analysis."""
    return """
Analyze this resume and extract information in the following XML structure. Keep the XML structure EXACTLY as shown, filling in the appropriate information:

<resume>
    <identity>
        <name></name>
        <currentTitle></currentTitle>
        <location></location>
        <clearance></clearance>
    </identity>

    <skills>
        <technical>
            <skill name="" level="" context=""/>
        </technical>
        <domain>
            <expertise name="" years="" context=""/>
        </domain>
        <soft>
            <skill name="" demonstrated_at=""/>
        </soft>
    </skills>

    <experience>
        <position>
            <company></company>
            <title></title>
            <duration>
                <start></start>
                <end></end>
            </duration>
            <highlights>
                <item impact="" metrics=""></item>
            </highlights>
            <skills_used>
                <skill name="" context=""/>
            </skills_used>
        </position>
    </experience>

    <education>
        <degree>
            <type></type>
            <field></field>
            <institution></institution>
            <completion></completion>
            <thesis_topic></thesis_topic>
        </degree>
    </education>

    <certifications>
        <certification>
            <name></name>
            <issuer></issuer>
            <date></date>
            <status></status>
        </certification>
    </certifications>

    <projects>
        <project>
            <name></name>
            <description></description>
            <technologies_used>
                <tech name="" purpose=""/>
            </technologies_used>
            <impact></impact>
        </project>
    </projects>
</resume>

Important instructions:
1. Maintain exact XML structure and tags
2. Do not omit any tags - use empty tags if no information is found
3. Add relevant attributes where specified (name, level, context, etc.)
4. Split compound information into appropriate attributes
5. Include numeric metrics when available
6. Provide context for skills where they were used
7. Connect skills to specific experiences or projects"""

def get_verification_prompt() -> str:
    """Get a prompt to verify XML structure and content."""
    return """
Please verify the following for the generated XML:
1. All tags are properly closed
2. Required attributes are filled
3. Dates are consistently formatted
4. Skills are properly cross-referenced
5. Impact metrics are quantified where possible

If any issues are found, please regenerate the XML with corrections."""
