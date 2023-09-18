import os
import time
from typing import Optional

import openai
from pydantic import BaseModel

from cases.page_compress.simple_input import InputBox

from components.llm.llm_key_extract import LLMKeyExtract
from context.base_context import BaseContext

from dag.base_components.end_note import EndNode
from dag.base_components.executable import Status
from dag.base_components.executable_node import ExecutableNode
from dag.base_components.start_node import StartNode

from dag.builder import DagBuilder
from dag.dag import Dag
from dag.dag_run import SequenceDagRun, ParallelDagRun

from dag_parser.draw_dag import DrawDag

from model.llm import ChatGPT


class StartOutput(BaseModel):
    ret: str


class TestStart(StartNode):
    """
    消息箱子，仅仅提供消息
    """

    def __init__(self, id_: int, label: str
                 ):
        """
        :param info: 记录的消息
        """
        super().__init__(id_, label)

    def _get_info(self):
        return StartOutput(ret=self.get_context().get_user_input())

    def output(self):
        return StartOutput


class ReplyInput(BaseModel):
    param1: str
    param2: str
    param3: str


class TestReply(EndNode):

    def _execute(self, input_: ReplyInput):
        print("\n参数1：")
        print(input_.param1)
        print("----------------------------------------")

        print("参数2：")
        print(input_.param2)
        print("----------------------------------------")

        print("参数3：")
        print(input_.param3)
        print("----------------------------------------")

    def input(self):
        return ReplyInput


class ExeInput(BaseModel):
    param: Optional[str]


class ExeOutput(BaseModel):
    ret: str


class TestExecute(ExecutableNode):

    def __init__(self, id_: int, label: str, sleep_time=None):
        super().__init__(id_, label)
        self.sleep_time = sleep_time

    def _execute(self, input_: ExeInput):
        if self.sleep_time is not None:
            time.sleep(self.sleep_time)

        if input_.param is None:
            return ExeOutput(ret="上游崩了")
        return ExeOutput(ret=input_.param)

    def input(self):
        return ExeInput

    def output(self):
        return ExeOutput


def test_DAG():
    builder = DagBuilder(Dag("test_DAG"))

    root = builder.allocate_root(TestStart, label="Input")

    node1 = builder.allocate(TestExecute, label="节点1")
    node2 = builder.allocate(TestExecute, label="节点2")
    node3 = builder.allocate(TestExecute, label="节点3")
    node4 = builder.allocate(TestExecute, label="节点4")
    node5 = builder.allocate(TestExecute, label="节点5")
    node6 = builder.allocate(TestExecute, label="节点6")

    reply = builder.allocate(TestReply, label="Reply")

    root.OUT.ret.connect(node1.IN.param)
    root.OUT.ret.connect(node2.IN.param)

    node1.OUT.ret.connect(node3.IN.param)
    node1.OUT.ret.connect(node4.IN.param)

    node2.OUT.ret.connect(node6.IN.param)

    node3.OUT.ret.connect(reply.IN.param1)

    node4.OUT.ret.connect(node5.IN.param)

    node5.OUT.ret.connect(reply.IN.param2)

    node6.OUT.ret.connect(reply.IN.param3)

    dag = builder.build()

    # DrawDag.draw_from_root(dag.root, "test_DAG.gv")

    dag_run = SequenceDagRun(dag)
    user_input = "这是user_input，看看是否能传递到reply"
    context = BaseContext(user_input=user_input)
    dag_run.run(context)
    # dag_run.draw_result()
    assert len(dag_run.get_result().failed_nodes) == 0


def test_ParallelDagRun():
    builder = DagBuilder(Dag("test_ParallelDagRun"))

    root = builder.allocate_root(TestStart, label="Input")

    node1 = builder.allocate(TestExecute, label="节点1", sleep_time=1)
    node2 = builder.allocate(TestExecute, label="节点2", sleep_time=-1)
    node3 = builder.allocate(TestExecute, label="节点3")
    node4 = builder.allocate(TestExecute, label="节点4")
    # 故意让5,6 sleep
    node5 = builder.allocate(TestExecute, label="节点5", sleep_time=1)
    node6 = builder.allocate(TestExecute, label="节点6", sleep_time=1)

    reply = builder.allocate(TestReply, label="Reply")

    root.OUT.ret.connect(node1.IN.param)
    root.OUT.ret.connect(node2.IN.param)

    node1.OUT.ret.connect(node3.IN.param)
    node1.OUT.ret.connect(node4.IN.param)

    node2.OUT.ret.connect(node6.IN.param)

    node3.OUT.ret.connect(reply.IN.param1)

    node4.OUT.ret.connect(node5.IN.param)

    node5.OUT.ret.connect(reply.IN.param2)

    node6.OUT.ret.connect(reply.IN.param3)

    dag = builder.build()

    # DrawDag.draw_from_root(dag.root, "test_DAG.gv")

    dag_run = ParallelDagRun(dag)
    user_input = "测试多线程并发dag看是否ok"
    context = BaseContext(user_input=user_input)
    import time
    s = time.time()
    dag_run.run(context)
    e = time.time()

    cost = e - s

    dag_run.draw_result(f_name="test_ParallelDagRun_result.gv")

    # 有一个节点，故意搞崩的
    assert len(dag_run.get_result().failed_nodes) == 1
    assert int(cost) == 2


if __name__ == '__main__':
    test_ParallelDagRun()

