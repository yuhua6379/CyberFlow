import re

from common.base_thread import get_logger
from components.tools.llm_calc.base import BaseCalc
from model.llm import BaseLLM


class KeyExtractCalc(BaseCalc):
    def __init__(self, llm: BaseLLM, max_tokens: int, prompt_template: str):
        super().__init__(llm, max_tokens)
        self.max_tokens = max_tokens
        self.prompt_template = prompt_template

    def extract(self, content: str):

        content = re.split("[\n.。]", content)
        results = []
        temp = []
        for line in content:
            temp.append(line)
            temp_content = "\n".join(temp)
            tokens = self.evaluate_tokens(temp_content)
            if tokens <= self.max_tokens * 0.5:
                continue

            if self.max_tokens * 0.7 <= tokens:
                # 最后一段内容超标了，舍弃
                temp.pop(-1)
                temp_content = "\n".join(temp)

            res = self.predict(self.prompt_template.format(input=temp_content))
            get_logger().debug(f"temp block result: {res}")
            temp = []
            results.append(res)

        if len(temp) > 0:
            res = self.predict(self.prompt_template.format(input="\n".join(temp)))
            results.append(res)

        return "\n".join(results)
