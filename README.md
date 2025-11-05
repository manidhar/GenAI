# GeniAI Project

## Environment Setup

1. Clone the repository
```bash
git clone https://github.com/manidhar/GenAI.git
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

### LangGraph Examples (09_langGraph)

The LangGraph examples demonstrate building AI workflows using LangGraph. First, install the required dependencies:


#### Running Hello World Example

1. Navigate to the LangGraph directory:
```bash
cd 09_langGraph
```

2. Run the hello world example:
```bash
python -m basics.hello_world
```

This will:
- Create a simple graph with "hello" and "bye" nodes
- Process the message "Manidhar" through the graph
- Generate and display a visualization of the graph structure
- Print the final output

You can also run it from the project root with:
```bash
python -m 09_langGraph.basics.hello_world
```

The example will show a PNG image of the graph structure and print the message transformations through the nodes.

### LangGraph Examples (09_langGraph)

The LangGraph examples demonstrate how to build and visualize AI workflows using LangGraph.

#### Running the Hello World Example

From the `09_langGraph` directory:
```bash
# Run as a local package
python -m basics.hello_world
```

Or from the project root:
```bash
# Run as part of the full project package
python -m 09_langGraph.basics.hello_world
```

The hello world example will:
1. Create a simple graph with "hello" and "bye" nodes
2. Process a message through the graph
3. Display a visualization of the graph structure
4. Print the final output

## RQ Queue (08_rag_queue)

This project includes a small RQ-based queue for retrieval-augmented generation (RAG). The queue lives in `08_rag_queue` and uses Valkey/Redis (port 6379) and RQ workers to process jobs.

Important notes
- The worker code initializes heavy native libraries (OpenAI client, HuggingFace tokenizers, Qdrant client). To avoid macOS fork-related crashes and deadlocks, the repository initializes these resources lazily inside the job function and requires `TOKENIZERS_PARALLELISM=false` in the environment.
- If you run workers in containers or via a process manager, ensure the environment variable is exported before the worker process starts.

Environment variables (add them to your `.env`):

```properties
# Already listed above but callout for RQ
GEMINI_API_KEY=your_gemini_api_key_here
base_url=https://generativelanguage.googleapis.com/v1beta/openai/
TOKENIZERS_PARALLELISM=false
```

Start the FastAPI server for RQ (serves the enqueue endpoints):

```bash
# from repo root
uvicorn 08_rag_queue.server:app --reload --port 8000
```

Start an RQ worker (single-process example):

```bash
# ensure env is loaded or exported first
export TOKENIZERS_PARALLELISM=false
# run worker (adjust queue name / url as needed)
rq worker --url redis://localhost:6379 --verbose
```

Debugging tips
- If a worker crashes with Objective-C / fork errors on macOS, try the following (debug only):

```bash
# temporary debug flag (not recommended for production)
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES TOKENIZERS_PARALLELISM=false rq worker --url redis://localhost:6379 --verbose
```

- After making code changes to the worker module, restart the worker process so the new module-level behavior is loaded.
- If running with Docker / docker-compose, make sure the worker container's environment includes `TOKENIZERS_PARALLELISM=false` and avoid publishing Redis (6379) to the public network; bind it to localhost or secure it with a password.

Where to look
- Worker implementation: `08_rag_queue/queues/worker.py` (lazy initialization is used to avoid pre-fork native init)
- Server (enqueue endpoints): `08_rag_queue/server.py`


## Security Notes

- Never commit the `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use environment variables for all sensitive configuration