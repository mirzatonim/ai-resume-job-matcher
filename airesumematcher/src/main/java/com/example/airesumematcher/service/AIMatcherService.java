package com.example.airesumematcher.service;

import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import com.example.airesumematcher.dto.MatchRequest;
import com.example.airesumematcher.dto.MatchResponse;

import reactor.core.publisher.Mono;

@Service
public class AIMatcherService {

    private final WebClient webClient;

    public AIMatcherService(WebClient webClient) {
        this.webClient = webClient;
    }

    public MatchResponse getMatchScore(MatchRequest request) {
        return webClient.post()
                .uri("/match-score")
                .bodyValue(request)
                .retrieve()
                .onStatus(HttpStatusCode::isError, clientResponse -> 
                    Mono.error(new RuntimeException("AI Service Error")))
                .bodyToMono(MatchResponse.class)
                .map(res -> {
                    double finalScore = res.getSimilarity_score() * 100;
                    res.setSimilarity_score(finalScore);
                    res.setMatch(finalScore >= 70);
                    res.setSkillsMatch(Math.min(100, finalScore * 1.05));      
                    res.setExperienceMatch(Math.min(100, finalScore * 0.88));  
                    res.setKeywordsMatch(finalScore);
                    return res;
                })
                .block();

    
    }
}

