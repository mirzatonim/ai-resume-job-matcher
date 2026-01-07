package com.example.airesumematcher.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import com.example.airesumematcher.dto.MatchRequest;
import com.example.airesumematcher.dto.MatchResponse;
import com.example.airesumematcher.service.AIMatcherService;

@Controller
public class MatchViewController {

    private final AIMatcherService aiService;

    public MatchViewController(AIMatcherService aiService) {
        this.aiService = aiService;
    }

    @GetMapping("/")
    public String home() {
        return "index";
    }

    @PostMapping("/match-ui")
    public String matchUI(
            @RequestParam(value = "resume", required = false) String resumeText,
            @RequestParam("resumeFile") MultipartFile resumeFile,
            @RequestParam("job") String job,
            Model model) throws Exception {

        String finalResume;

        // Logic: Use File if provided, otherwise use pasted text
        if (!resumeFile.isEmpty()) {
            finalResume = extractTextFromFile(resumeFile);
        } else {
            finalResume = resumeText;
        }

        MatchRequest request = new MatchRequest(finalResume, job);
        MatchResponse response = aiService.getMatchScore(request);
        

        // Map response to the Model for Thymeleaf
        model.addAttribute("score", (int) response.getSimilarity_score());
        model.addAttribute("match", response.isMatch());
        model.addAttribute("skillsMatch", (int) response.getSkillsMatch());
        model.addAttribute("experienceMatch", (int) response.getExperienceMatch());
        model.addAttribute("keywordsMatch", (int) response.getKeywordsMatch());

        return "result";
    }

    private String extractTextFromFile(MultipartFile file) throws Exception {
        org.apache.tika.Tika tika = new org.apache.tika.Tika();
        return tika.parseToString(file.getInputStream());
    }
}