# Job Tracking System

A comprehensive system for managing and tracking job applications throughout the hiring process.

## Design Philosophy

This project follows a modular design approach with clear separation of concerns:

1. **PDF Processing Module**
   - Handles PDF document processing
   - Integrates with LLaMA 3.2 Vision via Ollama
   - Extracts structured content with XML tags
   - Input: PDF file path -> Output: Tagged content

2. **XML Processing Module**
   - Processes LLaMA-generated XML content
   - Extracts and validates tag structure
   - Maintains hierarchical relationships
   - Input: Tagged text -> Output: Structured tag data

3. **Graph Processing Module** (Planned)
   - Transforms structured data into knowledge graph
   - Defines nodes and relationships
   - Enables query and analysis capabilities
   - Input: Structured tag data -> Output: Graph database

Each module has a single responsibility and clear interfaces, making the system maintainable and extensible.

## Technology Stack

- Frontend: React.js
- Backend: Node.js/Express
- Database: MongoDB
- LLM Integration: Ollama with LLaMA 3.2 Vision
- Graph Database: (TBD)

## Project Structure

```
job-tracking-system/
├── src/
│   ├── pdf_processor.py    # PDF processing and LLaMA integration
│   ├── xml_processor.py    # XML extraction and structuring
│   ├── graph_processor.py  # Knowledge graph creation (planned)
│   └── main.py            # Application entry point
├── docs/                  # Documentation
└── README.md             # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- Ollama with LLaMA 3.2 Vision model
- PDF processing libraries

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/truaxki/job-tracking-system.git
   ```

2. Install dependencies:
   ```bash
   cd job-tracking-system
   pip install -r requirements.txt
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: [https://github.com/truaxki/job-tracking-system](https://github.com/truaxki/job-tracking-system)