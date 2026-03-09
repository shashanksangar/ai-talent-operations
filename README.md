# AI Talent Operations - Main Orchestrator

A comprehensive AI-powered talent operations platform that coordinates multiple specialized agents for efficient recruiting workflows.

## 🏗️ Architecture

This repository serves as the main orchestrator for the AI Talent ecosystem:

- **ai-talent-scheduling-agent** - Interview scheduling with thumb rules
- **ai-talent-model-mapping-agent** - AI model analysis and researcher profiling
- **ai-talent-sourcing-agent** - Candidate sourcing and discovery
- **ai-talent-matching-agent** - Candidate-job matching
- **ai-talent-outreach-agent** - Automated outreach and communication

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run configuration stress test
python stress_test.py

# Run scheduling workflow
python main.py --workflow scheduling --interviewer "Sarah Chen" --candidate "John Doe" --role "ML Engineer"

# Run model mapping workflow
python main.py --workflow model_mapping --model "GPT-4"
```

## 📋 Workflows

### Scheduling Agent
- Enforces 1 interview per interviewer per week
- Prevents double-booking and scheduling conflicts
- Outlook calendar integration ready

### Model Mapping Agent
- Maps AI models to technical summaries
- Detailed author profiling (first author: homepage/github/scholar/arxiv)
- arXiv integration for research paper discovery

## 🔧 Configuration

Edit `config.yaml` to configure agent settings and API keys.

## 🧪 Testing

```bash
# Run stress test
python stress_test.py

# Run individual agent tests
cd ../ai-talent-scheduling-agent && python -m pytest
cd ../ai-talent-model-mapping-agent && python -m pytest
```

## 📚 Related Repositories

- [AI Talent Scheduling Agent](https://github.com/shashanksangar/ai-talent-scheduling-agent)
- [AI Talent Model Mapping Agent](https://github.com/shashanksangar/ai-talent-model-mapping-agent)
- [AI Talent Sourcing Agent](https://github.com/shashanksangar/ai-talent-sourcing-agent)
- [AI Talent Matching Agent](https://github.com/shashanksangar/ai-talent-matching-agent)
- [AI Talent Outreach Agent](https://github.com/shashanksangar/ai-talent-outreach-agent)

## 🤝 Contributing

Each agent is developed in its own repository. Please contribute to the specific agent you're working on.

## 📄 License

MIT License

**Now accepting operational efficiency projects.** Ready for first workflow implementation.

---

*Part of the AI Talent Copilot ecosystem*
