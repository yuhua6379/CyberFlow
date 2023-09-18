import re

from common.log.logger import get_logger
from components.tools.llm_calc.base import BaseCalc
from model.llm import BaseLLM


class KeyExtractCalc(BaseCalc):
    def __init__(self, llm: BaseLLM, max_tokens: int, prompt_template: str, result_max_tokens: int = None,
                 max_extract_round: int = 1):
        super().__init__(llm, max_tokens)
        self.max_tokens = max_tokens
        self.prompt_template = prompt_template
        self.result_max_tokens = result_max_tokens
        self.max_extract_round = max_extract_round - 1

    def extract(self, content: str):
        result = self._extract(content)
        for i in range(self.max_extract_round):
            if self.result_max_tokens is None:
                return result
            if self.evaluate_tokens(result) > self.result_max_tokens:
                result = self._extract(result)
        return result

    def _extract(self, content: str):

        content = re.split("[\n.。]", content)
        results = []
        temp = []
        for line in content:
            temp.append(line)
            temp_content = "\n".join(temp)
            tokens = self.evaluate_tokens(temp_content)
            if tokens <= self.max_tokens * 0.5:
                continue

            if tokens >= self.max_tokens * 0.7:
                # 最后一段内容超标了，舍弃
                temp.pop(-1)
                temp_content = "\n".join(temp)

            res = self.predict(self.prompt_template.format(input=temp_content))
            get_logger().debug(f"temp block result: {res}")
            temp = []
            results.append(res)

            str_result = "\n".join(results)
            result_tokens = self.evaluate_tokens(str_result)
            if self.max_extract_round == 0 and result_tokens > self.result_max_tokens:
                results.pop(-1)
                get_logger().info(f"strip for exceeding result_max_tokens tokens: {result_tokens}")
                return "\n".join(results)

        if len(temp) > 0:
            res = self.predict(self.prompt_template.format(input="\n".join(temp)))
            results.append(res)

        return "\n".join(results)
