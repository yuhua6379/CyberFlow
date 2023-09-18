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
from dag.dag_run import SequenceDagRun
from dag_parser.draw_dag import DrawDag
from datasource.config import vector_db_factory
from model.llm import ChatGPT

openai.api_key = os.environ["openai_api_key"]
gpt = ChatGPT()
builder = DagBuilder(Dag())

root = builder.allocate_root(InfoBox, label="用户输入")
reply = builder.allocate(LLMReply, label="回复用户", llm=gpt)
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

extract_character_info = builder.allocate(LLMSummary, llm=gpt, label="提取信息")

if __name__ == '__main__':
    root.out.info.connect(has_weapon.input)
    has_weapon.out.output.connect(crawler_weapon.query)
    crawler_weapon.out.result.connect(extract_weapon_info.input)
    extract_weapon_info.out.output.connect(reply.weapon_info)

    root.out.info.connect(has_character.input)
    has_character.out.output.connect(crawler_character.query)
    crawler_character.out.result.connect(extract_character_info.input)
    extract_character_info.out.output.connect(reply.character_info)

    dag = builder.build()

    DrawDag.draw_from_root(dag.root)
    #
    #
    # dag_run = DagRun(root.node)
    #
    # user_input = "我想知道夜兰能不能拿裁叶萃光"
    # db = vector_db_factory.get_vector_db("genshin_knowledge")
    # context = BaseContext(user_input=user_input, knowledge=VectorDBKnowledgeBase(db=db))
    # context.set("角色", character)
    # context.set("武器", weapon)
    # context.set("装备", artifact)
    # dag_run.run(context)
