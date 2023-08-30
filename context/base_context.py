from typing import Any

from context.knowledge_base import KnowledgeBase


class BaseContext:
    def __init__(self, user_input: Any, knowledge: KnowledgeBase):
        self.user_input = user_input
        self.knowledge = knowledge
        self.extend = {}

    def set(self, k, v):
        self.extend[k] = v

    def get(self, k):
        return self.extend.get(k)

    def get_user_input(self):
        return self.user_input

    def get_knowledge_base(self):
        return self.knowledge
