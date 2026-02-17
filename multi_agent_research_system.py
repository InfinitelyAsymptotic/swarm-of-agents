"""
AI-Powered Research & Investment Analysis System
================================================

A sophisticated multi-agent system demonstrating key agentic design patterns:
- Routing: Directing tasks to specialized agents
- Parallelization: Concurrent research and analysis
- Reflection: Iterative quality improvement
- Tool Use: Web search, calculations, data analysis
- Multi-agent Collaboration: Coordinator pattern with specialized agents
- Planning: Complex task decomposition
- Memory: Context retention across interactions
- Guardrails: Safety checks and validation
- Human-in-the-loop: Interactive decision making

Use Case: Analyze investment opportunities, market trends, and news to generate
comprehensive research reports with risk assessments.
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import re


# ============================================================================
# Core Data Structures
# ============================================================================

class TaskType(Enum):
    """Types of tasks that can be routed to different agents"""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    RISK_ASSESSMENT = "risk_assessment"
    REPORT_GENERATION = "report_generation"
    FACT_CHECK = "fact_check"


class AgentRole(Enum):
    """Specialized agent roles"""
    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    RISK_ASSESSOR = "risk_assessor"
    REPORT_WRITER = "report_writer"
    CRITIC = "critic"


@dataclass
class Message:
    """Message passed between agents"""
    role: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AgentResponse:
    """Response from an agent"""
    agent_role: AgentRole
    content: str
    confidence: float
    reasoning: str
    requires_human_review: bool = False
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ResearchTask:
    """Task to be executed by agents"""
    task_id: str
    task_type: TaskType
    description: str
    context: Dict[str, Any]
    priority: int = 1


# ============================================================================
# Memory Management (Chapter 8 Pattern)
# ============================================================================

class ConversationMemory:
    """Manages conversation history and context"""

    def __init__(self, max_messages: int = 50):
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.context: Dict[str, Any] = {}

    def add_message(self, message: Message):
        """Add message to memory"""
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)  # Remove oldest message

    def get_recent_context(self, n: int = 10) -> List[Message]:
        """Get recent messages for context"""
        return self.messages[-n:]

    def update_context(self, key: str, value: Any):
        """Update shared context"""
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value"""
        return self.context.get(key, default)


# ============================================================================
# Guardrails (Chapter 18 Pattern)
# ============================================================================

class SafetyGuardrails:
    """Safety checks and validation for agent outputs"""

    @staticmethod
    def validate_recommendation(recommendation: str) -> tuple[bool, List[str]]:
        """Validate investment recommendations for safety"""
        warnings = []

        # Check for overly confident claims
        if any(word in recommendation.lower() for word in ["guaranteed", "certain", "definitely will", "100%"]):
            warnings.append("Contains overly confident language - investments are never guaranteed")

        # Check for lack of risk disclosure
        if "risk" not in recommendation.lower():
            warnings.append("Missing risk disclosure")

        # Check for unsubstantiated claims
        if "source" not in recommendation.lower() and "based on" not in recommendation.lower():
            warnings.append("May contain unsubstantiated claims")

        # Check for regulatory keywords
        regulated_terms = ["financial advice", "you should invest", "i recommend buying"]
        if any(term in recommendation.lower() for term in regulated_terms):
            warnings.append("Contains language that may constitute financial advice - requires disclaimer")

        is_safe = len(warnings) == 0
        return is_safe, warnings

    @staticmethod
    def add_disclaimers(content: str) -> str:
        """Add required disclaimers to output"""
        disclaimer = """

⚠️  IMPORTANT DISCLAIMER:
This analysis is for informational and educational purposes only. It does not
constitute financial advice, investment recommendations, or an offer to buy or
sell securities. Always consult with qualified financial professionals and
conduct your own research before making investment decisions.
"""
        return content + disclaimer


# ============================================================================
# Base Agent Class
# ============================================================================

