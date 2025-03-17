# CindyAI - Learning Experience Platform Assistant

CindyAI is an intelligent assistant designed to enhance learning experiences by providing interactive help and insights based on educational content from various sources including YouTube videos, articles, and PDFs.

## Features

- Interactive chatbot for learning assistance
- Content processing from multiple sources:
  - YouTube video transcripts
  - Articles
  - PDF documents
- RESTful API for seamless integration with LXP
- Modern, responsive user interface

## Tech Stack

### Backend
- FastAPI (Python)
- LangChain for AI/LLM operations
- SQLAlchemy for database management
- Various content processing libraries (PyTube, PyPDF2, etc.)

### Frontend
- Vue.js 3 (Composition API)
- TypeScript
- Pinia for state management
- Tailwind CSS with shadcn for styling

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Virtual environment tool (venv)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file and set required environment variables:
   ```
   OPENAI_API_KEY=your_api_key
   ```

5. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 