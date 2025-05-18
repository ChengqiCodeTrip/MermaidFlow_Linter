from collections import defaultdict
from pathlib import Path
from scripts.MermaidSegmentor import MermaidSegmentor
from pydantic import BaseModel, Field
import regex as re

class ConfigCls(BaseModel):
    segmentor_config: Path = Field(..., description="Path to the segmentor configuration file")
    checker_config: Path = Field(..., description="Path to the checker configuration file")

class OperatorInfo(BaseModel):
    node_type: str = Field(..., description="Type of the node")
    description: str = Field(..., description="Description of the node type")
    required_connections: dict = Field(default_factory=dict, description="Dictionary of required input and output connections")

class SegmentParts(BaseModel):
    head: list = Field(default=None, description="Flowchart TD declaration")
    comments: list = Field(default=None, description="Comment lines in the mermaid diagram")
    nodes_initialization: list = Field(default=None, description="Node initialization statements")
    empty: list = Field(default=None, description="Empty lines in the diagram")
    class_definition: list = Field(default=None, description="Class definition statements")
    nodes_assignment: list = Field(default=None, description="Node class assignment statements")
    nodes_connections: list = Field(default=None, description="Node connection statements")

class ConnectionInfo(BaseModel):
    source: str = Field(default=None, description="The source node name that connects to the target node")
    target: str = Field(default=None, description="The target node name that receives connection from the source node")
    label: str | None = Field(default=None, description="The label text on the connection line if present, otherwise None")

class MermaidCheker():
    
    def __init__(self, config: ConfigCls):
        self.segmentor = MermaidSegmentor(config.segmentor_config)
        self.checker_config = config.checker_config
        self.operation_register = defaultdict(OperatorInfo)
    
    def register_for_node_type(self, node_type_info: OperatorInfo):
        self.operation_register[node_type_info.node_type] = node_type_info
    
    def extract_node_class_mapping(self, segmentation: SegmentParts):
        node_assignment = segmentation.nodes_assignment
        # get (node name, class) pair from node_assignment
        node_class_pairs = []
        
        if node_assignment:
            for assignment in node_assignment:
                # Extract node name and class from assignment line (format: "class node_name class_name")
                match = re.match(r'^\s*class\s+(\w+)\s+(\w+)$', assignment)
                if match:
                    node_name, class_name = match.groups()
                    node_class_pairs.append((node_name, class_name))
        
        # Create a dictionary mapping node names to their classes
        node_to_class_map = dict(node_class_pairs)
        
        return node_to_class_map
    
    def extract_node_connection_map(self, segmentation: SegmentParts):
        nodes_connections = segmentation.nodes_connections
        extracted_node_connection = []
        for nodes_connection in nodes_connections:
            # Extract source, target, and label from connection line (format: "source --> |label| target" or "source --> target")
            match = re.match(r'^\s*(\w+)\s*-->\s*(?:\|(.*?)\|)?\s*(\w+)$', nodes_connection)
            if match:
                source, label, target = match.groups()
                connection_info = ConnectionInfo(
                    source=source,
                    target=target,
                    label=label  # Will be None if no label was present
                )
                extracted_node_connection.append(connection_info)
        return extracted_node_connection

    def __call__(self, file_path: Path): 
        segmentation = self.segmentor(file_path)
        segmentation = SegmentParts(**segmentation)
        node_class = self.extract_node_class_mapping(segmentation)
        nodes_connections_info = self.extract_node_connection_map(segmentation)

        ...