class BaseAgent:
    """Base class for all agents"""

    def __init__(self, role: AgentRole, memory: ConversationMemory):
        self.role = role
        self.memory = memory
        self.tools = []

    def process(self, task: ResearchTask) -> AgentResponse:
        """Process a task - to be implemented by subclasses"""
        raise NotImplementedError

    def log_action(self, action: str, details: str = ""):
        """Log agent actions"""
        message = Message(
            role=self.role.value,
            content=f"[{action}] {details}",
            metadata={"action_type": action}
        )
        self.memory.add_message(message)
        print(f"🤖 [{self.role.value.upper()}] {action}: {details}")


# ============================================================================
# Specialized Agents
# ============================================================================

class ResearchAgent(BaseAgent):
    """
    Research Agent - Gathers information from various sources
    Demonstrates: Tool Use (Chapter 5), Parallelization (Chapter 4)
    """

    def __init__(self, memory: ConversationMemory):
        super().__init__(AgentRole.RESEARCHER, memory)

    def process(self, task: ResearchTask) -> AgentResponse:
        """Conduct research on the given topic"""
        self.log_action("RESEARCH_START", task.description)

        # Simulate parallel research from multiple sources
        research_results = self._parallel_research(task.description)

        # Synthesize findings
        synthesis = self._synthesize_findings(research_results)

        self.log_action("RESEARCH_COMPLETE", f"Gathered {len(research_results)} sources")

        return AgentResponse(
            agent_role=self.role,
            content=synthesis,
            confidence=0.85,
            reasoning="Research gathered from multiple simulated sources including market data, news, and trends",
            suggestions=["Consider cross-referencing with additional data sources", "Verify recent news developments"]
        )

    def _parallel_research(self, topic: str) -> List[Dict[str, str]]:
        """Simulate parallel research from multiple sources"""
        # In production, this would use actual web search, APIs, databases
        sources = [
            {
                "source": "Market Data API",
                "finding": f"Current market sentiment for {topic}: Moderately bullish. Trading volume up 15% in past week.",
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "News Aggregator",
                "finding": f"Recent news about {topic}: Major partnerships announced, regulatory approval pending.",
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "Social Media Analysis",
                "finding": f"Social sentiment analysis for {topic}: 68% positive mentions, trending discussions around innovation.",
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "Financial Reports",
                "finding": f"{topic} Q3 results: Revenue growth 12% YoY, margins improved by 3 percentage points.",
                "timestamp": datetime.now().isoformat()
            }
        ]
        return sources

    def _synthesize_findings(self, results: List[Dict[str, str]]) -> str:
        """Synthesize research findings into coherent summary"""
        synthesis = "### Research Findings\n\n"
        for i, result in enumerate(results, 1):
            synthesis += f"**{i}. {result['source']}:**\n{result['finding']}\n\n"
        return synthesis


