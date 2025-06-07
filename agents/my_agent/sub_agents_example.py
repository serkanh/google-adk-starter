"""
Example sub-agents for your agent.

This file demonstrates how to create specialized sub-agents that can be
orchestrated by your main agent for complex tasks.
"""

from google.adk.agents import Agent, Sequential, Parallel
from google.adk.models.lite_llm import LiteLlm


def create_research_agent() -> Agent:
    """Create a sub-agent specialized in research tasks."""
    return Agent(
        name="researcher",
        model=LiteLlm(model="gpt-4"),
        description="Specializes in researching and gathering information",
        instruction="""You are a research specialist. Your role is to:
        - Find relevant information on topics
        - Analyze and summarize findings
        - Identify credible sources
        - Highlight key insights
        Be thorough but concise in your research.""",
        tools=[],  # Add research-specific tools here
    )


def create_writer_agent() -> Agent:
    """Create a sub-agent specialized in writing tasks."""
    return Agent(
        name="writer",
        model=LiteLlm(model="gpt-4"),
        description="Specializes in creating well-written content",
        instruction="""You are a professional writer. Your role is to:
        - Create clear, engaging content
        - Adapt tone and style as needed
        - Ensure proper grammar and structure
        - Make complex topics accessible
        Focus on clarity and impact.""",
        tools=[],  # Add writing-specific tools here
    )


def create_reviewer_agent() -> Agent:
    """Create a sub-agent specialized in reviewing and improving content."""
    return Agent(
        name="reviewer",
        model=LiteLlm(model="gpt-3.5-turbo"),  # Can use a lighter model
        description="Reviews and improves content quality",
        instruction="""You are a content reviewer. Your role is to:
        - Check for accuracy and clarity
        - Suggest improvements
        - Ensure consistency
        - Verify completeness
        Be constructive and specific in your feedback.""",
        tools=[],  # Add review-specific tools here
    )


# Example orchestration patterns
def create_content_workflow() -> Sequential:
    """Create a sequential workflow for content creation."""
    return Sequential(
        agents=[
            create_research_agent(),
            create_writer_agent(),
            create_reviewer_agent(),
        ],
        description="Research, write, and review content"
    )


def create_parallel_analysis() -> Parallel:
    """Create parallel agents for multi-perspective analysis."""
    return Parallel(
        agents=[
            Agent(
                name="technical_analyzer",
                model=LiteLlm(model="gpt-4"),
                description="Analyzes technical aspects",
                instruction="Focus on technical accuracy and feasibility."
            ),
            Agent(
                name="business_analyzer",
                model=LiteLlm(model="gpt-4"),
                description="Analyzes business implications",
                instruction="Focus on business value and ROI."
            ),
        ],
        description="Analyze from multiple perspectives simultaneously"
    )


# Example of using sub-agents in your main agent:
#
# from .sub_agents_example import create_research_agent, create_writer_agent
#
# def create_my_agent() -> Agent:
#     return Agent(
#         name="coordinator",
#         model=LiteLlm(model="gpt-4"),
#         description="Coordinates specialized sub-agents",
#         instruction="You coordinate different specialists to complete complex tasks.",
#         sub_agents=[
#             create_research_agent(),
#             create_writer_agent(),
#         ],
#         # ... other config ...
#     )