# main.py

import logging
from config import ENABLE_VOICE, MODEL_NAME, OLLAMA_HOST

from modules.memory import ConversationMemory
from modules.voice import speak
from modules.logger import get_logger

from core.agent import Agent
from core.tools import create_tool_registry

# Initialize logger
logger = get_logger("TalhaGPT.main")
logger.info(f"Starting TalhaGPT with model: {MODEL_NAME} on {OLLAMA_HOST}")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """
    Start and run the TalhaGPT application.
    """

    # --------------------------------------------------------
    # CONVERSATION MEMORY
    # --------------------------------------------------------

    try:
        memory = ConversationMemory()
        logger.info("Conversation memory initialized")
    except Exception as e:
        logger.error(f"Failed to initialize memory: {e}", exc_info=True)
        memory = None

    # --------------------------------------------------------
    # TOOL REGISTRY
    # --------------------------------------------------------

    try:
        registry = create_tool_registry()
        logger.info("Tool registry created")
    except Exception as e:
        logger.error(f"Failed to create tool registry: {e}", exc_info=True)
        return

    # --------------------------------------------------------
    # AGENT
    # --------------------------------------------------------

    agent = Agent(
        model_name=MODEL_NAME,
        tool_registry=registry,
        max_steps=6,
        memory=memory,
    )

    # --------------------------------------------------------
    # STARTUP
    # --------------------------------------------------------

    print("\n🤖 Starting TalhaGPT...")
    print("TalhaGPT is ready!")
    print("Type 'q' to exit.")
    print("=" * 40)
    logger.info("TalhaGPT startup complete")

    # --------------------------------------------------------
    # VOICE STARTUP
    # --------------------------------------------------------

    if ENABLE_VOICE:

        try:
            speak("TalhaGPT is ready.")
            logger.info("Startup voice message played")

        except Exception as e:
            logger.error(f"Voice error at startup: {e}", exc_info=True)
            print(f"[Voice Error]: {e}")

    # --------------------------------------------------------
    # CHAT LOOP
    # --------------------------------------------------------

    while True:

        try:
            user_input = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):

            print("\n\nShutting down TalhaGPT...")
            logger.info("TalhaGPT shutdown initiated by user")
            break

        # ----------------------------------------------------
        # EMPTY MESSAGE
        # ----------------------------------------------------

        if not user_input:
            continue

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if user_input.lower() in {
            "q",
            "exit",
            "quit",
        }:

            print("Shutting down TalhaGPT...")
            logger.info("TalhaGPT shutdown initiated")
            break

        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        user_message = {
            "role": "user",
            "content": user_input,
        }

        logger.debug(f"User input: {user_input}")

        # ----------------------------------------------------
        # RUN AGENT
        # ----------------------------------------------------

        try:

            result = agent.run(
                [user_message]
            )

        except Exception as e:

            error_msg = f"Agent error: {e}"
            logger.error(error_msg, exc_info=True)
            print(f"\n[Agent Error]: {e}")
            continue

        # ----------------------------------------------------
        # DISPLAY RESPONSE
        # -------------------------------------------- --------

        print(
            f"\n🤖 TalhaGPT: {result}"
        )
        logger.debug(f"Agent response: {result}")

        # ----------------------------------------------------
        # VOICE OUTPUT
        # -------------------------------------------- --------

        if ENABLE_VOICE:

            try:
                speak(result)
                logger.debug("Response played via voice")

            except Exception as e:
                logger.error(f"Voice output error: {e}", exc_info=True)
                print(f"[Voice Error]: {e}")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        print(f"[Critical Error]: {e}")
        raise