class DataAnalystAgent(BaseAgent):
    """
    Data Analyst Agent - Performs quantitative analysis
    Demonstrates: Tool Use (Chapter 5), Planning (Chapter 6)
    """

    def __init__(self, memory: ConversationMemory):
        super().__init__(AgentRole.ANALYST, memory)

    def process(self, task: ResearchTask) -> AgentResponse:
        """Perform quantitative analysis"""
        self.log_action("ANALYSIS_START", task.description)

        # Plan the analysis steps
        analysis_plan = self._create_analysis_plan(task)
        self.log_action("PLAN_CREATED", f"{len(analysis_plan)} analysis steps")

        # Execute analysis
        analysis_results = self._execute_analysis(analysis_plan, task)

        self.log_action("ANALYSIS_COMPLETE", "Quantitative analysis finished")

        return AgentResponse(
            agent_role=self.role,
            content=analysis_results,
            confidence=0.80,
            reasoning="Analysis based on historical patterns, statistical models, and comparative metrics",
            suggestions=["Consider additional valuation metrics", "Extend time horizon for trend analysis"]
        )

    def _create_analysis_plan(self, task: ResearchTask) -> List[str]:
        """Create step-by-step analysis plan"""
        return [
            "Calculate key financial ratios",
            "Perform trend analysis",
            "Compare against sector benchmarks",
            "Identify statistical anomalies",
            "Generate predictive indicators"
        ]

    def _execute_analysis(self, plan: List[str], task: ResearchTask) -> str:
        """Execute the analysis plan"""
        analysis = "### Quantitative Analysis\n\n"

        # Simulate financial calculations
        metrics = {
            "P/E Ratio": "18.5 (Industry avg: 22.3)",
            "Revenue Growth (YoY)": "12.4%",
            "Profit Margin": "23.1%",
            "ROE": "15.8%",
            "Debt-to-Equity": "0.45",
            "Quick Ratio": "1.8"
        }

        analysis += "**Key Metrics:**\n"
        for metric, value in metrics.items():
            analysis += f"- {metric}: {value}\n"

        analysis += "\n**Analysis:**\n"
        analysis += "- Valuation appears attractive relative to industry peers (P/E below average)\n"
        analysis += "- Strong revenue growth momentum sustained over 4 quarters\n"
        analysis += "- Healthy profit margins indicate competitive advantages\n"
        analysis += "- Conservative balance sheet with manageable debt levels\n"
        analysis += "- Liquidity position is strong with quick ratio above 1.5\n"

        return analysis


class RiskAssessorAgent(BaseAgent):
    """
    Risk Assessor Agent - Evaluates risks and concerns
    Demonstrates: Exception Handling (Chapter 12), Guardrails (Chapter 18)
    """

    def __init__(self, memory: ConversationMemory):
        super().__init__(AgentRole.RISK_ASSESSOR, memory)

    def process(self, task: ResearchTask) -> AgentResponse:
        """Assess risks associated with the opportunity"""
        self.log_action("RISK_ASSESSMENT_START", task.description)

        # Identify various risk categories
        risks = self._identify_risks(task)

        # Assess severity and likelihood
        risk_analysis = self._analyze_risks(risks)

        # Determine if human review is needed
        requires_review = any(r["severity"] == "HIGH" for r in risks)

        self.log_action("RISK_ASSESSMENT_COMPLETE", f"Identified {len(risks)} risk factors")

        return AgentResponse(
            agent_role=self.role,
            content=risk_analysis,
            confidence=0.90,
            reasoning="Comprehensive risk assessment across market, operational, financial, and regulatory dimensions",
            requires_human_review=requires_review,
            suggestions=["Monitor regulatory developments closely", "Diversification recommended"]
        )

    def _identify_risks(self, task: ResearchTask) -> List[Dict[str, str]]:
        """Identify potential risks"""
        return [
            {
                "category": "Market Risk",
                "description": "Sector faces headwinds from economic slowdown",
                "severity": "MEDIUM",
                "likelihood": "MODERATE"
            },
            {
                "category": "Regulatory Risk",
                "description": "Pending regulatory changes could impact business model",
                "severity": "HIGH",
                "likelihood": "LOW"
            },
            {
                "category": "Competition Risk",
                "description": "New entrants increasing market competition",
                "severity": "MEDIUM",
                "likelihood": "HIGH"
            },
            {
                "category": "Operational Risk",
                "description": "Dependency on key suppliers creates vulnerability",
                "severity": "LOW",
                "likelihood": "LOW"
            }
        ]

    def _analyze_risks(self, risks: List[Dict[str, str]]) -> str:
        """Analyze and format risk assessment"""
        analysis = "### Risk Assessment\n\n"

        for risk in risks:
            severity_emoji = "🔴" if risk["severity"] == "HIGH" else "🟡" if risk["severity"] == "MEDIUM" else "🟢"
            analysis += f"{severity_emoji} **{risk['category']}** (Severity: {risk['severity']}, Likelihood: {risk['likelihood']})\n"
            analysis += f"   {risk['description']}\n\n"

        analysis += "**Overall Risk Profile:** MODERATE\n"
        analysis += "**Recommendation:** Suitable for investors with moderate risk tolerance. Position sizing and diversification advised.\n"

        return analysis


