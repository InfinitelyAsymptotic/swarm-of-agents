# Orchestrating Autonomy: Multi-Agent AI Systems Demo

**By Pranjal Joshi**

An interactive educational repository for learning about multi-agent AI systems through hands-on Jupyter notebooks. This demo is designed for the talk **"Orchestrating Autonomy: Designing Multi-Agent AI Systems"**.

## ⭐ Featured: Production Demo

**[`multi_agent_systems_demo.ipynb`](multi_agent_systems_demo.ipynb)** - A world-class, single-notebook demonstration featuring:

- 🤖 **Real AI agents** powered by OpenAI GPT models
- 📊 **Interactive visualizations** (Plotly, NetworkX, Mermaid diagrams)
- 🎨 **CS336-quality presentation** with live execution
- 🏗️ **Production-ready patterns** (sequential, feedback loops, hierarchical)
- 💼 **Real-world example**: Multi-agent research and writing team
- ⚡ **Live demo ready** - perfect for presentations!

> This is a complete, executable demo showcasing multi-agent orchestration with LangGraph and OpenAI.

## 📚 Overview

This repository provides a comprehensive, hands-on introduction to designing and implementing multi-agent AI systems using open-source tools. Inspired by Stanford's CS336 interactive learning approach, these notebooks combine theory with practical implementations.

## 🎯 What You'll Learn

- **Fundamentals** of multi-agent systems architecture
- **Communication patterns** between agents (point-to-point, broadcast, pub-sub, etc.)
- **Orchestration strategies** (sequential, parallel, hierarchical, dynamic)
- **Hands-on implementation** using LangGraph and other modern frameworks
- **Visualization techniques** for understanding agent interactions

## 📁 Repository Structure

```
swarm-of-agents/
├── multi_agent_systems_demo.ipynb              # ⭐ MAIN PRODUCTION DEMO
├── notebooks/
│   ├── 01_intro_to_multi_agent_systems.ipynb       # Fundamentals & core concepts
│   ├── 02_agent_communication_patterns.ipynb       # Message passing & protocols
│   ├── 03_orchestration_strategies.ipynb           # Coordination patterns
│   └── 04_hands_on_langgraph_demo.ipynb           # Real-world implementation
├── utils/
│   ├── __init__.py
│   └── visualization.py                            # Graph & timeline visualizations
├── assets/                                          # Generated visualizations
├── requirements.txt                                 # Python dependencies
├── .env.example                                     # API key template
└── README.md
```

## 🚀 Quick Start

### For the Production Demo (Recommended)

