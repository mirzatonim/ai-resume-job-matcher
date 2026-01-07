package com.example.airesumematcher.controller;


import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import com.example.airesumematcher.dto.MatchRequest;
import com.example.airesumematcher.dto.MatchResponse;
import com.example.airesumematcher.service.AIMatcherService;

@RestController
@RequestMapping("/api/match")
public class MatchApiController {

    private final AIMatcherService aiService;

    public MatchApiController(AIMatcherService aiService) {
        this.aiService = aiService;
    }

    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<MatchResponse> match(@RequestBody MatchRequest request) {
        return ResponseEntity.ok(aiService.getMatchScore(request));
    }

    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<MatchResponse> matchWithFile(
            @RequestParam("resumeFile") MultipartFile resumeFile,
            @RequestParam("job") String job) throws IOException {

        String resume = new String(resumeFile.getBytes(), StandardCharsets.UTF_8);
        MatchRequest request = new MatchRequest(resume, job);

        return ResponseEntity.ok(aiService.getMatchScore(request));
    }
}
