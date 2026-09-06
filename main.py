# main.py

from config import ENABLE_VOICE, MODEL_NAME, OLLAMA_HOST

from modules.memory import ConversationMemory
from modules.voice import speak
from modules.logger import get_logger

from core.agent import Agent
from core.tools import create_tool_registry

logger = get_logger("TalhaGPT.main")
logger.info(f"Starting TalhaGPT with model: {MODEL_NAME} on {OLLAMA_HOST}")


def main():
    """Start and run the TalhaGPT application."""

    try:
        memory = ConversationMemory()
        logger.info("Conversation memory initialized")
    except Exception as e:
        logger.error("Failed to initialize memory: %s", e, exc_info=True)
        memory = None

    try:
        registry = create_tool_registry()
        logger.info("Tool registry created")
    except Exception as e:
        logger.error("Failed to create tool registry: %s", e, exc_info=True)
        return

    agent = Agent(
        model_name=MODEL_NAME,
        tool_registry=registry,
        max_steps=6,
        memory=memory,
    )

    print("\n🤖 Starting TalhaGPT...")
    print("TalhaGPT is ready!")
    print("Type 'q' to exit.")
    print("=" * 40)
    logger.info("TalhaGPT startup complete")

    if ENABLE_VOICE:
        try:
            speak("TalhaGPT is ready.")
            logger.info("Startup voice message played")
        except Exception as e:
            logger.error("Voice error at startup: %s", e, exp_info=True)
            print(f"[Voice Error]: {e}")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nShutting down TalhaGPT...")
            logger.info("TalhaGPT shutdown initiated by user")
            break

        if not user_input:
            continue

        if user_input.lower() in {"q", "exit", "quit"}:
            print("Shutting down TalhaGPT...")
            logger.info("TalhaGPT shutdown initiated")
            break

        user_message = {"role": "user", "content": user_input}
        logger.debug("User input: %s", user_input)

        print("\n🤖 TalhaGPT: ", end="", flush=True)

        try:
            result = agent.run(
                [user_message],
                on_token=lambda token: print(token, end="", flush=True),
            )
        except Exception as e:
            logger.error("Agent error: %s", e, exp_info=True)
            print(f"\n[Agent Error]: {e}")
            continue

        print()
        logger.debug("Agent response: %s", result)

        if ENABLE_VOICE:
            try:
                speak(result)
                logger.debug("Response played via voice")
            except Exception as e:
                logger.error("Voice output error: %s", e, exp_info=True)
                print(f"[Voice Error]: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical("Unhandled exception: %s", e, exp_info=True)
        print(f"[Critical Error]: {e}")
        raise
