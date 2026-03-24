python
#!/usr/bin/env python3
"""
AI Code Contribution Filter/Validator
Detects low-quality AI-generated pull requests using heuristic analysis.

This tool analyzes PR diffs, commit messages, and code patterns to identify
potentially AI-generated contributions that may require extra scrutiny.
"""

import re
import json
import sys
from collections import Counter
from typing import Dict, List, Tuple

# Common AI-generated code patterns and phrases
AI_PHRASES = [
    "certainly", "i apologize", "i understand", "let me",
    "here's the", "here is the", "as an ai", "i've updated",
    "i have updated", "i'll", "i will", "my apologies"
]

GENERIC_COMMIT_PATTERNS = [
    r"^update\s+\w+\.\w+$",
    r"^fix\s+issue$",
    r"^improve\s+code$",
    r"^refactor$",
    r"^changes$",
    r"^updated?\s+file",
]

# Repetitive code patterns that AI often generates
REPETITIVE_PATTERNS = [
    r"(\w+)\s*=\s*\1",  # Variable assigned to itself
    r"(if\s+\w+:\s*\n\s*pass\s*\n){3,}",  # Multiple empty if blocks
    r"(#\s*TODO:?\s*.{10,}\n){3,}",  # Excessive TODOs
]


class AICodeDetector:
    """Detects AI-generated code contributions using heuristic analysis."""

    def __init__(self):
        self.score = 0
        self.flags = []

    def analyze_commit_message(self, message: str) -> int:
        """Analyze commit message for AI-generated patterns."""
        score = 0
        message_lower = message.lower()

        # Check for AI conversational phrases
        for phrase in AI_PHRASES:
            if phrase in message_lower:
                score += 15
                self.flags.append(f"AI phrase detected: '{phrase}'")

        # Check for generic commit patterns
        for pattern in GENERIC_COMMIT_PATTERNS:
            if re.match(pattern, message.lower().strip()):
                score += 10
                self.flags.append(f"Generic commit message pattern")
                break

        # Check message length (AI often generates verbose messages)
        if len(message) > 500:
            score += 8
            self.flags.append("Unusually long commit message")

        return score

    def analyze_code_diff(self, diff: str) -> int:
        """Analyze code diff for repetitive and suspicious patterns."""
        score = 0

        # Check for repetitive patterns
        for pattern in REPETITIVE_PATTERNS:
            matches = re.findall(pattern, diff)
            if matches:
                score += 12 * len(matches)
                self.flags.append(f"Repetitive code pattern found ({len(matches)} instances)")

        # Check for excessive comments (AI loves to over-comment)
        comment_lines = len(re.findall(r'^\+\s*#', diff, re.MULTILINE))
        code_lines = len(re.findall(r'^\+\s*[^#\s]', diff, re.MULTILINE))
        
        # Safe division - only calculate ratio if we have code lines
        if code_lines > 0:
            comment_ratio = comment_lines / code_lines
            if comment_ratio > 0.5:
                score += 10
                self.flags.append(f"Excessive comments ratio: {comment_lines}/{code_lines}")

        # Check for overly uniform line lengths (AI formatting)
        added_lines = re.findall(r'^\+(.*)$', diff, re.MULTILINE)
        if len(added_lines) > 10:
            line_lengths = [len(line) for line in added_lines if line.strip()]
            if line_lengths:
                avg_length = sum(line_lengths) / len(line_lengths)
                # Calculate variance with safe division
                variance = sum((x - avg_length) ** 2 for x in line_lengths) / len(line_lengths)
                if variance < 50:  # Very uniform line lengths
                    score += 8
                    self.flags.append("Suspiciously uniform code formatting")

        return score

    def analyze_pr(self, commit_message: str, diff: str) -> Dict:
        """Perform complete PR analysis."""
        self.score = 0
        self.flags = []

        # Accumulate scores from different analysis methods
        self.score += self.analyze_commit_message(commit_message)
        self.score += self.analyze_code_diff(diff)

        # Determine risk level based on score
        if self.score >= 40:
            risk_level = "HIGH"
        elif self.score >= 20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "score": self.score,
            "risk_level": risk_level,
            "flags": self.flags,
            "requires_review": self.score >= 20
        }


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 3:
        print("Usage: python ai_pr_validator.py <commit_message> <diff_file>")
        print("Example: python ai_pr_validator.py 'Fix bug' changes.diff")
        sys.exit(1)

    commit_message = sys.argv[1]
    diff_file = sys.argv[2]

    try:
        with open(diff_file, 'r', encoding='utf-8') as f:
            diff = f.read()
    except FileNotFoundError:
        print(f"Error: Diff file '{diff_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading diff file: {e}")
        sys.exit(1)

    # Perform analysis
    detector = AICodeDetector()
    result = detector.analyze_pr(commit_message, diff)

    # Output results as JSON
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["risk_level"] == "LOW" else 1)


if __name__ == "__main__":
    main()