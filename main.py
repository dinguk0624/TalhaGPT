# main.py

from config import ENABLE_VOICE, MODEL_NAME, OLLAMA_HOST, REQUIRE_TOOL_CONFIRM, VERSION

from modules.memory import ConversationMemory
from modules.voice import speak
from modules.logger import get_logger

from core.agent import Agent
from core.tools import create_tool_registry

logger = get_logger("TalhaGPT.main")
logger.info("Starting TalhaGPT %s with model: %s on %s", VERSION, MODEL_NAME, OLLAMA_HOST)

_EXC = {"exc_info": True}

HELP_TEXT = """
Komutlar:
  /help     — bu yardım
  /clear    — sohbet hafızasını temizle
  /status   — model / host bilgisi
  /tools    — kayıtlı tool listesi
  q / exit  — çıkış
""".strip()


def _confirm_tool(tool_name: str, arguments: dict) -> bool:
    print(f"\n⚠️  Tool izni: {tool_name}({arguments})")
    try:
        answer = input("   Çalıştırılsın mı? [e/H]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return False
    return answer in {"e", "evet", "y", "yes"}


def main():
    """Start and run the TalhaGPT application."""

    try:
        memory = ConversationMemory(max_history=12)
        logger.info("Conversation memory initialized")
    except Exception as e:
        logger.error("Failed to initialize memory: %s", e, **_EXC)
        memory = None

    try:
        registry = create_tool_registry()
        logger.info("Tool registry created")
    except Exception as e:
        logger.error("Failed to create tool registry: %s", e, **_EXC)
        return

    agent = Agent(
        model_name=MODEL_NAME,
        tool_registry=registry,
        max_steps=4,
        memory=memory,
        on_confirm=_confirm_tool if REQUIRE_TOOL_CONFIRM else None,
        require_confirm=REQUIRE_TOOL_CONFIRM,
    )

    print(f"\n🤖 TalhaGPT v{VERSION}")
    print(f"   Model: {MODEL_NAME}")
    print("   Hazır. /help yazabilirsin. Çıkmak için q.")
    print("=" * 40)
    logger.info("TalhaGPT startup complete")

    if ENABLE_VOICE:
        try:
            speak("TalhaGPT is ready.")
            logger.info("Startup voice message played")
        except Exception as e:
            logger.error("Voice error at startup: %s", e, **_EXC)
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

        low = user_input.lower()

        if low in {"q", "exit", "quit"}:
            print("Shutting down TalhaGPT...")
            logger.info("TalhaGPT shutdown initiated")
            break

        # ---- Slash commands (no model call) ----
        if low in {"/help", "help", "?"}:
            print(HELP_TEXT)
            continue

        if low in {"/clear", "/reset"}:
            if memory is not None:
                memory.clear()
                print("🧹 Hafıza temizlendi.")
            else:
                print("Hafıza yok.")
            continue

        if low == "/status":
            print(f"TalhaGPT v{VERSION}")
            print(f"Model: {MODEL_NAME}")
            print(f"Host:  {OLLAMA_HOST}")
            print(f"Tool confirm: {REQUIRE_TOOL_CONFIRM}")
            if memory is not None:
                print(f"Memory messages: {memory.count()}")
            continue

        if low == "/tools":
            names = sorted(registry.list_tools() if hasattr(registry, "list_tools") else [])
            if not names:
                # fallback: schemas
                try:
                    schemas = registry.get_schemas()
                    names = sorted(
                        s.get("function", {}).get("name", "?") for s in schemas
                    )
                except Exception:
                    names = []
            print("Tools:")
            for n in names:
                print(f"  • {n}")
            continue

        user_message = {"role": "user", "content": user_input}
        logger.debug("User input: %s", user_input)

        print("\n🤖 TalhaGPT: ", end="", flush=True)

        try:
            result = agent.run(
                [user_message],
                on_token=lambda token: print(token, end="", flush=True),
            )
        except Exception as e:
            logger.error("Agent error: %s", e, **_EXC)
            print(f"\n[Agent Error]: {e}")
            continue

        print()
        logger.debug("Agent response: %s", result)

        if ENABLE_VOICE:
            try:
                speak(result)
                logger.debug("Response played via voice")
            except Exception as e:
                logger.error("Voice output error: %s", e, **_EXC)
                print(f"[Voice Error]: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical("Unhandled exception: %s", e, **_EXC)
        print(f"[Critical Error]: {e}")
        raise
