from typing import Dict
import openai
from telegram import User
from util import DEFAULT, get_config, get_prompt


model_name = 'gpt-3.5-turbo'
openai.api_key = get_config()['chat_key']


def format_req(content: str, mode=0):
    role = ['user', 'system', 'assistant']
    return {'role': role[mode], 'content': content}


class Chat:

    def __init__(self, mode: str = DEFAULT) -> None:
        self.mode = mode
        self.prompt = get_prompt(mode)
        self.conversation = [format_req(self.prompt, 1)]

    def answer(self) -> str:
        resp = openai.ChatCompletion().create(
            model=model_name, messages=self.conversation
        )
        assert isinstance(resp, dict)
        resp = resp['choices'][0]['message']
        self.conversation.append(resp)
        return resp.content

    def talk(self, content: str | None) -> str:
        if content is None:
            return ''
        self.conversation.append(format_req(content))
        return self.answer()

    def regenerate(self) -> str:
        self.conversation.pop()
        return self.answer()


class ChatManager:

    def __init__(self) -> None:
        self.conversation_list: Dict[User, Chat] = {}

    def new(self, user: User | None, mode: str | None = DEFAULT) -> Chat:
        assert user is not None
        self.conversation_list[user] = Chat(DEFAULT if mode is None else mode)
        return self.conversation_list[user]

    def get(self, user: User | None) -> Chat:
        if user in self.conversation_list:
            return self.conversation_list[user]
        return self.new(user)

    def list_(self) -> list:
        return [(i.id, i.name) for i in self.conversation_list.keys()]
