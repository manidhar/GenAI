package com.ai.gemini_chat_backend;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Service
public class QnAService {
    // Access to API key and endpoint
    @Value("${gemini.api.url}")
    private String geminiApiUrl;
    @Value("${gemini.api.key}")
    private String geminiApiKey;

    private final WebClient webClient;

    public QnAService(WebClient.Builder webClient) {
        this.webClient = webClient.build();
    }

    public String getAnswer(String question) {
        // Construct the request payload for the Gemini API
        Map<String,Object> requestPayload = Map.of(
                "contents",new Object[]{
                        Map.of("parts", new Object[]{Map.of("text", question)})
                }
        );
        // Make API call to Gemini
        String response=webClient.post()
                .uri(geminiApiUrl)
                .header("x-goog-api-key", geminiApiKey)
                .header("content-type", "application/json")
                .bodyValue(requestPayload)
                .retrieve()
                .bodyToMono(String.class)
                .block();

        // Return response
        return response;
    }
}
