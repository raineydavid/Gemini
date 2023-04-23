import openai
import pyttsx3

class AI:
    def __init__(self, openai_module, system="", rate=150):
        self.system = system
        self.openai = openai_module
        self.rate = rate
        self.messages = [{"role": "system", "content": system}]

    def generate_response(self, prompt, voice=False, clear_messages=False):
        if clear_messages:
            self.messages = [{"role": "system", "content": self.system}]

        self.messages.append({"role": "user", "content": prompt})

        response_json = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )

        response_text = response_json["choices"][0]["message"]["content"]

        if voice:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)

            engine.say(response_text)
            engine.runAndWait()

        self.messages.append({"role": "assistant", "content": response_text})

        return response_text, self.messages
