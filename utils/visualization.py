"""Visualization utilities for multi-agent systems."""

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime


def visualize_agent_graph(
    agents: List[str],
    connections: List[Tuple[str, str]],
    node_colors: Optional[Dict[str, str]] = None,
    title: str = "Multi-Agent System Architecture"
) -> None:
    """
    Visualize agents and their connections as a directed graph.

    Args:
        agents: List of agent names
        connections: List of tuples (from_agent, to_agent)
        node_colors: Optional dict mapping agent names to colors
        title: Graph title
    """
    G = nx.DiGraph()
    G.add_nodes_from(agents)
    G.add_edges_from(connections)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Prepare node colors
    if node_colors:
        colors = [node_colors.get(node, '#3498db') for node in G.nodes()]
    else:
        colors = '#3498db'

    # Draw the graph
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=3000, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
        width=2,
        connectionstyle='arc3,rad=0.1'
    )

    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def visualize_communication_flow(
    messages: List[Dict],
    title: str = "Agent Communication Flow"
) -> None:
    """
    Visualize message flow between agents using an interactive Plotly Sankey diagram.

    Args:
        messages: List of dicts with 'from', 'to', and 'content' keys
        title: Diagram title
    """
    # Get unique agents
    agents = list(set([msg['from'] for msg in messages] + [msg['to'] for msg in messages]))
    agent_indices = {agent: i for i, agent in enumerate(agents)}

    # Prepare data for Sankey diagram
    source = [agent_indices[msg['from']] for msg in messages]
    target = [agent_indices[msg['to']] for msg in messages]
    value = [1] * len(messages)

    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=agents,
            color="#3498db"
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="rgba(52, 152, 219, 0.4)"
        )
    )])

    fig.update_layout(
        title_text=title,
        font_size=12,
        height=600
    )
    fig.show()


def create_agent_timeline(
    events: List[Dict],
    title: str = "Agent Activity Timeline"
) -> None:
    """
    Create a timeline visualization of agent activities.

    Args:
        events: List of dicts with 'agent', 'task', 'start', 'end' keys
        title: Timeline title
    """
    fig = go.Figure()

    for event in events:
        fig.add_trace(go.Scatter(
            x=[event['start'], event['end']],
            y=[event['agent'], event['agent']],
            mode='lines+markers',
            name=event['task'],
            line=dict(width=10),
            hovertemplate=f"<b>{event['agent']}</b><br>" +
                         f"Task: {event['task']}<br>" +
                         f"Duration: {event['start']} - {event['end']}<extra></extra>"
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Agent",
        height=400,
        showlegend=True,
        hovermode='closest'
    )
    fig.show()


def plot_agent_interactions(
    interaction_matrix: Dict[str, Dict[str, int]],
    title: str = "Agent Interaction Heatmap"
) -> None:
    """
    Plot a heatmap of agent interactions.

    Args:
        interaction_matrix: Nested dict {from_agent: {to_agent: count}}
        title: Heatmap title
    """
    agents = sorted(list(interaction_matrix.keys()))

    # Create matrix
    matrix = []
    for from_agent in agents:
        row = []
        for to_agent in agents:
            count = interaction_matrix.get(from_agent, {}).get(to_agent, 0)
            row.append(count)
        matrix.append(row)

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=agents,
        y=agents,
        colorscale='Blues',
        text=matrix,
        texttemplate="%{text}",
        textfont={"size": 12}
    ))

    fig.update_layout(
        title=title,
        xaxis_title="To Agent",
        yaxis_title="From Agent",
        height=500,
        width=500
    )
    fig.show()


def visualize_orchestration_pattern(
    pattern_type: str,
    agents: List[str],
    title: Optional[str] = None
) -> None:
    """
    Visualize different orchestration patterns.

    Args:
        pattern_type: One of 'sequential', 'parallel', 'hierarchical'
        agents: List of agent names
        title: Optional custom title
    """
    G = nx.DiGraph()

    if pattern_type == 'sequential':
        # Sequential: A -> B -> C -> D
        for i in range(len(agents) - 1):
            G.add_edge(agents[i], agents[i + 1])
        pos = {agent: (i, 0) for i, agent in enumerate(agents)}
        title = title or "Sequential Orchestration Pattern"

    elif pattern_type == 'parallel':
        # Parallel: Orchestrator -> [A, B, C, D] -> Aggregator
        G.add_node("Orchestrator")
        G.add_node("Aggregator")
        for agent in agents:
            G.add_edge("Orchestrator", agent)
            G.add_edge(agent, "Aggregator")

        pos = {"Orchestrator": (len(agents) / 2, 2)}
        for i, agent in enumerate(agents):
            pos[agent] = (i, 1)
        pos["Aggregator"] = (len(agents) / 2, 0)
        title = title or "Parallel Orchestration Pattern"

    elif pattern_type == 'hierarchical':
        # Hierarchical: Supervisor -> [Manager1, Manager2] -> [Worker1, Worker2, Worker3]
        supervisor = agents[0] if agents else "Supervisor"
        managers = agents[1:3] if len(agents) > 1 else ["Manager1", "Manager2"]
        workers = agents[3:] if len(agents) > 3 else ["Worker1", "Worker2", "Worker3"]

        G.add_node(supervisor)
        for manager in managers:
            G.add_edge(supervisor, manager)
            for worker in workers:
                G.add_edge(manager, worker)

        pos = {supervisor: (1, 2)}
        for i, manager in enumerate(managers):
            pos[manager] = (i * 1.5, 1)
        for i, worker in enumerate(workers):
            pos[worker] = (i * 0.7, 0)
        title = title or "Hierarchical Orchestration Pattern"

    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(G, pos, node_color='#2ecc71', node_size=3000, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
        width=2
    )

    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
