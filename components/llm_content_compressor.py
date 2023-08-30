from pydantic import BaseModel

from common.base_thread import get_logger
from dag.base_components.executable_node import ExecutableNode
from model.llm import BaseLLM


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


class LLMContentCompressor(ExecutableNode):

    def input(self) -> BaseModel:
        return Input

    def output(self) -> BaseModel:
        return Output

    def __init__(self, id_: int, label: str, llm: BaseLLM,
                 summary_desc: str = "写一段上面这段话的摘要，且回复我这段摘要，且你只允许回复这段摘要。"):
        super().__init__(id_, label)
        self.prompt_template = "'{input}'\n" + summary_desc + "\n<>"

        self.llm = llm

    def _execute(self, input_: Input) -> dict:

        long_content = input_.input
        long_content = long_content.split("\n")
        results = []
        temp = []
        for line in long_content:
            temp.append(line)
            if len("\n".join(temp)) < 500:
                continue
            else:
                res = self.llm.chat(self.prompt_template.format(input="\n".join(temp)))
                get_logger().debug(f"temp result: {res}")
                temp = []
                results.append(res)

        if len(temp) > 0:
            res = self.llm.chat(self.prompt_template.format(input="\n".join(temp)))
            results.append(res)

        return Output(output="\n".join(results))
