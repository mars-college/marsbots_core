from manifest import Manifest


class CharacterCapability:
    def __init__(self, name: str, prompt: str, api_key: str):
        self.name = name
        self.prompt = prompt
        self.llm = Manifest(
            client_name="openai",
            client_connection=api_key,
            max_tokens=100,
            temperature=1.0,
            stop_token="<",
        )

    def reply_to_message(self, message: str, sender_name: str):
        prompt = self.prompt
        prompt += "\n\n"
        prompt += f'<{sender_name}> "{message}"\n'
        prompt += f"<{self.name}>"
        completion = self.llm.run(prompt=prompt)
        return completion
