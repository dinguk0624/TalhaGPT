# main.py

from config import ENABLE_VOICE, MODEL_NAME

from modules.memory import ConversationMemory
from modules.voice import speak

from core.agent import Agent
from core.tools import create_tool_registry


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

    memory = ConversationMemory()

    # --------------------------------------------------------
    # TOOL REGISTRY
    # --------------------------------------------------------

    registry = create_tool_registry()

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

    # --------------------------------------------------------
    # VOICE STARTUP
    # --------------------------------------------------------

    if ENABLE_VOICE:

        try:
            speak("TalhaGPT is ready.")

        except Exception as e:
            print(f"[Voice Error]: {e}")

    # --------------------------------------------------------
    # CHAT LOOP
    # --------------------------------------------------------

    while True:

        try:
            user_input = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):

            print("\n\nShutting down TalhaGPT...")
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
            break

        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        user_message = {
            "role": "user",
            "content": user_input,
        }

        # ----------------------------------------------------
        # RUN AGENT
        # ----------------------------------------------------

        try:

            result = agent.run(
                [user_message]
            )

        except Exception as e:

            print(f"\n[Agent Error]: {e}")
            continue

        # ----------------------------------------------------
        # DISPLAY RESPONSE
        # ----------------------------------------------------

        print(
            f"\n🤖 TalhaGPT: {result}"
        )

        # ----------------------------------------------------
        # VOICE OUTPUT
        # ----------------------------------------------------

        if ENABLE_VOICE:

            try:
                speak(result)

            except Exception as e:
                print(f"[Voice Error]: {e}")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
