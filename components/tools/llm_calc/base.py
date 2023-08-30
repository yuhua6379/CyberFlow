import jieba

from model.llm import BaseLLM


class BaseCalc:
    def __init__(self, llm: BaseLLM, max_tokens: int):
        self.max_tokens = max_tokens
        self.llm = llm

    @classmethod
    def evaluate_tokens(cls, content: str):
        return len(list(jieba.cut(content)))

    def predict(self, prompt: str, retry: int = 3):
        ex = None
        for _ in range(retry):
            try:
                return self._predict(prompt)
            except Exception as e:
                ex = e
        raise ex

    def _predict(self, prompt: str):
        prompt_tokens = self.evaluate_tokens(prompt)
        if prompt_tokens > self.max_tokens:
            raise RuntimeError(f"{prompt_tokens} exceeds max_tokens: {self.max_tokens}")
        return self.llm.chat(prompt)
