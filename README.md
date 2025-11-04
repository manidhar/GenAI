# GeniAI Project

## Environment Setup

1. Clone the repository
```bash
git clone <repository-url>
cd GeniAI
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file
Create a new file named `.env` in the root directory and add the following environment variables:

```properties
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Base URL for API (if needed)
base_url=https://generativelanguage.googleapis.com/v1beta/openai/

# Tokenizers Configuration
TOKENIZERS_PARALLELISM=false
```

Replace `your_openai_api_key_here` and `your_gemini_api_key_here` with your actual API keys:
- Get your OpenAI API key from: https://platform.openai.com/api-keys
- Get your Gemini API key from: https://makersuite.google.com/app/apikey

5. Verify Setup
```bash
# Test the environment setup
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Setup OK' if 'GEMINI_API_KEY' in os.environ else 'Missing ENV')"
```

## Project Structure

```
GeniAI/
├── 01_Tokenization/       # Tokenization examples
├── 02_hello_world/        # Basic API usage examples
├── 03_prompts/            # Various prompt engineering examples
└── 04_Ollama_fastapi/    # FastAPI integration with Ollama
```

## Running the Applications

### FastAPI Ollama Server
```bash
cd 04_Ollama_fastapi
uvicorn ollama_api:app --reload --port 8000
```

## Security Notes

- Never commit the `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use environment variables for all sensitive configuration