1. **Clone and setup**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/swarm-of-agents.git
   cd swarm-of-agents
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key**:
   - Get an API key from [platform.openai.com](https://platform.openai.com)
   - Open `multi_agent_systems_demo.ipynb`
   - Set the API key in the configuration cell

3. **Run the demo**:
   ```bash
   jupyter notebook multi_agent_systems_demo.ipynb
   # or
   jupyter lab multi_agent_systems_demo.ipynb
   ```

4. **Execute all cells** and watch the multi-agent system in action!

### For Learning Notebooks

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/swarm-of-agents.git
   cd swarm-of-agents
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter**:
   ```bash
   jupyter notebook
   # or
   jupyter lab
   ```

5. **Start with** `notebooks/01_intro_to_multi_agent_systems.ipynb`

### Using with LLMs (Optional)

The notebooks work with mock agents by default for learning the patterns. To use real LLMs:

#### Option 1: OpenAI (Cloud)
```bash
# Set your API key
export OPENAI_API_KEY="your-api-key-here"
```

#### Option 2: Local Models (Free)
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2
# The notebooks will automatically detect and use local models
```

## 📓 Notebook Guide

### 1. Introduction to Multi-Agent Systems
**Duration**: 30-40 minutes
**Topics**:
- What are multi-agent systems?
- Core components: perceive, reason, act
- Agent communication basics
- Design principles

**Key Takeaways**: Understand the motivation for multi-agent systems and their fundamental building blocks.

---

### 2. Agent Communication Patterns
**Duration**: 40-50 minutes
**Topics**:
- Point-to-Point messaging
- Broadcast communication
- Publish-Subscribe pattern
- Request-Reply protocol
- Blackboard pattern
- Visualizing communication flows

**Key Takeaways**: Learn different ways agents can communicate and when to use each pattern.

---

### 3. Orchestration Strategies
**Duration**: 45-60 minutes
**Topics**:
- Sequential orchestration (pipelines)
- Parallel orchestration (concurrent execution)
- Hierarchical orchestration (supervisor pattern)
- Dynamic orchestration (adaptive routing)
- Comparison and decision framework

**Key Takeaways**: Master different strategies for coordinating multiple agents.

---

### 4. Hands-On with LangGraph
**Duration**: 60-75 minutes
**Topics**:
- LangGraph fundamentals (state graphs, nodes, edges)
- Building sequential agent chains
- Conditional routing
- Supervisor pattern implementation
- Real-world example: Research assistant system

**Key Takeaways**: Build production-ready multi-agent systems using modern frameworks.

---

## 🛠️ Technologies Used

### Core Frameworks
- **LangGraph**: State-based agent orchestration
- **LangChain**: LLM integration and tooling
- **AutoGen**: Alternative multi-agent framework (examples included)
- **CrewAI**: Role-based multi-agent systems (examples included)

### Visualization
- **NetworkX**: Graph-based visualizations
- **Matplotlib**: Static plots
- **Plotly**: Interactive diagrams
- **Graphviz**: Agent flow diagrams

### Optional
- **Ollama**: Local LLM support
- **OpenAI API**: Cloud LLM integration

## 📊 Key Features

### Interactive Visualizations
All notebooks include rich visualizations:
- Agent interaction graphs
- Communication flow diagrams (Sankey)
- Timeline views of agent activities
- Heatmaps of agent interactions
- Orchestration pattern diagrams

### Hands-On Exercises
Each notebook includes practical exercises to reinforce learning:
- Design your own agent system
- Implement communication protocols
- Choose optimal orchestration strategies
- Build complete multi-agent applications

### Production-Ready Patterns
Learn patterns you can use in real projects:
- Error handling and retry logic
- State management
- Agent coordination
- Result aggregation
- Monitoring and debugging

## 🎓 Learning Path

We recommend following this learning path:

1. **Beginner** (2-3 hours):
   - Start with Notebook 1 (Introduction)
   - Complete exercises in Notebook 2 (Communication)
   - Experiment with visualization functions

2. **Intermediate** (3-4 hours):
   - Study Notebook 3 (Orchestration)
   - Build the examples in Notebook 4 (LangGraph)
   - Modify examples to solve your own problems

3. **Advanced** (4+ hours):
   - Integrate real LLMs (OpenAI or local)
   - Build a complete multi-agent project
   - Experiment with AutoGen and CrewAI
   - Contribute improvements back to this repo!

## 🔧 Troubleshooting

### Jupyter kernel issues
```bash
python -m ipykernel install --user --name=swarm-env
```

### Import errors
```bash
# Make sure you're in the right directory
cd swarm-of-agents
# Reinstall requirements
pip install -r requirements.txt --upgrade
```

### Visualization not showing
```bash
# For Jupyter Notebook
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension

# For Jupyter Lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs**: Open an issue describing the problem
2. **Suggest improvements**: Share ideas for new examples or explanations
3. **Add examples**: Submit PRs with new agent patterns or use cases
4. **Improve documentation**: Help make the notebooks clearer

## 📚 Additional Resources

### Papers & Research
- [Multi-Agent Systems: A Survey](https://arxiv.org/abs/2309.02427)
- [LangChain Multi-Agent Systems](https://python.langchain.com/docs/use_cases/agent_workflows)

### Frameworks
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [CrewAI Documentation](https://docs.crewai.com/)

### Courses
- [Stanford CS336: Language Modeling from Scratch](https://stanford-cs336.github.io/)
- [DeepLearning.AI: Multi AI Agent Systems](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)

## 📝 Citation

If you use this repository in your research or presentations, please cite:

```bibtex
@misc{swarm-of-agents-2024,
  title={Orchestrating Autonomy: A Deep Dive into Designing Multi-Agent AI Systems},
  author={Your Name},
  year={2024},
  publisher={GitHub},
  url={https://github.com/YOUR_USERNAME/swarm-of-agents}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Stanford CS336](https://stanford-cs336.github.io/) interactive learning approach
- Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain)
- Visualization techniques adapted from network science literature
- Community contributions from multi-agent AI researchers

## 📬 Contact

For questions, feedback, or collaboration opportunities:
- Open an [Issue](https://github.com/YOUR_USERNAME/swarm-of-agents/issues)
- Discussions: Use [GitHub Discussions](https://github.com/YOUR_USERNAME/swarm-of-agents/discussions)

---

**Happy Learning!** 🚀 Build amazing multi-agent systems!