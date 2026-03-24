python
#!/usr/bin/env python3
"""
Test suite for ai_pr_validator.py
Tests the AI Code Contribution Filter/Validator functionality.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Import the script under test
import ai_pr_validator as script_under_test


class TestAICodeDetectorInitialization:
    """Test AICodeDetector class initialization."""
    
    def test_detector_initializes_with_zero_score(self):
        """Test that detector initializes with score of 0."""
        detector = script_under_test.AICodeDetector()
        assert detector.score == 0
    
    def test_detector_initializes_with_empty_flags(self):
        """Test that detector initializes with empty flags list."""
        detector = script_under_test.AICodeDetector()
        assert detector.flags == []
        assert isinstance(detector.flags, list)


class TestAnalyzeCommitMessage:
    """Test commit message analysis functionality."""
    
    def test_analyze_commit_message_with_ai_phrases(self):
        """Test detection of AI conversational phrases in commit messages."""
        detector = script_under_test.AICodeDetector()
        message = "Certainly, I have updated the code to fix the issue"
        score = detector.analyze_commit_message(message)
        
        assert score > 0
        assert any("AI phrase detected" in flag for flag in detector.flags)
    
    def test_analyze_commit_message_with_generic_pattern(self):
        """Test detection of generic commit message patterns."""
        detector = script_under_test.AICodeDetector()
        message = "update file.py"
        score = detector.analyze_commit_message(message)
        
        assert score >= 10
        assert any("Generic commit message pattern" in flag for flag in detector.flags)
    
    def test_analyze_commit_message_with_long_message(self):
        """Test detection of unusually long commit messages."""
        detector = script_under_test.AICodeDetector()
        message = "A" * 501  # Create a message longer than 500 characters
        score = detector.analyze_commit_message(message)
        
        assert score >= 8
        assert any("Unusually long commit message" in flag for flag in detector.flags)
    
    def test_analyze_commit_message_with_clean_message(self):
        """Test that clean commit messages return low or zero score."""
        detector = script_under_test.AICodeDetector()
        message = "Add user authentication feature"
        score = detector.analyze_commit_message(message)
        
        assert score == 0
        assert len(detector.flags) == 0
    
    def test_analyze_commit_message_case_insensitive(self):
        """Test that AI phrase detection is case-insensitive."""
        detector = script_under_test.AICodeDetector()
        message = "CERTAINLY this will work"
        score = detector.analyze_commit_message(message)
        
        assert score > 0
        assert any("AI phrase detected" in flag for flag in detector.flags)
    
    def test_analyze_commit_message_with_empty_string(self):
        """Test handling of empty commit message."""
        detector = script_under_test.AICodeDetector()
        message = ""
        score = detector.analyze_commit_message(message)
        
        assert score == 0
        assert isinstance(score, int)
    
    def test_analyze_commit_message_multiple_ai_phrases(self):
        """Test detection of multiple AI phrases increases score."""
        detector = script_under_test.AICodeDetector()
        message = "Certainly, I apologize for the confusion. Here's the updated code."
        score = detector.analyze_commit_message(message)
        
        # Should detect multiple phrases
        assert score >= 30  # At least 2 phrases * 15 points each
        ai_phrase_flags = [flag for flag in detector.flags if "AI phrase detected" in flag]
        assert len(ai_phrase_flags) >= 2


class TestAnalyzeCodeDiff:
    """Test code diff analysis functionality."""
    
    def test_analyze_code_diff_with_repetitive_patterns(self):
        """Test detection of repetitive code patterns."""
        detector = script_under_test.AICodeDetector()
        diff = """
+    x = x
+    y = y
+    z = z
        """
        score = detector.analyze_code_diff(diff)
        
        assert score > 0
        assert any("Repetitive code pattern" in flag for flag in detector.flags)
    
    def test_analyze_code_diff_with_excessive_comments(self):
        """Test detection of excessive comment ratio."""
        detector = script_under_test.AICodeDetector()
        diff = """
+    # This is a comment
+    # Another comment
+    # Yet another comment
+    x = 1
+    # More comments
+    y = 2
        """
        score = detector.analyze_code_diff(diff)
        
        # Comment ratio is > 0.5, should trigger flag
        assert score >= 10
    
    def test_analyze_code_diff_with_clean_code(self):
        """Test that clean code diffs return low score."""
        detector = script_under_test.AICodeDetector()
        diff = """