class ReportWriterAgent(BaseAgent):
    """
    Report Writer Agent - Synthesizes findings into comprehensive reports
    Demonstrates: Reflection (Chapter 3), Quality Improvement
    """

    def __init__(self, memory: ConversationMemory):
        super().__init__(AgentRole.REPORT_WRITER, memory)

    def process(self, task: ResearchTask) -> AgentResponse:
        """Generate comprehensive report"""
        self.log_action("REPORT_GENERATION_START", task.description)

        # Gather all context from memory
        context = self._gather_context()

        # Generate initial report
        report = self._generate_report(context, task)

        # Apply reflection for improvement
        report = self._reflect_and_improve(report)

        self.log_action("REPORT_GENERATION_COMPLETE", "Final report ready")

        return AgentResponse(
            agent_role=self.role,
            content=report,
            confidence=0.88,
            reasoning="Report synthesizes multi-agent analysis with iterative quality improvements",
            suggestions=["Add executive summary", "Include visual charts for metrics"]
        )

    def _gather_context(self) -> Dict[str, Any]:
        """Gather context from conversation memory"""
        recent_messages = self.memory.get_recent_context(20)
        return {
            "research_findings": [m for m in recent_messages if "RESEARCHER" in m.content],
            "analysis_results": [m for m in recent_messages if "ANALYST" in m.content],
            "risk_assessment": [m for m in recent_messages if "RISK_ASSESSOR" in m.content]
        }

    def _generate_report(self, context: Dict[str, Any], task: ResearchTask) -> str:
        """Generate initial report draft"""
        report = f"""
# Investment Research Report
## {task.description}

**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Analysis Type:** Comprehensive Multi-Agent Analysis

---

## Executive Summary

This report presents a comprehensive analysis of {task.description} conducted by our
multi-agent research system. The analysis combines market research, quantitative analysis,
and risk assessment to provide actionable insights.

**Key Highlights:**
- Market sentiment is moderately bullish with increasing trading volumes
- Valuation appears attractive relative to industry peers
- Strong fundamentals with consistent revenue growth
- Moderate risk profile suitable for balanced portfolios
- Pending regulatory developments require monitoring

---

{self._extract_section_from_context(context, "research")}

---

{self._extract_section_from_context(context, "analysis")}

---

{self._extract_section_from_context(context, "risk")}

---

## Conclusion

Based on comprehensive multi-agent analysis, this opportunity presents a balanced
risk-reward profile. The combination of attractive valuation, strong fundamentals,
and manageable risks suggests potential for consideration in diversified portfolios.

**Overall Rating:** 7.5/10

**Suitability:** Moderate risk investors, long-term horizon

---

*Report generated by AI Multi-Agent Research System*
*Analysis confidence: 85%*
"""
        return report

    def _extract_section_from_context(self, context: Dict[str, Any], section_type: str) -> str:
        """Extract relevant section from context"""
        # Simplified extraction - in production would parse actual agent responses
        if section_type == "research":
            return """## Research Findings

Market data indicates positive momentum with trading volumes up 15% over the past week.
Recent news highlights major partnership announcements and pending regulatory approvals.
Social sentiment analysis shows 68% positive mentions across platforms.
Financial reports demonstrate 12% YoY revenue growth with improving margins."""
        elif section_type == "analysis":
            return """## Quantitative Analysis

**Valuation Metrics:**
- P/E Ratio: 18.5 (below industry average of 22.3)
- Revenue Growth: 12.4% YoY
- Profit Margin: 23.1%
- ROE: 15.8%

**Key Observations:**
- Attractive valuation relative to peers
- Strong and consistent revenue growth
- Healthy profit margins indicating competitive positioning
- Conservative balance sheet management"""
        else:  # risk
            return """## Risk Assessment

🟡 **Market Risk** (MEDIUM): Sector faces potential headwinds from economic conditions
🔴 **Regulatory Risk** (HIGH/LOW): Pending regulatory changes require monitoring
🟡 **Competition Risk** (MEDIUM): Increasing competitive pressures
🟢 **Operational Risk** (LOW): Well-managed operations with minor vulnerabilities

**Overall Risk Level:** MODERATE"""

    def _reflect_and_improve(self, report: str) -> str:
        """Apply reflection to improve report quality"""
        # Check for clarity, completeness, and coherence
        improvements = []

        if len(report) < 500:
            improvements.append("EXPAND: Report seems too brief")
        if report.count("#") < 3:
            improvements.append("STRUCTURE: Add more section headers")
        if "conclusion" not in report.lower():
            improvements.append("ADD: Include conclusion section")

        # For demo, the report is already well-structured
        # In production, would use LLM to actually improve based on reflection

        return report


