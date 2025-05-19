from collections import defaultdict
import json
from pathlib import Path
from scripts.MermaidSegmentor import MermaidSegmentor
from pydantic import BaseModel, Field
import regex as re
import networkx as nx

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
        self.legal_node_type = self.extract_legal_type(self.checker_config)
    
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
    
    def extract_legal_type(self, checker_config):
        # Read through checker_config to extract legal node types
        legal_node_types = []
        
        try:
            # Load the checker configuration file
            with open(checker_config, 'r') as f:
                config_data = json.load(f)
            
            # Extract node_type from each entry in the configuration
            for node_config in config_data:
                if 'node_type' in node_config:
                    legal_node_types.append(node_config['node_type'])
                    
            return legal_node_types
        except Exception as e:
            print(f"Error reading checker configuration: {e}")
            return []
    
    def create_graph(self, nodes_connection_info):
        G = nx.DiGraph()
        G.add_edges_from(
            [(value.source, value.target) for value in nodes_connection_info]
        )
        return G
    
    def extract_nodes_and_connections(self, file_path):
        segmentation = self.segmentor(file_path)
        segmentation = SegmentParts(**segmentation)
        node_class = self.extract_node_class_mapping(segmentation)
        node_connections_info = self.extract_node_connection_map(segmentation)
        return node_class, node_connections_info

    def __call__(self, file_path: Path): 
        self.node_class, self.node_connection_info = self.extract_nodes_and_connections(file_path)
        self.graph = self.create_graph(self.node_connection_info)
        is_pass_all = self.detect_the_graph(self.graph, self.node_class, self.node_connection_info)

        ...

    def detect_the_graph(self, graph, node_class, node_connection_info):
        # List of all validation functions to run on the graph
        detect_functions = [
            self.W1_contain_problem_and_return_node,
            self.W2_node_connection,
            self.W3_interface_check,
            self.W4_violate_node_type,
            self.W5_ensemble_violation
        ]
        
        all_violations = []
        
        # Execute each validation function and collect violations
        for func in detect_functions:
            violations = func(graph, node_class, node_connection_info)
            all_violations.extend(violations)
        
        # Print all violations if any
        if all_violations:
            print("The following violations were detected in the graph:")
            for i, violation in enumerate(all_violations, 1):
                print(f"{i}. {violation}")
            return False
        
        print("All validations passed successfully!")
        return True

    def W1_contain_problem_and_return_node(self, graph, node_class, node_connection_info):
        """Check if the graph contains both PROBLEM and RETURN nodes"""
        violations = []
        
        if "PROBLEM" not in node_class.keys():
            violations.append("W1: Missing required 'PROBLEM' node in the flowchart, which is the starting point of the workflow")
        
        if "RETURN" not in node_class.keys():
            violations.append("W1: Missing required 'RETURN' node in the flowchart, which is the endpoint of the workflow")
        
        return violations
    
    def W2_node_connection(self, graph, node_class, node_connection_info):
        """
        Check if each node is connected to both PROBLEM and RETURN nodes.
        Each node should have a path from PROBLEM and a path to RETURN.
        """
        violations = []
        
        for node in node_class.keys():
            if node in ["PROBLEM", "RETURN"]:
                continue
                
            is_connect_to_problem = nx.has_path(graph, "PROBLEM", node)
            is_connect_to_return = nx.has_path(graph, node, "RETURN")
            
            if not (is_connect_to_problem and is_connect_to_return):
                violations.append(f"W2: Node '{node}' is not properly connected in the workflow. Connected to PROBLEM: {is_connect_to_problem}, Connected to RETURN: {is_connect_to_return}. Each node must have a path from PROBLEM and a path to RETURN.")
        
        return violations

    def W3_interface_check(self, graph, node_class, node_connection_info):
        """Check if PROBLEM and RETURN nodes are of Interface class type"""
        violations = []
        
        if "PROBLEM" in node_class:
            if node_class["PROBLEM"] != "Interface":
                violations.append("W3: PROBLEM node must be of 'Interface' class type")
        
        if "RETURN" in node_class:
            if node_class["RETURN"] != "Interface":
                violations.append("W3: RETURN node must be of 'Interface' class type")
        
        return violations

    def W4_violate_node_type(self, graph, node_class, node_connection_info):
        """Check if all nodes have valid node types according to configuration"""
        violations = []
        
        for node, node_type in node_class.items():
            if node_type not in self.legal_node_type:
                violations.append(f"W4: Node '{node}' has an invalid type '{node_type}'. Valid types are: {', '.join(self.legal_node_type)}")
        
        return violations
    
    def W5_ensemble_violation(self, graph: nx.DiGraph, node_class, node_connection_info):
        violations = []
        
        for node, node_type in node_class.items():
            if node_type == "ScEnSembleOp":
                incoming = list(graph.predecessors(node))
                if len(incoming) < 2:
                    violations.append(f"W5: ScEnSembleOp node '{node}' must have at least 2 incoming connections, but only has {len(incoming)}. Ensemble operations require multiple inputs to function properly.")
        
        return violations