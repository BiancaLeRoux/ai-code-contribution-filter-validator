# AI Code Contribution Filter/Validator

> Stop drowning in low-quality AI-generated pull requests. Automate the detection of "slop" contributions and reclaim your review time.

## The Problem

Open-source maintainers are overwhelmed. AI-generated PRs flood repositories with:
- Generic, repetitive code changes
- Over-commented, verbose implementations  
- Conversational commit messages ("Certainly! I've updated...")
- Low-value contributions that waste precious review time

**You can't sustain this pace.** This tool helps you filter signal from noise.

## What It Does

AI Code Filter uses heuristic analysis to detect likely AI-generated contributions:

✅ **Commit Message Analysis** - Flags conversational AI phrases and generic patterns  
✅ **Code Pattern Detection** - Identifies repetitive structures and suspicious formatting  
✅ **Risk Scoring** - Assigns LOW/MEDIUM/HIGH risk levels with actionable recommendations  
✅ **GitHub Actions Ready** - Integrates seamlessly into your CI/CD pipeline  

## Quick Start

### As a GitHub Action

```yaml
name: AI PR Filter
on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run AI Filter
        run: |
          python ai_code_filter.py "${{ github.event.pull_request.title }}" diff.txt
```

### As a CLI Tool

```bash
python ai_code_filter.py "commit message" diff.txt
```

## Detection Heuristics

- **AI Conversational Phrases**: "certainly", "I apologize", "here's the", etc.
- **Generic Commits**: "update file", "fix issue", "improve code"
- **Repetitive Patterns**: Duplicate code blocks, excessive TODOs
- **Over-commenting**: Comment-to-code ratio > 50%
- **Uniform Formatting**: Suspiciously consistent line lengths

## Output Example

```json
{
  "risk_level": "HIGH",
  "score": 45,
  "flags": [
    "AI phrase detected: 'certainly'",
    "Generic commit message pattern",
    "Excessive comments ratio: 15/20"
  ],
  "recommendation": "Manual review strongly recommended."
}
```

## Pricing

- **Free**: Public repositories
- **Pro ($29/mo)**: Private repositories, 5 repos
- **Enterprise ($99/mo)**: Unlimited repos, priority support

## Roadmap

- [ ] Machine learning model for improved accuracy
- [ ] GitLab/Bitbucket support
- [ ] Browser extension for code review
- [ ] Integration with code review platforms

## License

MIT License - Free for public repos, paid license required for private/commercial use.

---

**Reclaim your time. Focus on contributions that matter.**