import ollama

from config import MODEL_NAME
from core.agent import Agent
from core.tools import create_tool_registry


def main():

    registry = create_tool_registry()

    agent = Agent(
        model_name=MODEL_NAME,
        tool_registry=registry,
        max_steps=6,
    )

    messages = [
        {
            "role": "system",
            "content": (
                "Sen TalhaGPT'sin. "
                "Gerekli olduğunda araçlarını kullan."
            ),
        },
        {
            "role": "user",
            "content": "Ankara'nın hava durumunu öğren.",
        },
    ]

    result = agent.run(messages)

    print("\n==============================")
    print("🤖 TalhaGPT:")
    print(result)
    print("==============================")


if __name__ == "__main__":
    main()