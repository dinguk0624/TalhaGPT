
# core/agent.py

import json

import ollama


class Agent:
    """
    Main agent loop for TalhaGPT.

    Model -> Tool -> Model -> Tool -> Final answer

    ConversationMemory can be connected to preserve
    conversation history between sessions.
    """

    def __init__(
        self,
        model_name: str,
        tool_registry,
        max_steps: int = 6,
        memory=None,
    ):
        self.model_name = model_name
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.memory = memory

    # ========================================================
    # ARGUMENT PARSING
    # ========================================================

    def _parse_arguments(self, arguments):
        """
        Safely convert tool arguments into a dictionary.
        """

        if arguments is None:
            return {}

        if isinstance(arguments, dict):
            return arguments

        if isinstance(arguments, str):

            try:
                parsed = json.loads(arguments)

                if isinstance(parsed, dict):
                    return parsed

            except json.JSONDecodeError:
                pass

        return {}

    # ========================================================
    # MEMORY SAVE
    # ========================================================

    def _save_message(
        self,
        role: str,
        content: str = "",
        **kwargs
    ):
        """
        Save a message to ConversationMemory if enabled.
        """

        if self.memory is None:
            return

        try:

            self.memory.add_message(
                role,
                content,
                **kwargs
            )

        except Exception as e:

            print(
                f"[Memory Error] Failed to save message: {e}"
            )

    # ========================================================
    # MEMORY LOAD
    # ========================================================

    def _load_memory_messages(self):
        """
        Load conversation history from ConversationMemory.
        """

        if self.memory is None:
            return []

        try:

            messages = self.memory.get_messages()

            if isinstance(messages, list):
                return messages

        except Exception as e:

            print(
                f"[Memory Error] Failed to load messages: {e}"
            )

        return []

    # ========================================================
    # PREPARE MESSAGES
    # ========================================================

    def _prepare_messages(
        self,
        messages: list[dict]
    ) -> list[dict]:
        """
        Combine persistent memory with current messages.
        """

        stored_messages = self._load_memory_messages()

        if not stored_messages:
            return [
                dict(message)
                for message in messages
                if isinstance(message, dict)
            ]

        combined = []

        for message in stored_messages:

            if isinstance(message, dict):

                combined.append(
                    dict(message)
                )

        for message in messages:

            if not isinstance(message, dict):
                continue

            if message not in combined:

                combined.append(
                    dict(message)
                )

        return combined

    # ========================================================
    # ENSURE SYSTEM PROMPT
    # ========================================================

    def _ensure_system_prompt(
        self,
        messages: list[dict]
    ) -> list[dict]:
        """
        Make sure the model receives clear instructions
        about memory and available tools.
        """

        system_instruction = (
            "You are TalhaGPT, a helpful AI assistant. "

            "You have access to tools. "

            "When the user explicitly asks you to remember, "
            "save, store, or note information, use the "
            "save_note tool. "

            "When the user asks about information that may "
            "already exist in RAG memory, use the "
            "search_memory tool before answering. "

            "Do not claim that you saved something unless "
            "the save_note tool actually succeeded. "

            "After a successful tool call, give the user "
            "a clear final response."
        )

        has_system = False

        for message in messages:

            if (
                isinstance(message, dict)
                and message.get("role") == "system"
            ):

                has_system = True
                break

        if not has_system:

            messages.insert(
                0,
                {
                    "role": "system",
                    "content": system_instruction,
                }
            )

        return messages

    # ========================================================
    # RUN AGENT
    # ========================================================

    def run(
        self,
        messages: list[dict]
    ) -> str:
        """
        Run the TalhaGPT agent loop.
        """

        # ----------------------------------------------------
        # PREPARE CONVERSATION
        # ----------------------------------------------------

        messages = self._prepare_messages(
            messages
        )

        messages = self._ensure_system_prompt(
            messages
        )

        # ----------------------------------------------------
        # SAVE NEW MESSAGES
        # ----------------------------------------------------

        if self.memory is not None:

            existing_messages = (
                self._load_memory_messages()
            )

            for message in messages:

                if message not in existing_messages:

                    self._save_message(
                        message.get(
                            "role",
                            "user"
                        ),
                        message.get(
                            "content",
                            ""
                        ),
                        **{
                            key: value
                            for key, value
                            in message.items()
                            if key not in (
                                "role",
                                "content"
                            )
                        }
                    )

        # ----------------------------------------------------
        # AGENT LOOP
        # ----------------------------------------------------

        for step in range(
            self.max_steps
        ):

            print(
                f"\n🧠 [Agent] Step "
                f"{step + 1}/{self.max_steps}"
            )

            # ------------------------------------------------
            # CALL MODEL
            # ------------------------------------------------

            try:

                response = ollama.chat(
                    model=self.model_name,
                    messages=messages,
                    tools=self.tool_registry.get_schemas(),
                )

            except Exception as e:

                return (
                    f"Model execution error: {e}"
                )

            response_message = response.message

            # ------------------------------------------------
            # TOOL CALLS
            # ------------------------------------------------

            tool_calls = (
                response_message.tool_calls
                or []
            )

            # ------------------------------------------------
            # NORMAL RESPONSE
            # ------------------------------------------------

            if not tool_calls:

                content = (
                    response_message.content
                    or ""
                ).strip()

                # --------------------------------------------
                # EMPTY RESPONSE
                # --------------------------------------------

                if not content:

                    print(
                        "[Agent] Model returned an empty "
                        "response."
                    )

                    # Try one more model request with an
                    # explicit instruction.
                    messages.append(
                        {
                            "role": "user",
                            "content": (
                                "Please continue and provide "
                                "a clear response. If a tool "
                                "is required, use the "
                                "appropriate tool."
                            ),
                        }
                    )

                    continue

                # --------------------------------------------
                # SAVE ASSISTANT RESPONSE
                # --------------------------------------------

                assistant_message = {
                    "role": "assistant",
                    "content": content,
                }

                messages.append(
                    assistant_message
                )

                self._save_message(
                    "assistant",
                    content
                )

                return content

            # ------------------------------------------------
            # SAVE ASSISTANT TOOL CALL
            # ------------------------------------------------

            assistant_message = {
                "role": "assistant",
                "content": (
                    response_message.content
                    or ""
                ),
                "tool_calls": [
                    {
                        "function": {
                            "name": (
                                tool_call.function.name
                            ),
                            "arguments": (
                                tool_call.function.arguments
                            ),
                        }
                    }
                    for tool_call in tool_calls
                ],
            }

            messages.append(
                assistant_message
            )

            self._save_message(
                "assistant",
                response_message.content or "",
                tool_calls=assistant_message[
                    "tool_calls"
                ]
            )

            # ------------------------------------------------
            # EXECUTE TOOLS
            # ------------------------------------------------

            for tool_call in tool_calls:

                tool_name = (
                    tool_call.function.name
                )

                arguments = (
                    self._parse_arguments(
                        tool_call.function.arguments
                    )
                )

                print(
                    f"⚙️ [Tool] {tool_name}"
                )

                print(
                    f"   Arguments: {arguments}"
                )

                # --------------------------------------------
                # CHECK TOOL
                # --------------------------------------------

                if not self.tool_registry.has(
                    tool_name
                ):

                    tool_result = (
                        f"Error: Tool "
                        f"'{tool_name}' was not found."
                    )

                else:

                    try:

                        tool_result = (
                            self.tool_registry.execute(
                                tool_name,
                                arguments
                            )
                        )

                    except Exception as e:

                        tool_result = (
                            "Tool execution error: "
                            f"{e}"
                        )

                # --------------------------------------------
                # PRINT RESULT
                # --------------------------------------------

                print(
                    f"📦 [Tool Result]: "
                    f"{tool_result}"
                )

                # --------------------------------------------
                # SEND TOOL RESULT TO MODEL
                # --------------------------------------------

                tool_message = {
                    "role": "tool",
                    "content": str(
                        tool_result
                    ),
                }

                messages.append(
                    tool_message
                )

                self._save_message(
                    "tool",
                    str(tool_result)
                )

        # ----------------------------------------------------
        # MAXIMUM STEPS
        # ----------------------------------------------------

        return (
            "The agent reached its maximum "
            f"limit of {self.max_steps} steps. "
            "The operation was stopped."
        )
