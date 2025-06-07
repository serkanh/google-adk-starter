"""My Agent - Main agent module."""

import logging
import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, InMemorySessionService

from .settings import APP_NAME, DB_URL, DEFAULT_USER_ID

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SessionManager:
    """Manages session persistence for the agent."""

    def __init__(self):
        """Initialize session service with fallback to in-memory if DB fails."""
        try:
            self.service = DatabaseSessionService(db_url=DB_URL)
            logger.info(f"Connected to database at {DB_URL}")
        except Exception as e:
            logger.warning(f"Database connection failed: {e}. Using in-memory sessions.")
            self.service = InMemorySessionService()

    async def get_or_create_session(self, user_id: str = DEFAULT_USER_ID) -> str:
        """Get existing session or create new one for the user."""
        try:
            sessions = self.service.list_sessions(app_name=APP_NAME, user_id=user_id)

            if sessions and sessions.sessions:
                session_id = sessions.sessions[0].id
                logger.info(f"Resuming session: {session_id}")
                return session_id

            # Create new session with initial state
            new_session = self.service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                state={
                    "conversations": [],
                    "context": {},
                    "preferences": {}
                }
            )
            logger.info(f"Created new session: {new_session.id}")
            return new_session.id

        except Exception as e:
            logger.error(f"Session management error: {e}")
            raise


# Initialize session manager
session_manager = SessionManager()


def create_my_agent() -> Agent:
    """Create and configure your agent.

    TODO: Customize this function to define your agent's:
    - Name and description
    - Model (GPT-4, Gemini, Claude, etc.)
    - Instructions and personality
    - Tools and capabilities
    - Sub-agents if needed
    """
    return Agent(
        name="my_agent",
        model=LiteLlm(model="gpt-4"),  # TODO: Configure your preferred model
        description="A helpful AI assistant",  # TODO: Add your agent's description
        instruction="""You are a helpful AI assistant.

        TODO: Replace this with your agent's specific instructions.
        Define its expertise, personality, and capabilities.

        Example instructions:
        - What the agent specializes in
        - How it should interact with users
        - Any specific guidelines or constraints
        - Tone and communication style
        """,
        tools=[],  # TODO: Add your tools here
        sub_agents=[],  # TODO: Add specialized sub-agents here
    )


async def get_root_agent() -> Agent:
    """Get the root agent instance."""
    return create_my_agent()


async def get_runner() -> Runner:
    """Initialize the ADK runner with session management."""
    logger.info("Initializing My Agent...")

    agent = await get_root_agent()
    session_id = await session_manager.get_or_create_session()

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_manager.service
    )

    logger.info(f"Runner initialized with session: {session_id}")
    return runner


# Expose for ADK CLI
root_agent = get_root_agent()
runner = get_runner