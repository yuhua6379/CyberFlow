from typing import Union, Type

from common.log.logger import get_logger
from dag.base.attach_to import AttachTo
from dag.base.mapper import Mapper
from dag.base_components.end_note import EndNode
from dag.base_components.start_node import StartNode
from dag.dag import Dag


class OutPropWrapper:
    """
    只是一个输出点的外壳，是OutputBuilder的broker
    """

    def __init__(self, output_builder, name: str):
        self.name = name
        self.output_builder = output_builder

    def connect(self, other_in_prop_wrapper):
        self.output_builder.attach_to(self.name, other_in_prop_wrapper.input_builder, other_in_prop_wrapper)


class OutputBuilder:
    def __init__(self, node: StartNode):
        self.node = node
        # 获取节点的输出

        keys = self.node.output().schema()["properties"].keys()
        self.keys = set(keys)
        self.down_streams = dict()

    def __getattr__(self, name):
        if name in self.keys:
            # 返回一个属性包装器，用作回掉触发attach_to
            return OutPropWrapper(self, name)

    def attach_to(self, out_prop_name, other_input_builder, other_in_prop_wrapper):
        other_node = other_input_builder.node
        if other_node.id not in self.down_streams:
            self.down_streams[other_node.id] = {
                # 记录跟某个node连接了
                "node": other_node,
                "outputs": {}
            }

        # 增加两个node连接的细节，参数的转换路径，最终可以转化为mapper
        self.down_streams[other_node.id]["outputs"][out_prop_name] = (out_prop_name, other_in_prop_wrapper.name)

        other_input_builder.on_attach(self)

    def build(self, dag: Dag):
        get_logger().info(f"building {self.node.id}-{self.node.label} ...")
        for node_id, item in self.down_streams.items():
            node = item["node"]
            outputs = item["outputs"]

            mapper = Mapper()
            for output in outputs.values():
                get_logger().debug(f"[out].{output[0]} map to [in].{output[1]} ...")
                mapper.map(*output)
            dag.connect(self.node, node, mapper)


class InPropWrapper:
    """
    只是一个输出点的外壳，供对外操作
    """

    def __init__(self, input_builder, name: str):
        self.name = name
        self.input_builder = input_builder


class InputBuilder:
    def __init__(self, node: EndNode):
        self.node = node
        # 获取节点的输入
        keys = self.node.input().schema()["properties"].keys()
        self.keys = set(keys)
        self.up_streams_set = set()

    def __getattr__(self, name):
        if name in self.keys:
            # 返回一个属性包装器，供对外操作
            return InPropWrapper(self, name)

    def on_attach(self, other_output_builder):
        other_node = other_output_builder.node
        if other_output_builder.node.id not in self.up_streams_set:
            self.up_streams_set.add(other_output_builder.node.id)
        else:
            raise RuntimeError(f"{self.node.id}-{self.node.label} "
                               f"is already connected with {other_node.id}-{other_node.label}")


class NodeConnector:
    def __init__(self, node: Union[StartNode, EndNode]):
        self.node = node
        self.OUT = self.IN = None
        if isinstance(node, StartNode) is True or isinstance(node, AttachTo):
            self.OUT = OutputBuilder(self.node)
        if isinstance(node, EndNode) is True:
            self.IN = InputBuilder(self.node)

    def build(self, dag: Dag):
        if self.OUT is not None:
            self.OUT.build(dag)


class DagBuilder:
    def __init__(self, dag: Dag):
        self.dag = dag
        self.node_connectors = list()

    def allocate(self, type_: Type, *args, **kwargs):
        connector = NodeConnector(self.dag.allocate(type_, *args, **kwargs))
        self.node_connectors.append(connector)
        return connector

    def allocate_root(self, type_: Type, *args, **kwargs):
        connector = self.allocate(type_, *args, **kwargs)
        self.dag.root = connector.node
        return connector

    def build(self) -> Dag:
        for connector in self.node_connectors:
            connector.build(self.dag)

        return self.dag
