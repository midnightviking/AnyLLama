# AnyLLama - Docker-based LLM Management System

AnyLLama is a Docker-based system that provides an easy way to manage and serve Large Language Models (LLMs) using Ollama and AnythingLLM.

## Overview

This project consists of three main components:
- **Ollama**: The core LLM serving engine
- **Model Selection Interface**: A web interface for downloading and managing models
- **AnythingLLM**: A chat interface for interacting with your models

## Quick Start

### Prerequisites
- Docker and Docker Compose installed on your system
- At least 8GB of RAM (more recommended for larger models)
- Internet connection for downloading models

### 1. Start the Services

Run the following command in the project directory:

```bash
docker compose up -d --build
```

This will start all three services:
- Ollama server (port 11434)
- Model Selection Interface (port 5100) 
- AnythingLLM (port 3001)

### 2. Download and Serve Models

1. **Open the Model Selection Interface**
   - Navigate to http://localhost:5100 in your web browser
   - This interface allows you to browse available models and download them

2. **Pull a Model**
   - In the interface, you can search for and select models like:
     - `llama3.2:1b` (small, fast model - good for testing)
     - `llama3.1:8b` (medium model - good balance of speed/quality)
     - `codellama:7b` (specialized for code generation)
   - Click on Pull to start downloading it
   - The download progress will be displayed in real-time

3. **Alternative: Command Line Model Download**
   ```bash
   # Download a specific model directly via Ollama
   docker compose exec ollama ollama pull llama3.2:1b
   ```

### 3. Use AnythingLLM

1. **Access the Chat Interface**
   - Navigate to http://localhost:3001 in your web browser
   - This is your main chat interface for interacting with downloaded models

2. **Configure AnythingLLM**
   - On first visit, you'll need to set up AnythingLLM
   - Configure it to use the Ollama service at: `http://ollama:11434`
   - Select your downloaded model from the available options

## Service Details

### Port Mappings
- **5100**: Model Selection Interface - Download and manage Ollama models
- **11434**: Ollama API - Direct API access to the LLM server
- **3001**: AnythingLLM - Chat interface and document processing

### Docker Services

#### Ollama Container
- Runs the Ollama server for serving LLM models
- Handles model downloads and inference
- GPU acceleration support (if available)

#### Model Selection Container  
- Python Flask application for model management
- Provides a web interface for downloading models
- Real-time download progress tracking
- Model status monitoring

#### AnythingLLM Container
- Full-featured chat interface
- Document upload and processing capabilities  
- Workspace and conversation management
- Integration with Ollama backend

## Common Workflows

### First Time Setup
1. `docker compose up -d --build`
2. Visit http://localhost:5100 to download a model
3. Visit http://localhost:3001 to configure AnythingLLM
4. Start chatting with your local LLM!

### Adding New Models
1. Go to http://localhost:5100
2. Search for the desired model
3. Click to download (this may take a while depending on model size)
4. Once downloaded, the model will be available in AnythingLLM

### Checking Service Status
```bash
# View running containers
docker compose ps

# View logs for a specific service
docker compose logs ollama
docker compose logs model_selection
docker compose logs anythingllm
```

### Stopping Services
```bash
# Stop all services
docker compose down

# Stop and remove volumes (warning: this will delete downloaded models)
docker compose down -v
```

## Troubleshooting

### Models Not Appearing
- Ensure Ollama service is running: `docker compose ps`
- Check if models are downloaded: visit http://localhost:5100
- Verify network connectivity between containers

### Out of Memory Issues
- Smaller models like `llama3.2:1b` require less RAM
- Consider increasing Docker memory limits
- Monitor system resources during model downloads

### Port Conflicts
- Ensure ports 3001, 5100, and 11434 are not in use by other applications
- Modify port mappings in `docker-compose.yml` if needed