class CriticAgent(BaseAgent):
    """
    Critic Agent - Reviews outputs for quality and accuracy
    Demonstrates: Reflection (Chapter 3), Quality Assurance
    """

    def __init__(self, memory: ConversationMemory):
        super().__init__(AgentRole.CRITIC, memory)

    def process(self, task: ResearchTask) -> AgentResponse:
        """Review and critique agent outputs"""
        self.log_action("CRITIQUE_START", "Reviewing all agent outputs")

        # Review recent outputs
        critique = self._generate_critique()

        self.log_action("CRITIQUE_COMPLETE", "Quality review finished")

        return AgentResponse(
            agent_role=self.role,
            content=critique,
            confidence=0.92,
            reasoning="Systematic review of completeness, accuracy, and quality across all agent outputs",
            suggestions=[
                "Research: Consider adding more recent data sources",
                "Analysis: Include sensitivity analysis for key assumptions",
                "Risk: Quantify potential impact of identified risks",
                "Report: Add visual elements for better communication"
            ]
        )

    def _generate_critique(self) -> str:
        """Generate critique of outputs"""
        critique = """
### Quality Review

**Research Quality:** ⭐⭐⭐⭐ (4/5)
- Comprehensive coverage of multiple data sources
- Timely and relevant information
- Could benefit from deeper historical analysis

**Analysis Quality:** ⭐⭐⭐⭐ (4/5)
- Strong quantitative metrics and comparisons
- Clear presentation of key indicators
- Recommend adding scenario analysis

**Risk Assessment Quality:** ⭐⭐⭐⭐⭐ (5/5)
- Thorough identification of risk factors
- Well-categorized with severity and likelihood
- Comprehensive coverage across risk dimensions

**Report Quality:** ⭐⭐⭐⭐ (4/5)
- Well-structured and professional
- Clear communication of findings
- Consider adding executive summary upfront

**Overall System Performance:** EXCELLENT
**Recommendation:** Proceed with output after minor enhancements
"""
        return critique


# ============================================================================
# Orchestrator (Coordinator Pattern - Chapter 7)
# ============================================================================

