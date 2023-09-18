import os

import openai

from cases.genshin_impact_question.crawler_genshin_wiki import GenshinPageCrawler
from cases.genshin_impact_question.game_info import character, weapon, artifact
from cases.genshin_impact_question.llm_reply import LLMReply
from components.infobox import InfoBox
from components.llm.llm_build_kw import LLMBuildKW
from components.llm.llm_key_extract import LLMKeyExtract
from components.llm.llm_summary import LLMSummary
from components.web.search import Search
from context.base_context import BaseContext
from context.knowledge_base import VectorDBKnowledgeBase
from dag.builder import DagBuilder
from dag.dag import Dag
from dag.dag_run import SequenceDagRun, ParallelDagRun
from dag_parser.draw_dag import DrawDag
from datasource.config import vector_db_factory
from model.llm import ChatGPT

openai.api_key = os.environ["openai_api_key"]
gpt = ChatGPT()
gpt4 = ChatGPT(model="gpt-4")
builder = DagBuilder(Dag("原神问题"))

root = builder.allocate_root(InfoBox, label="用户输入")
reply = builder.allocate(LLMReply, label="回复用户", llm=gpt4)
has_weapon = builder.allocate(LLMBuildKW,
                              label="是否包含武器",
                              content_desc="这个是和游戏有关的一段话",
                              key_desc="武器", llm=gpt)

crawler_weapon = builder.allocate(GenshinPageCrawler, label="爬取武器并摘要", llm=gpt, max_tokens=1000)

extract_weapon_info = builder.allocate(LLMSummary, llm=gpt, label="提取信息")

has_character = builder.allocate(LLMBuildKW,
                                 label="是否包含角色",
                                 content_desc="这个是和游戏有关的一段话",
                                 key_desc="角色", llm=gpt)

crawler_character = builder.allocate(GenshinPageCrawler, label="爬取角色并摘要", llm=gpt, max_tokens=2000)

extract_character_info = builder.allocate(LLMSummary, llm=gpt4, label="提取信息")

if __name__ == '__main__':
    root.OUT.info.connect(has_weapon.IN.input)
    has_weapon.OUT.output.connect(crawler_weapon.IN.query)
    crawler_weapon.OUT.result.connect(extract_weapon_info.IN.input)
    extract_weapon_info.OUT.output.connect(reply.IN.weapon_info)

    root.OUT.info.connect(has_character.IN.input)
    has_character.OUT.output.connect(crawler_character.IN.query)
    crawler_character.OUT.result.connect(extract_character_info.IN.input)
    extract_character_info.OUT.output.connect(reply.IN.character_info)

    dag = builder.build()

    # DrawDag.draw_from_root(dag)

    dag_run = ParallelDagRun(dag)

    user_input = "我想知道艾尔海森能不能用裁叶萃光"

    db = vector_db_factory.get_vector_db("genshin_knowledge")
    context = BaseContext(user_input=user_input, knowledge=VectorDBKnowledgeBase(db=db))
    context.set("角色", character)
    context.set("武器", weapon)
    context.set("装备", artifact)
    dag_run.run(context)