+    def calculate_sum(a, b):
+        return a + b
+    
+    result = calculate_sum(5, 3)
        """
        score = detector.analyze_code_diff(diff)
        
        # Should have low or zero score for clean code
        assert score == 0
    
    def test_analyze_code_diff_with_empty_string(self):
        """Test handling of empty diff."""
        detector = script_under_test.AICodeDetector()
        diff = ""
        score = detector.analyze_code_diff(diff)
        
        assert score == 0
        assert isinstance(score, int)
    
    def test_analyze_code_diff_with_multiple_todo_comments(self):
        """Test detection of excessive TODO comments."""
        detector = script_under_test.AICodeDetector()
        diff = """
+    # TODO: Implement feature A
+    # TODO: Implement feature B
+    # TODO: Implement feature C
+    # TODO: Implement feature D
        """
        score = detector.analyze_code_diff(diff)
        
        assert score > 0
    
    def test_analyze_code_diff_comment_ratio_with_no_code_lines(self):
        """Test that comment ratio calculation handles zero code lines safely."""
        detector = script_under_test.AICodeDetector()
        diff = """
+    # Only comments here
+    # No actual code
        """
        score = detector.analyze_code_diff(diff)
        
        # Should not crash with division by zero
        assert isinstance(score, int)
        assert score >= 0
    
    def test_analyze_code_diff_balanced_comments(self):
        """Test that balanced comment-to-code ratio doesn't trigger flag."""
        detector = script_under_test.AICodeDetector()
        diff = """
+    # Initialize variables
+    x = 1
+    y = 2
+    z = 3
+    # Calculate result
+    result = x + y + z
        """
        score = detector.analyze_code_diff(diff)
        
        # Comment ratio should be reasonable, not triggering excessive comment flag
        comment_flags = [flag for flag in detector.flags if "comment" in flag.lower()]
        assert len(comment_flags) == 0


class TestModuleConstants:
    """Test that module constants are properly defined."""
    
    def test_ai_phrases_constant_exists(self):
        """Test that AI_PHRASES constant is defined and is a list."""
        assert hasattr(script_under_test, 'AI_PHRASES')
        assert isinstance(script_under_test.AI_PHRASES, list)
        assert len(script_under_test.AI_PHRASES) > 0
    
    def test_generic_commit_patterns_constant_exists(self):
        """Test that GENERIC_COMMIT_PATTERNS constant is defined."""
        assert hasattr(script_under_test, 'GENERIC_COMMIT_PATTERNS')
        assert isinstance(script_under_test.GENERIC_COMMIT_PATTERNS, list)
        assert len(script_under_test.GENERIC_COMMIT_PATTERNS) > 0
    
    def test_repetitive_patterns_constant_exists(self):
        """Test that REPETITIVE_PATTERNS constant is defined."""
        assert hasattr(script_under_test, 'REPETITIVE_PATTERNS')
        assert isinstance(script_under_test.REPETITIVE_PATTERNS, list)
        assert len(script_under_test.REPETITIVE_PATTERNS) > 0


class TestIntegrationScenarios:
    """Test integrated scenarios combining multiple analysis methods."""
    
    def test_high_score_ai_generated_pr(self):
        """Test detection of obviously AI-generated PR."""
        detector = script_under_test.AICodeDetector()
        
        # AI-like commit message
        commit_msg = "Certainly! I have updated the code as requested. Here's the improved version."
        detector.analyze_commit_message(commit_msg)
        
        # AI-like diff with excessive comments
        diff = """
+    # This function calculates the sum
+    # It takes two parameters
+    # Returns the sum of the parameters
+    def add(a, b):
+        # Return the result
+        return a + b
        """
        detector.analyze_code_diff(diff)
        
        # Should have accumulated significant score
        assert detector.score > 20
        assert len(detector.flags) > 0
    
    def test_clean_human_pr(self):
        """Test that clean human-written PR gets low score."""
        detector = script_under_test.AICodeDetector()
        
        # Clean commit message
        commit_msg = "Implement user authentication with JWT tokens"
        detector.analyze_commit_message(commit_msg)
        
        # Clean diff
        diff = """
+    def authenticate_user(username, password):
+        token = generate_jwt(username)
+        return token
        """
        detector.analyze_code_diff(diff)
        
        # Should have low score
        assert detector.score == 0