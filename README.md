# Aurix AI Assistant 🐨

Aurix AI Assistant is a powerful, privacy-first, locally-run AI meeting assistant. It enables users to process audio/video recordings (including YouTube videos and file uploads) to perform local speech-to-text transcription, translation, semantic indexing, and conversational Q&A.

The entire application runs locally, utilizing local Whisper models for transcription, local embeddings for vector search, and a Flask-based web interface.

---

## 🚀 Key Features

- **Audio/Video Processing**: Download audio directly from YouTube URLs or upload local MP3/WAV/MP4 files.
- **Local Speech-to-Text**: High-accuracy local transcription using OpenAI's Whisper model.
- **Multilingual Support**: Supports transcribing in multiple languages, with automatic Hindi-to-English translation.
- **RAG-Powered Conversations**: Perform semantic indexing on transcripts using ChromaDB and Hugging Face embedding models, allowing natural conversation with your meeting records.
- **Export Formats**: Export meetings summaries and transcripts to high-quality PDF or TXT formats.
- **Privacy-First**: No data leaves your machine; LLM calls and transcription occur completely locally or via secure API integrations.

---

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-CORS
- **Speech-to-Text**: OpenAI Whisper, PyTorch
- **Vector Database**: ChromaDB
- **LLM/Embeddings**: LangChain, langchain-huggingface (local embeddings), Mistral AI
- **Acquisition**: yt-dlp, FFmpeg, pydub
- **Styling & UI**: Vanilla CSS, Modern Responsive HTML5, Custom JavaScript

---

## 📦 Getting Started

### Prerequisites

- **Python 3.10+**
- **FFmpeg**: Must be installed on your system path.
  - *macOS*: `brew install ffmpeg`
  - *Ubuntu/Linux*: `sudo apt-get install ffmpeg`

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shubhamkr371/Aurix-AI.git
   cd Aurix-AI
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r Requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   MISTRAL_API_KEY=your-mistral-api-key
   FLASK_SECRET_KEY=your-secure-flask-secret
   ```

5. **Run the application**:
   ```bash
   python server.py
   ```
   Open your browser and navigate to `http://localhost:5000`.

---

## 🐳 Docker Deployment

The application includes a fully optimized production Dockerfile and a `docker-compose.yml` orchestration configuration.

### Using Docker Compose

1. Build and start the container:
   ```bash
   docker compose up --build -d
   ```
2. The application will be accessible at `http://localhost:5000`.
3. Check status and health:
   ```bash
   docker compose ps
   ```

---

## 🧪 Testing

The repository features a fully mocked, high-speed test suite using `pytest`. Testing does not require downloading heavy ML models or having active API keys.

### Running Tests Locally

1. Install development and testing dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run the test suite:
   ```bash
   pytest tests/ -v
   ```

---

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration. The workflow runs automatically on pushes and pull requests targeting the `main` branch.

The pipeline comprises three automated jobs:
1. **Lint & Security Scan**:
   - Runs `flake8` to detect syntax errors and style violations.
   - Runs `bandit` to identify security vulnerabilities.
2. **Run Tests**:
   - Executes the mocked `pytest` suite inside a clean virtual environment.
3. **Docker Build**:
   - Compiles the production Docker image to ensure validity.
   - Performs a container **Smoke Test** by spinning up the built image, injecting mock credentials, and executing a health check on `http://localhost:5000/api/health`.

