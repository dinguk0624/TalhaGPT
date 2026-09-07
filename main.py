# main.py

from config import (
    ENABLE_VOICE,
    MODEL_NAME,
    OLLAMA_HOST,
    REQUIRE_TOOL_CONFIRM,
    VERSION,
    VISION_MODEL,
)

from modules.memory import ConversationMemory
from modules.permissions import PermissionManager
from modules.sessions import SessionStore
from modules.voice import speak
from modules.logger import get_logger

from core.agent import Agent
from core.tools import create_tool_registry

logger = get_logger("TalhaGPT.main")
logger.info("Starting TalhaGPT %s with model: %s on %s", VERSION, MODEL_NAME, OLLAMA_HOST)

_EXC = {"exc_info": True}

HELP_TEXT = """
Komutlar:
  /help              — bu yardım
  /clear             — bu oturumun sohbet hafızasını temizle
  /status            — model / host / oturum bilgisi
  /tools             — kayıtlı tool listesi
  /permissions       — tool izinleri (allow / ask / deny)
  /allow <tool>      — aracı her zaman çalıştır
  /ask <tool>        — çalıştırmadan önce sor
  /deny <tool>       — aracı engelle
  /sessions          — sohbet oturumlarını listele
  /new [başlık]      — yeni sohbet oturumu
  /switch <id>       — oturum değiştir
  q / exit           — çıkış
""".strip()


permissions = PermissionManager()


def _confirm_tool(tool_name: str, arguments: dict) -> bool:
    print(f"\n⚠️  Tool izni: {tool_name}({arguments})")
    try:
        answer = input("   [e=evet / h=hayır / a=her zaman]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return False
    if answer in {"a", "always", "her zaman", "herzaman"}:
        permissions.set_policy(tool_name, "allow")
        print(f"   '{tool_name}' bundan sonra izinli.")
        return True
    return answer in {"e", "evet", "y", "yes"}


def _make_agent(memory: ConversationMemory | None) -> Agent:
    return Agent(
        model_name=MODEL_NAME,
        tool_registry=registry,
        max_steps=4,
        memory=memory,
        on_confirm=_confirm_tool if REQUIRE_TOOL_CONFIRM else None,
        require_confirm=REQUIRE_TOOL_CONFIRM,
        permissions=permissions,
    )


def _set_policy_command(tool_name: str, policy: str) -> None:
    name = tool_name.strip()
    known = set(registry.list_tools())
    if name and name not in known:
        print(f"Bilinmeyen tool: {name}")
        print("Kayıtlı: " + ", ".join(sorted(known)))
        return
    print(permissions.set_policy(name, policy))


def main():
    """Start and run the TalhaGPT application."""

    global registry

    try:
        sessions = SessionStore()
        memory = sessions.memory
        logger.info("Session %s initialized", sessions.current_id())
    except Exception as e:
        logger.error("Failed to initialize sessions: %s", e, **_EXC)
        try:
            memory = ConversationMemory(max_history=12)
            sessions = None
        except Exception as e2:
            logger.error("Failed to initialize memory: %s", e2, **_EXC)
            memory = None
            sessions = None

    try:
        registry = create_tool_registry()
        logger.info("Tool registry created")
    except Exception as e:
        logger.error("Failed to create tool registry: %s", e, **_EXC)
        return

    agent = _make_agent(memory)

    print(f"\n🤖 TalhaGPT v{VERSION}")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Vision: {VISION_MODEL}")
    if sessions is not None:
        print(f"   Oturum: {sessions.current_id()} ({sessions.current_title()})")
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

        if low in {"/help", "help", "?"}:
            print(HELP_TEXT)
            continue

        if low in {"/clear", "/reset"}:
            if memory is not None:
                memory.clear()
                print("🧹 Bu oturumun hafızası temizlendi.")
            else:
                print("Hafıza yok.")
            continue

        if low == "/status":
            print(f"TalhaGPT v{VERSION}")
            print(f"Model: {MODEL_NAME}")
            print(f"Vision: {VISION_MODEL}")
            print(f"Host:  {OLLAMA_HOST}")
            print(f"Tool confirm: {REQUIRE_TOOL_CONFIRM}")
            if sessions is not None:
                print(f"Oturum: {sessions.current_id()} ({sessions.current_title()})")
            if memory is not None:
                print(f"Memory messages: {memory.count()}")
            continue

        if low == "/tools":
            names = sorted(registry.list_tools() if hasattr(registry, "list_tools") else [])
            print("Tools:")
            for n in names:
                print(f"  • {n}")
            continue

        if low == "/permissions":
            names = registry.list_tools()
            print("Tool izinleri:")
            for name, policy in permissions.list_policies(names).items():
                print(f"  {name}: {policy}")
            continue

        if low.startswith("/allow "):
            _set_policy_command(user_input[7:], "allow")
            continue
        if low.startswith("/ask "):
            _set_policy_command(user_input[5:], "ask")
            continue
        if low.startswith("/deny "):
            _set_policy_command(user_input[6:], "deny")
            continue

        if low == "/sessions":
            if sessions is None:
                print("Oturum yöneticisi yok.")
                continue
            current = sessions.current_id()
            print("Oturumlar:")
            for item in sessions.list_sessions():
                mark = "*" if item.get("id") == current else " "
                print(
                    f" {mark} {item.get('id')}  —  {item.get('title')}  "
                    f"({item.get('updated_at', '')})"
                )
            continue

        if low == "/new" or low.startswith("/new "):
            if sessions is None:
                print("Oturum yöneticisi yok.")
                continue
            title = user_input[4:].strip()
            sid = sessions.create(title or None)
            memory = sessions.memory
            agent.memory = memory
            print(f"🆕 Yeni oturum: {sid} ({sessions.current_title()})")
            continue

        if low.startswith("/switch "):
            if sessions is None:
                print("Oturum yöneticisi yok.")
                continue
            target = user_input[8:].strip()
            switched = sessions.switch(target)
            if not switched:
                print(f"Oturum bulunamadı: {target}")
                continue
            memory = sessions.memory
            agent.memory = memory
            print(f"↔️  Oturum: {switched} ({sessions.current_title()})")
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

        if sessions is not None:
            sessions.touch()

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
    registry = None
    try:
        main()
    except Exception as e:
        logger.critical("Unhandled exception: %s", e, **_EXC)
        print(f"[Critical Error]: {e}")
        raise
