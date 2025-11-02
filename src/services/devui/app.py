"""Main entry point for the Dev UI application. This simply spawns the Dev UI server with the specified agents."""

import logging

# This application is the entry point so we configure logging here.
logging.basicConfig(level=logging.INFO)

from agent_framework.devui import serve
from shared.agents.graph_documenter import GraphDocumenterAgent

logger = logging.getLogger(__name__)


def main():
    """Main function to start the Dev UI server with specified agents."""

    logger.info("Initializing Dev UI server...")
    agents = [GraphDocumenterAgent().agent]
    logger.info(f"Starting Dev UI with agents: {agents}")

    logger.info("Launching Dev UI server on port 7860...")
    try:
        serve(entities=agents, port=7860, auto_open=True, tracing_enabled=True)
    except Exception as e:
        logger.error(f"Failed to start Dev UI server: {e}")


if __name__ == "__main__":
    main()
