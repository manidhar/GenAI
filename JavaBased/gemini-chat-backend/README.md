# Gemini Chat Backend

A small Java Spring Boot backend for a question-and-answer (QnA) API used by the Gemini Chat project.

This repository contains a Spring Boot application (Gradle-based) that exposes an endpoint for asking questions and returning answers from a `QnAService`.

## Table of contents

- Project overview
- Requirements
- Quickstart (build & run)
- Environment variables & IntelliJ
- Running tests
- API
- Project structure
- Common issues & troubleshooting
- Contributing
- License

## Project overview

- Name: gemini-chat-backend
- Technology: Java 17, Spring Boot, Gradle
- Purpose: Provide a small HTTP API that accepts questions and returns answers via a pluggable `QnAService`.

## Requirements

- JDK 17 (OpenJDK or Oracle JDK)
- Gradle wrapper is included (use `./gradlew`)
- macOS, Linux or Windows (examples below assume macOS / zsh)

Verify Java version:

```bash
java -version
# OpenJDK 17.x or equivalent is required
```

## Quickstart

From the project root (where `gradlew` lives), run:

```bash
# Build the project
./gradlew clean build

# Run tests
./gradlew test

# Start the app (uses Spring Boot's bootRun)
./gradlew bootRun
```

After `bootRun` the server should start on port 8080 by default. You can change config in `src/main/resources/application.properties`.

Alternatively, run the generated jar:

```bash
# Build produces build/libs/gemini-chat-backend-<version>.jar
java -jar build/libs/gemini-chat-backend-0.0.1-SNAPSHOT.jar
```

## Environment variables (local & CI) and running with them

This project may read configuration and secrets from environment variables (for example, an API key or API URL for a Gemini/LLM service). Two common env vars you might use:

- `GEMINI_API_KEY` — your API key
- `GEMINI_API_URL` — base URL for the API

How to set and use them:

- macOS / Linux (zsh / bash)

```bash
# Temporarily for the current shell session
export GEMINI_API_KEY="your_api_key_here"
export GEMINI_API_URL="https://api.example.com"

# Then run the app with Gradle (env vars are inherited by the process)
./gradlew bootRun

# Or one-liner without exporting permanently
GEMINI_API_KEY="your_api_key_here" GEMINI_API_URL="https://api.example.com" ./gradlew bootRun
```

To run the packaged jar with env vars:

```bash
GEMINI_API_KEY="your_api_key_here" java -jar build/libs/gemini-chat-backend-0.0.1-SNAPSHOT.jar
```

- Windows (PowerShell)

```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
$env:GEMINI_API_URL = "https://api.example.com"
./gradlew.bat bootRun
```

Persisting vars on macOS (zsh): add the exports to `~/.zshrc` and run `source ~/.zshrc`.

Spring Boot mapping notes:

- Spring will expose environment variables to your application (you can reference them in `application.properties` or `@Value` using property names). If you prefer System properties, you can pass JVM options like `-Dgemini.api.key=...` in run configurations or `JAVA_OPTS`.

## Running in IntelliJ IDEA (Run / Debug)

To run the app from IntelliJ with environment variables configured:

1. Open the project in IntelliJ (File -> Open -> select the project root where `build.gradle` is).
2. Let IntelliJ import the Gradle project (it may ask to enable auto-import).
3. Create or edit a Run/Debug configuration:
   - Run -> Edit Configurations...
   - Click + -> Application
   - Name: `GeminiChatBackendApplication`
   - Main class: `com.ai.gemini_chat_backend.GeminiChatBackendApplication`
   - Use classpath of module: choose the main module (usually `gemini-chat-backend.main` or similar)
   - Working directory: project root (default)
   - Environment variables: `GEMINI_API_KEY=your_api_key_here,GEMINI_API_URL=https://api.example.com` (comma-separated)
   - VM options (optional): `-Dspring.profiles.active=dev` or other system properties
   - Program arguments: (none required for typical runs)
   - Click Apply -> OK
4. Select the new configuration and click Run (green ▶) or Debug (🐞) to start the application inside the IDE.

Notes and alternatives inside IntelliJ:

- Instead of environment variables you can pass system properties via VM options: e.g. `-Dgemini.api.key=your_api_key_here` and then use `@Value("${gemini.api.key}")` or reference the property in `application.properties`.
- IntelliJ will show console logs and allow debugging breakpoints once started.
- To run Gradle tasks from IntelliJ, open the Gradle tool window and run `bootRun` or `test` tasks directly; those tasks will inherit the environment variables defined in the IDE Run configuration if you invoke them through the configuration.

## Running tests & reports

Run tests with the Gradle wrapper:

```bash
./gradlew test
```

Test reports are available at:

```
build/reports/tests/test/index.html
```

If you see failures referencing `NoSuchBeanDefinitionException` for `QnAService`, see the Troubleshooting section below.

## API

Base path: `/api/qna`

- POST /api/qna/ask
  - Request body: JSON { "question": "What is ...?" }
  - Response: plain string answer

Example using curl:

```bash
curl -sS -X POST http://localhost:8080/api/qna/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the capital of France?"}'
```

## Project structure

Key source files (under `src/main/java/com/ai/gemini_chat_backend`):

- `GeminiChatBackendApplication.java` — Spring Boot application entry point
- `AIController.java` — REST controller exposing `/api/qna/ask`
- `QnAService.java` — service interface for obtaining answers
- `QnAServiceImpl.java` — example `@Service` implementation (may be provided in the codebase)

Configuration & resources:

- `src/main/resources/application.properties`
- `build.gradle` and Gradle wrapper files for building

## Common issues & troubleshooting

1. JVM exits with non-zero value when starting the app
   - Symptoms: Gradle shows: "Process 'command .../bin/java' finished with non-zero exit value 1"
   - Cause: Usually Spring failed to start due to bean creation errors or missing configuration.
   - Fixes:
     - Look at the full stacktrace with `./gradlew bootRun --stacktrace` or check the test report `build/reports/tests/test/index.html`.
     - Ensure there is a Spring bean implementing `QnAService`. Example:

       - `QnAService.java` (interface)
       - `QnAServiceImpl.java` annotated with `@Service` that implements `getAnswer(String)`

     - Ensure controller uses constructor injection (no `= null` field initializers) so Spring can wire dependencies. Example constructor:

```java
public AIController(QnAService qnaService) {
    this.qnaService = qnaService;
}
```

2. Unit test failed: `contextLoads()` fails with `NoSuchBeanDefinitionException` for `QnAService`
   - Ensure a bean exists (see above) or add a test configuration that provides a test/mock bean.

## Developing

- Follow standard Spring Boot & Gradle patterns.
- Add more `QnAService` implementations or replace the stub with calls to an LLM or knowledge base as needed.
- If you add new beans, prefer constructor injection and mark service classes with `@Service`.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Run tests locally: `./gradlew test`
4. Open a PR with a description and link to any related issues

## License

This project does not include a license by default. Add a `LICENSE` file if you want to set a license.

---

If you'd like, I can also:
- add a minimal `QnAServiceImpl` stub to `src/main/java/...` if it's missing,
- run the tests and fix compile errors.

Tell me if you want me to create the README in a different style or add examples for Dockerization or CI.
