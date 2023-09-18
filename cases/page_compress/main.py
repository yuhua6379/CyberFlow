import os

import openai

from cases.page_compress.simple_input import InputBox
from cases.page_compress.simple_reply import SimpleReply
from components.llm.llm_key_extract import LLMKeyExtract
from components.store_into_vectordb import StoreIntoVectorDB
from context.base_context import BaseContext
from context.knowledge_base import KnowledgeBase, VectorDBKnowledgeBase

from dag.builder import DagBuilder
from dag.dag import Dag
from dag.dag_run import SequenceDagRun

from dag_parser.draw_dag import DrawDag
from datasource.config import VECTOR_DB_CONF, vector_db_factory
from model.llm import ChatGPT
from raw import *

openai.api_key = os.environ["openai_api_key"]
gpt = ChatGPT()
builder = DagBuilder(Dag("页面压缩"))

root = builder.allocate_root(InputBox,
                             label="用户输入")

extract_character = builder.allocate(LLMKeyExtract,
                                     label="收集角色知识",
                                     content_desc="这是游戏里面的角色",
                                     key_desc="角色名字", llm=gpt)
extract_weapon = builder.allocate(LLMKeyExtract,
                                  label="收集武器知识",
                                  content_desc="这是游戏里面的武器",
                                  key_desc="(武器名字) -> 类型:(武器类型)", llm=gpt)
extract_artifact = builder.allocate(LLMKeyExtract,
                                    label="收集套装知识",
                                    content_desc="这是游戏里面的套装",
                                    key_desc="(套装名字) -> 效果:(摘要效果)", llm=gpt)

reply = builder.allocate(SimpleReply, label="打印")


if __name__ == '__main__':
    root.OUT.weapon.connect(extract_weapon.IN.input)
    extract_weapon.OUT.output.connect(reply.IN.weapon)

    root.OUT.artifact.connect(extract_artifact.IN.input)
    extract_artifact.OUT.output.connect(reply.IN.artifact)

    root.OUT.character.connect(extract_character.IN.input)
    extract_character.OUT.output.connect(reply.IN.character)

    dag = builder.build()
    db = vector_db_factory.get_vector_db("genshin_knowledge")
    print(db.query("夜兰能不能用裁叶萃光"))

    # DrawDag.draw_from_root(dag.root)

    # dag_run = DagRun(dag.root)
    #
    # user_input = {"character": character,
    #               "weapon": weapon,
    #               "artifact": artifact}

    #
    # context = BaseContext(user_input=user_input, knowledge=VectorDBKnowledgeBase(db=db))
    # dag_run.run(context)