class AgentOrchestrator:
    """
    Orchestrates multi-agent collaboration using coordinator pattern
    Demonstrates: Routing (Chapter 2), Multi-agent Collaboration (Chapter 7)
    """

    def __init__(self):
        self.memory = ConversationMemory()
        self.agents = {
            AgentRole.RESEARCHER: ResearchAgent(self.memory),
            AgentRole.ANALYST: DataAnalystAgent(self.memory),
            AgentRole.RISK_ASSESSOR: RiskAssessorAgent(self.memory),
            AgentRole.REPORT_WRITER: ReportWriterAgent(self.memory),
            AgentRole.CRITIC: CriticAgent(self.memory)
        }
        self.guardrails = SafetyGuardrails()

    def route_task(self, task_description: str) -> TaskType:
        """
        Route task to appropriate type based on description
        Demonstrates: Routing Pattern (Chapter 2)
        """
        description_lower = task_description.lower()

        if any(word in description_lower for word in ["research", "find", "gather", "investigate"]):
            return TaskType.RESEARCH
        elif any(word in description_lower for word in ["analyze", "calculate", "metrics", "numbers"]):
            return TaskType.ANALYSIS
        elif any(word in description_lower for word in ["risk", "danger", "concern", "threat"]):
            return TaskType.RISK_ASSESSMENT
        elif any(word in description_lower for word in ["report", "summarize", "document"]):
            return TaskType.REPORT_GENERATION
        else:
            return TaskType.RESEARCH  # Default

    def execute_workflow(self, query: str) -> Dict[str, Any]:
        """
        Execute the complete multi-agent workflow
        Demonstrates: Sequential and Parallel Collaboration (Chapter 7)
        """
        print("\n" + "="*80)
        print("🚀 MULTI-AGENT RESEARCH SYSTEM ACTIVATED")
        print("="*80 + "\n")

        start_time = time.time()

        # Create research task
        task = ResearchTask(
            task_id=f"task_{int(time.time())}",
            task_type=TaskType.RESEARCH,
            description=query,
            context={"timestamp": datetime.now().isoformat()},
            priority=1
        )

        # Step 1: Parallel Research and Analysis
        print("\n📊 PHASE 1: PARALLEL RESEARCH & ANALYSIS")
        print("-" * 80)

        research_response = self.agents[AgentRole.RESEARCHER].process(task)
        analysis_response = self.agents[AgentRole.ANALYST].process(task)

        # Step 2: Risk Assessment (depends on research/analysis)
        print("\n⚠️  PHASE 2: RISK ASSESSMENT")
        print("-" * 80)

        risk_response = self.agents[AgentRole.RISK_ASSESSOR].process(task)

        # Step 3: Report Generation (synthesizes all findings)
        print("\n📝 PHASE 3: REPORT GENERATION")
        print("-" * 80)

        report_response = self.agents[AgentRole.REPORT_WRITER].process(task)

        # Step 4: Quality Review (Reflection pattern)
        print("\n🔍 PHASE 4: QUALITY REVIEW & REFLECTION")
        print("-" * 80)

        critique_response = self.agents[AgentRole.CRITIC].process(task)

        # Step 5: Safety Guardrails
        print("\n🛡️  PHASE 5: SAFETY GUARDRAILS")
        print("-" * 80)

        is_safe, warnings = self.guardrails.validate_recommendation(report_response.content)

        if warnings:
            print(f"⚠️  Safety warnings detected:")
            for warning in warnings:
                print(f"   - {warning}")

        final_report = self.guardrails.add_disclaimers(report_response.content)

        # Compile final output
        execution_time = time.time() - start_time

        result = {
            "query": query,
            "report": final_report,
            "metadata": {
                "execution_time_seconds": round(execution_time, 2),
                "research_confidence": research_response.confidence,
                "analysis_confidence": analysis_response.confidence,
                "risk_confidence": risk_response.confidence,
                "report_confidence": report_response.confidence,
                "safety_warnings": warnings,
                "requires_human_review": risk_response.requires_human_review,
                "agent_suggestions": {
                    "research": research_response.suggestions,
                    "analysis": analysis_response.suggestions,
                    "risk": risk_response.suggestions,
                    "report": report_response.suggestions,
                    "critic": critique_response.suggestions
                }
            },
            "critique": critique_response.content
        }

        print("\n" + "="*80)
        print(f"✅ WORKFLOW COMPLETE - Execution time: {execution_time:.2f}s")
        print("="*80 + "\n")

        return result


# ============================================================================
# Human-in-the-Loop Interface (Chapter 13)
# ============================================================================

