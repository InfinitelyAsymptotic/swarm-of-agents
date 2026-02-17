"""
Non-interactive Demo of AI-Powered Research & Investment Analysis System
Automatically runs through the complete workflow without user prompts
"""

# Import the main system
from multi_agent_research_system import AgentOrchestrator
import time
from datetime import datetime


def run_automated_demo():
    """Run the complete demo without interactive prompts"""

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
        time.sleep(0.05)

    print("\n" + "="*80)
    print("\n🚀 Starting automated demo...\n")
    time.sleep(0.5)

    # Create orchestrator
    orchestrator = AgentOrchestrator()

    # Demo query
    demo_query = "Tesla stock investment opportunity analysis"

    print(f"\n🎯 Analysis Query: '{demo_query}'")
    time.sleep(0.5)

    # Execute workflow
    result = orchestrator.execute_workflow(demo_query)

    # Display critique
    print("\n" + "="*80)
    print("📋 CRITIQUE & SUGGESTIONS")
    print("="*80)
    print(result["critique"])

    # Auto-approve for demo
    print("\n" + "="*80)
    print("👤 HUMAN REVIEW")
    print("="*80)
    print("\n[DEMO MODE: Auto-approving for demonstration purposes]")
    time.sleep(0.5)

    # Display final report
    print("\n" + "="*80)
    print("📄 FINAL REPORT")
    print("="*80)
    print(result["report"])

    # Display metrics
    print("\n" + "="*80)
    print("📈 EXECUTION METRICS")
    print("="*80)
    print(f"⏱️  Total execution time: {result['metadata']['execution_time_seconds']}s")

    avg_confidence = sum([
        result['metadata']['research_confidence'],
        result['metadata']['analysis_confidence'],
        result['metadata']['risk_confidence'],
        result['metadata']['report_confidence']
    ]) / 4 * 100

    print(f"🎯 Average confidence: {avg_confidence:.1f}%")
    print(f"🛡️  Safety checks: {'PASSED' if not result['metadata']['safety_warnings'] else 'WARNINGS PRESENT'}")

    # Display agent suggestions
    print("\n" + "="*80)
    print("💡 AGENT IMPROVEMENT SUGGESTIONS")
    print("="*80)

    for agent_name, suggestions in result['metadata']['agent_suggestions'].items():
        if suggestions:
            print(f"\n{agent_name.upper()}:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")

    print("\n" + "="*80)
    print("✅ DEMO COMPLETE - System ready for production use")
    print("="*80)

    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"research_report_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write("="*80 + "\n")
        f.write("AI-POWERED RESEARCH & INVESTMENT ANALYSIS SYSTEM\n")
        f.write("="*80 + "\n\n")
        f.write(f"Query: {demo_query}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n" + "="*80 + "\n\n")
        f.write(result["report"])
        f.write("\n\n" + "="*80 + "\n")
        f.write("CRITIQUE & QUALITY REVIEW\n")
        f.write("="*80 + "\n")
        f.write(result["critique"])
        f.write("\n\n" + "="*80 + "\n")
        f.write("EXECUTION METADATA\n")
        f.write("="*80 + "\n")
        f.write(f"Execution time: {result['metadata']['execution_time_seconds']}s\n")
        f.write(f"Average confidence: {avg_confidence:.1f}%\n")
        f.write(f"Requires human review: {result['metadata']['requires_human_review']}\n")
        f.write(f"Safety warnings: {len(result['metadata']['safety_warnings'])}\n")

    print(f"\n💾 Full report saved to: {filename}")

    print("\n" + "="*80)
    print("🎬 DEMO STATISTICS")
    print("="*80)
    print(f"📊 Total agents involved: 5 (Researcher, Analyst, Risk Assessor, Report Writer, Critic)")
    print(f"⚡ Parallel operations: 2 (Research + Analysis)")
    print(f"🔄 Reflection loops: 1 (Critic review)")
    print(f"🛡️  Safety checks: 4 types (Language, Disclosure, Claims, Regulatory)")
    print(f"💬 Messages in memory: {len(orchestrator.memory.messages)}")
    print(f"📝 Report sections: 6 (Summary, Research, Analysis, Risk, Conclusion, Disclaimer)")

    return result


if __name__ == "__main__":
    result = run_automated_demo()
