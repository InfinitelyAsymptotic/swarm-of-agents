#!/usr/bin/env python3
"""
Production-Ready Multi-Agent System Demo using OpenAI API

This demo showcases a complete research and content creation pipeline
with 5 specialized agents working together.

Agents:
1. Coordinator: Orchestrates the workflow
2. Researcher: Gathers information and insights
3. Writer: Creates content based on research
4. Critic: Reviews and provides feedback
5. Editor: Finalizes and polishes content

Author: Pranjal
Demo for: Google Developer Conference - Multi-Agent AI Systems Talk
"""

import os
import sys
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import openai
from openai import OpenAI


# ============================================================================
# Configuration and Setup
# ============================================================================

class AgentRole(Enum):
    """Enum for agent roles."""
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    WRITER = "writer"
    CRITIC = "critic"
    EDITOR = "editor"


@dataclass
class Message:
    """Represents a message between agents."""
    sender: str
    recipient: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentState:
    """Tracks the state of an agent."""
    name: str
    role: AgentRole
    status: str = "idle"  # idle, thinking, working, completed
    messages_received: int = 0
    messages_sent: int = 0
    last_activity: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================================
# Agent Base Class
# ============================================================================

class Agent:
    """
    Base Agent class with OpenAI integration.

    Each agent has:
    - A specialized system prompt
    - Conversation history
    - Error handling with retries
    - Activity logging
    """

    def __init__(
        self,
        name: str,
        role: AgentRole,
        system_prompt: str,
        client: OpenAI,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_retries: int = 3
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries

        self.state = AgentState(name=name, role=role)
        self.message_history: List[Message] = []
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]

    def receive_message(self, message: Message) -> None:
        """Receive and log a message."""
        self.message_history.append(message)
        self.state.messages_received += 1
        self.state.last_activity = datetime.now().isoformat()

    def _call_openai(self, user_message: str) -> str:
        """
        Call OpenAI API with retry logic and error handling.

        This is production-ready with:
        - Exponential backoff
        - Rate limit handling
        - Error recovery
        """
        self.conversation_history.append({"role": "user", "content": user_message})

        for attempt in range(self.max_retries):
            try:
                self.state.status = "thinking"

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=self.temperature,
                    max_tokens=2000
                )

                assistant_message = response.choices[0].message.content
                self.conversation_history.append(
                    {"role": "assistant", "content": assistant_message}
                )

                self.state.status = "completed"
                return assistant_message

            except openai.RateLimitError as e:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️  [{self.name}] Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)

            except openai.APIError as e:
                print(f"⚠️  [{self.name}] API error: {e}. Retrying...")
                time.sleep(1)

            except Exception as e:
                print(f"❌ [{self.name}] Unexpected error: {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise Exception(f"Failed after {self.max_retries} attempts")

    def process(self, task: str, context: Optional[str] = None) -> str:
        """
        Process a task and return the result.

        Args:
            task: The task description
            context: Optional context from previous agents

        Returns:
            The agent's response
        """
        self.state.status = "working"

        # Build the prompt with context if provided
        if context:
            prompt = f"Context from previous agents:\n{context}\n\nYour task:\n{task}"
        else:
            prompt = task

        # Call OpenAI
        result = self._call_openai(prompt)

        # Update state
        self.state.messages_sent += 1
        self.state.last_activity = datetime.now().isoformat()

        return result

    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "name": self.name,
            "role": self.role.value,
            "status": self.state.status,
            "messages_received": self.state.messages_received,
            "messages_sent": self.state.messages_sent,
            "total_messages": len(self.message_history)
        }


# ============================================================================
# Specialized Agents
# ============================================================================

class CoordinatorAgent(Agent):
    """
    Coordinator Agent: Orchestrates the workflow.
    """

    def __init__(self, client: OpenAI):
        super().__init__(
            name="Coordinator",
            role=AgentRole.COORDINATOR,
            system_prompt="""You are the Coordinator Agent in a multi-agent system.

Your responsibilities:
1. Break down complex tasks into subtasks
2. Assign tasks to specialized agents
3. Ensure smooth workflow between agents
4. Provide clear, actionable instructions

Be concise and directive. Output only the essential information needed by other agents.""",
            client=client,
            temperature=0.3  # Lower temperature for consistency
        )