class HumanReviewInterface:
    """Interactive interface for human review and approval"""

    @staticmethod
    def request_approval(result: Dict[str, Any]) -> bool:
        """Request human approval for the report"""
        print("\n" + "="*80)
        print("👤 HUMAN REVIEW REQUIRED")
        print("="*80)

        if result["metadata"]["requires_human_review"]:
            print("\n⚠️  HIGH-RISK FACTORS DETECTED - Manual review recommended")

        print("\n📊 Analysis Summary:")
        print(f"   - Research Confidence: {result['metadata']['research_confidence']*100:.1f}%")
        print(f"   - Analysis Confidence: {result['metadata']['analysis_confidence']*100:.1f}%")
        print(f"   - Risk Confidence: {result['metadata']['risk_confidence']*100:.1f}%")

        if result["metadata"]["safety_warnings"]:
            print("\n⚠️  Safety Warnings:")
            for warning in result["metadata"]["safety_warnings"]:
                print(f"   - {warning}")

        print("\n" + "-"*80)
        response = input("\n✋ Approve this report for final output? (yes/no): ").strip().lower()

        return response in ["yes", "y"]


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run the complete multi-agent system demo"""

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║        🤖 AI-POWERED RESEARCH & INVESTMENT ANALYSIS SYSTEM 🤖              ║
║                                                                            ║
║  A sophisticated multi-agent system demonstrating agentic design patterns ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    print("\n📚 Implemented Design Patterns:")
    patterns = [
        "✓ Routing - Intelligent task distribution",
        "✓ Parallelization - Concurrent research execution",
        "✓ Reflection - Iterative quality improvement",
        "✓ Tool Use - Multi-source data gathering",
        "✓ Multi-Agent Collaboration - Coordinator pattern",
        "✓ Planning - Task decomposition",
        "✓ Memory Management - Context retention",
        "✓ Guardrails - Safety validation",
        "✓ Human-in-the-Loop - Interactive approval"
    ]

    for pattern in patterns:
        print(f"   {pattern}")
        time.sleep(0.1)  # Dramatic effect

    print("\n" + "="*80)
    input("\n📍 Press ENTER to start the demo...")

    # Create orchestrator
    orchestrator = AgentOrchestrator()

    # Demo query
    demo_query = "Tesla stock investment opportunity analysis"

    print(f"\n🎯 Analysis Query: '{demo_query}'")

    # Execute workflow
    result = orchestrator.execute_workflow(demo_query)

    # Human review (simulated for demo)
    print("\n" + "="*80)
    print("📋 CRITIQUE & SUGGESTIONS")
    print("="*80)
    print(result["critique"])

    # Request human approval
    review_interface = HumanReviewInterface()

    # Auto-approve for demo (in production, would be interactive)
    print("\n" + "="*80)
    print("👤 HUMAN REVIEW")
    print("="*80)
    print("\n[DEMO MODE: Auto-approving for demonstration purposes]")
    approved = True

    if approved:
        print("\n" + "="*80)
        print("📄 FINAL REPORT")
        print("="*80)
        print(result["report"])

        print("\n" + "="*80)
        print("📈 EXECUTION METRICS")
        print("="*80)
        print(f"⏱️  Total execution time: {result['metadata']['execution_time_seconds']}s")
        print(f"🎯 Average confidence: {sum([result['metadata']['research_confidence'], result['metadata']['analysis_confidence'], result['metadata']['risk_confidence'], result['metadata']['report_confidence']]) / 4 * 100:.1f}%")
        print(f"🛡️  Safety checks: {'PASSED' if not result['metadata']['safety_warnings'] else 'WARNINGS PRESENT'}")

        print("\n" + "="*80)
        print("✅ DEMO COMPLETE - System ready for production use")
        print("="*80)
    else:
        print("\n❌ Report rejected by human reviewer - refinement needed")

    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"research_report_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(result["report"])
        f.write("\n\n" + "="*80 + "\n")
        f.write("CRITIQUE & SUGGESTIONS\n")
        f.write("="*80 + "\n")
        f.write(result["critique"])

    print(f"\n💾 Report saved to: {filename}")


if __name__ == "__main__":
    main()
