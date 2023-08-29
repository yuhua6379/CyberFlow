import os

import openai

from cases.genshin_impact_question.llm_reply import LLMReply
from components.infobox import InfoBox
from components.llm_build_kw import LLMBuildKW
from components.llm_summarizer import LLMSummarizer
from components.searcher import Searcher
from dag.builder import DagBuilder
from dag.dag import Dag, DagRun
from dag_parser.iterator import DagIterator
from model.llm import ChatGPT

openai.api_key = os.environ["openai_api_key"]
gpt = ChatGPT()
builder = DagBuilder(Dag())

root = builder.allocate(InfoBox, label="用户输入", info="我想知道夜兰能不能拿裁叶萃光")
reply = builder.allocate(LLMReply, label="回复用户", llm=gpt)
has_weapon = builder.allocate(LLMBuildKW,
                              llm=gpt,
                              label="是否包含武器",
                              prompt_template="'{input}'\n"
                                              "这个是和游戏有关的一段话，最后你要确定哪个词最可能是游戏里面的一种武器，回复我这个词，且你只允许回复这个词\n"
                                              "<>")

search_weapon = builder.allocate(Searcher, label="搜索武器")

extract_weapon_info = builder.allocate(LLMSummarizer, llm=gpt, label="提取信息")

has_character = builder.allocate(LLMBuildKW,
                                 llm=gpt,
                                 label="是否包含人物",
                                 prompt_template="'{input}'\n"
                                                 "这个是和游戏有关的一段话，最后你要确定哪个词最可能是游戏里面的一个角色，不是物品，回复我这个词，且你只允许回复这个词\n"
                                                 "<>")

search_character = builder.allocate(Searcher, label="搜索人物")

extract_character_info = builder.allocate(LLMSummarizer, llm=gpt, label="提取信息")

if __name__ == '__main__':
    root.out.info.connect(has_weapon.input)
    has_weapon.out.output.connect(search_weapon.query)
    search_weapon.out.result.connect(extract_weapon_info.input)
    extract_weapon_info.out.output.connect(reply.weapon_info)

    root.out.info.connect(has_character.input)
    has_character.out.output.connect(search_character.query)
    search_character.out.result.connect(extract_character_info.input)
    extract_character_info.out.output.connect(reply.character_info)

    root.out.info.connect(reply.user_demand)

    dag = builder.build()
    # DrawDag.draw_from_root(root.node)

    dag_run = DagRun()

    di = DagIterator(dag_run)
    di.iter_downstream(root.node)

    dag_run.run()
