package com.example.airesumematcher.dto;

import lombok.*;

@Data
public class MatchResponse {
    private double similarity_score;
    private boolean match;
    private double skillsMatch;
    private double experienceMatch;
    private double keywordsMatch;

}