class ResearcherAgent(Agent):
    """
    Researcher Agent: Gathers information and insights.
    """

    def __init__(self, client: OpenAI):
        super().__init__(
            name="Researcher",
            role=AgentRole.RESEARCHER,
            system_prompt="""You are the Researcher Agent in a multi-agent system.

Your responsibilities:
1. Gather relevant information on given topics
2. Provide key facts, statistics, and insights
3. Identify important trends and patterns
4. Structure information clearly for the Writer agent

Be thorough but concise. Focus on accuracy and relevance.
Format your research in clear bullet points or sections.""",
            client=client,
            temperature=0.7
        )


class WriterAgent(Agent):
    """
    Writer Agent: Creates content based on research.
    """

    def __init__(self, client: OpenAI):
        super().__init__(
            name="Writer",
            role=AgentRole.WRITER,
            system_prompt="""You are the Writer Agent in a multi-agent system.

Your responsibilities:
1. Create engaging, well-structured content
2. Use research provided by the Researcher agent
3. Write in a clear, professional, yet engaging style
4. Ensure logical flow and coherence

Be creative but stay true to the research. Write content that is
informative, engaging, and well-organized.""",
            client=client,
            temperature=0.8  # Higher temperature for creativity
        )


class CriticAgent(Agent):
    """
    Critic Agent: Reviews content and provides feedback.
    """

    def __init__(self, client: OpenAI):
        super().__init__(
            name="Critic",
            role=AgentRole.CRITIC,
            system_prompt="""You are the Critic Agent in a multi-agent system.

Your responsibilities:
1. Review content critically but constructively
2. Identify strengths and weaknesses
3. Suggest specific improvements
4. Check for accuracy, clarity, and engagement

Be honest but helpful. Provide actionable feedback that the Editor
can use to improve the content. Format feedback in clear sections:
- Strengths
- Areas for Improvement
- Specific Suggestions""",
            client=client,
            temperature=0.5
        )


class EditorAgent(Agent):
    """
    Editor Agent: Finalizes and polishes content.
    """

    def __init__(self, client: OpenAI):
        super().__init__(
            name="Editor",
            role=AgentRole.EDITOR,
            system_prompt="""You are the Editor Agent in a multi-agent system.

Your responsibilities:
1. Incorporate feedback from the Critic
2. Polish and refine the content
3. Ensure consistency in style and tone
4. Produce the final, publication-ready version

Be meticulous. The output should be polished, professional, and
ready for publication. This is the final step.""",
            client=client,
            temperature=0.6
        )


# ============================================================================
# Multi-Agent Orchestrator
# ============================================================================

