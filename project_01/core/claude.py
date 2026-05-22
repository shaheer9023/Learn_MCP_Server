import os
import json
from openai import OpenAI


class Claude:
    def __init__(self, model: str):
        base_url = os.getenv("ANTHROPIC_BASE_URL") or "https://api.groq.com/openai/v1"
        api_key = os.getenv("ANTHROPIC_API_KEY")

        print(f"[DEBUG] Connecting to: {base_url}")

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model = model

    def add_user_message(self, messages: list, message):
        if isinstance(message, list):
            messages.extend(message)
        else:
            if isinstance(message, str):
                content = message
            else:
                content = self._extract_text(message)
            messages.append({"role": "user", "content": content})

    def add_assistant_message(self, messages: list, message):
        if hasattr(message, 'choices'):
            msg = message.choices[0].message
            assistant_msg = {"role": "assistant", "content": msg.content or ""}
            if msg.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in msg.tool_calls
                ]
            messages.append(assistant_msg)
        else:
            content = message if isinstance(message, str) else self._extract_text(message)
            messages.append({"role": "assistant", "content": content})

    def _extract_text(self, message):
        if hasattr(message, 'choices'):
            return message.choices[0].message.content or ""
        if hasattr(message, 'content'):
            parts = []
            for block in message.content:
                if hasattr(block, 'text'):
                    parts.append(block.text)
            return "\n".join(parts)
        return str(message)

    def text_from_message(self, message):
        if hasattr(message, 'choices'):
            return message.choices[0].message.content or ""
        return str(message)

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ):
        all_messages = []

        if system:
            all_messages.append({"role": "system", "content": system})

        all_messages.extend(messages)

        params = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": all_messages,
            "temperature": min(temperature, 2.0),
        }

        if stop_sequences:
            params["stop"] = stop_sequences

        if tools:
            openai_tools = []
            for tool in tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.get("name"),
                        "description": tool.get("description", ""),
                        "parameters": tool.get("input_schema", {}),
                    }
                })
            params["tools"] = openai_tools

        response = self.client.chat.completions.create(**params)
        return response