class MultiAgentOrchestrator:
    """
    Orchestrates the multi-agent workflow.

    Manages:
    - Agent creation and lifecycle
    - Message passing between agents
    - Workflow execution
    - Result aggregation
    """

    def __init__(self, api_key: str):
        """Initialize the orchestrator with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)

        # Create all agents
        self.agents = {
            "coordinator": CoordinatorAgent(self.client),
            "researcher": ResearcherAgent(self.client),
            "writer": WriterAgent(self.client),
            "critic": CriticAgent(self.client),
            "editor": EditorAgent(self.client)
        }

        self.execution_log: List[Dict[str, Any]] = []

    def log_step(self, agent_name: str, action: str, content: str):
        """Log an execution step."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "content": content[:200] + "..." if len(content) > 200 else content
        }
        self.execution_log.append(log_entry)

    def print_step(self, emoji: str, agent_name: str, message: str):
        """Print a step in the workflow."""
        print(f"\n{emoji} [{agent_name}] {message}")
        print("─" * 80)

    def execute_research_and_write_pipeline(
        self,
        topic: str,
        content_type: str = "blog post"
    ) -> Dict[str, Any]:
        """
        Execute the complete research and content creation pipeline.

        Args:
            topic: The topic to research and write about
            content_type: Type of content (blog post, article, report, etc.)

        Returns:
            Dictionary containing all outputs and statistics
        """
        print("\n" + "=" * 80)
        print("🚀 MULTI-AGENT CONTENT CREATION PIPELINE")
        print("=" * 80)
        print(f"📋 Topic: {topic}")
        print(f"📝 Content Type: {content_type}")
        print("=" * 80)

        start_time = time.time()
        results = {}

        # ====================================================================
        # Step 1: Coordinator plans the workflow
        # ====================================================================
        self.print_step("🎯", "Coordinator", "Planning workflow...")

        coordinator_task = f"""Plan a workflow to create a {content_type} about: {topic}

Provide:
1. Key research questions to investigate
2. Content structure outline
3. Success criteria"""

        plan = self.agents["coordinator"].process(coordinator_task)
        results["plan"] = plan
        self.log_step("coordinator", "planning", plan)

        print(plan[:300] + "..." if len(plan) > 300 else plan)

        # ====================================================================
        # Step 2: Researcher gathers information
        # ====================================================================
        self.print_step("🔍", "Researcher", "Gathering information...")

        research_task = f"""Research the following topic: {topic}

Based on this plan:
{plan}

Provide comprehensive research with:
- Key facts and insights
- Important trends
- Relevant examples
- Notable quotes or statistics"""

        research = self.agents["researcher"].process(research_task)
        results["research"] = research
        self.log_step("researcher", "researching", research)

        print(research[:300] + "..." if len(research) > 300 else research)

        # ====================================================================
        # Step 3: Writer creates initial content
        # ====================================================================
        self.print_step("✍️", "Writer", "Creating content...")

        writing_task = f"""Write a {content_type} about: {topic}

Use this research:
{research}

Follow this structure from the plan:
{plan}

Create engaging, well-structured content."""

        draft = self.agents["writer"].process(writing_task)
        results["draft"] = draft
        self.log_step("writer", "writing", draft)

        print(draft[:400] + "..." if len(draft) > 400 else draft)

        # ====================================================================
        # Step 4: Critic reviews the content
        # ====================================================================
        self.print_step("🔎", "Critic", "Reviewing content...")

        critic_task = f"""Review this {content_type}:

{draft}

Provide constructive feedback on:
- Strengths
- Areas for improvement
- Specific suggestions for enhancement"""

        feedback = self.agents["critic"].process(critic_task)
        results["feedback"] = feedback
        self.log_step("critic", "reviewing", feedback)

        print(feedback[:300] + "..." if len(feedback) > 300 else feedback)

        # ====================================================================
        # Step 5: Editor finalizes the content
        # ====================================================================
        self.print_step("📝", "Editor", "Finalizing content...")

        editing_task = f"""Finalize this {content_type}:

Original draft:
{draft}

Critic's feedback:
{feedback}

Incorporate the feedback and produce a polished, final version."""

        final_content = self.agents["editor"].process(editing_task)
        results["final_content"] = final_content
        self.log_step("editor", "finalizing", final_content)

        # ====================================================================
        # Execution complete
        # ====================================================================
        execution_time = time.time() - start_time

        print("\n" + "=" * 80)
        print("✅ PIPELINE EXECUTION COMPLETE")
        print("=" * 80)

        # Gather statistics
        stats = {
            "execution_time_seconds": round(execution_time, 2),
            "total_agents": len(self.agents),
            "agent_stats": {
                name: agent.get_stats()
                for name, agent in self.agents.items()
            }
        }

        results["statistics"] = stats
        results["execution_log"] = self.execution_log

        # Print statistics
        print(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
        print(f"🤖 Agents involved: {len(self.agents)}")
        print(f"📊 Total API calls: {sum(s['messages_sent'] for s in stats['agent_stats'].values())}")

        print("\n📈 Agent Statistics:")
        for name, agent_stats in stats['agent_stats'].items():
            print(f"  • {name.title()}: {agent_stats['messages_sent']} outputs generated")

        print("\n" + "=" * 80)
        print("📄 FINAL CONTENT")
        print("=" * 80)
        print(final_content)
        print("=" * 80)

        return results

    def save_results(self, results: Dict[str, Any], output_file: str = "demo_output.json"):
        """Save results to a JSON file."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")


# ============================================================================
# Main Demo Function
# ============================================================================

def run_demo():
    """Run the multi-agent demo."""

    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("\nPlease set it using:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)

    print("\n🔑 OpenAI API Key detected")

    # Create orchestrator
    orchestrator = MultiAgentOrchestrator(api_key)

    # Define the demo topic
    topic = "How Multi-Agent AI Systems Are Transforming Software Development"

    # Execute the pipeline
    results = orchestrator.execute_research_and_write_pipeline(
        topic=topic,
        content_type="technical blog post"
    )

    # Save results
    orchestrator.save_results(results)

    return results


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    try:
        results = run_demo()
        print("\n✨ Demo completed successfully!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
