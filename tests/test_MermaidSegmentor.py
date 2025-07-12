from pathlib import Path
mmd_path = Path("/Users/archy/Documents/MermaidFlow_Linter/tests/graph.mmd")
segment_define = Path("/Users/archy/Documents/MermaidFlow_Linter/config/sgement_config.json")
checker_config = Path("/Users/archy/Documents/MermaidFlow_Linter/config/checker_config.json")
mermaid_code = """
flowchart TD
    %% Nodes
    PROBLEM([Problem])
    C1["Custom<br/>(role: simple_solver_1)"]
    C2["Custom<br/>(role: simple_solver_2)"]
    C3["Custom<br/>(role: alternative_solver)"]
    C4["Custom<br/>(role: detailed_solution_outline)"]
    C5["Custom<br/>(role: comprehensive_solution]"]
    P["Programmer<br/>(analysis: 'Solve the math problem step by step')]
    REFINE["Custom<br/>(role: refine_solution)"]
    ENSEMBLE["ScEnsemble<br/>"]
    RETURN([Return response & cost])

    %% Styles
    classDef CustomOp fill:#d0e1f9,stroke:#4378a2,stroke-width:2px;
    classDef ProgrammerOp fill:#f9c2c2,stroke:#c23737,stroke-width:2px;
    classDef ScEnSembleOp fill:#f9e4b7,stroke:#b99b37,stroke-width:2px;
    classDef Interface fill:#e2e2f2,stroke:#6a6ab2,stroke-width:2px;

    %% Assign classes
    class C1 CustomOp
    class C2 CustomOp
    class C3 CustomOp
    class C4 CustomOp
    class C5 CustomOp
    class P ProgrammerOp
    class REFINE CustomOp
    class PROBLEM Interface
    class RETURN Interface
    class ENSEMBLE ScEnSembleOp

    %% Flow (arrows show data relationships)
    PROBLEM --> |input|C1
    PROBLEM --> |input|C2
    PROBLEM --> |input|C3
    PROBLEM --> |input|C4
    PROBLEM --> |input|C5
    PROBLEM --> |problem|P
    C1 --> ENSEMBLE
    C2 --> ENSEMBLE
    C3 --> ENSEMBLE
    C4 --> ENSEMBLE
    C5 --> ENSEMBLE
    P --> ENSEMBLE
    ENSEMBLE --> REFINE
    REFINE --> RETURN
"""

def test_read_line():
    from scripts.MermaidSegmentor import MermaidSegmentor

    segmentor = MermaidSegmentor(config=segment_define)
    segmentor(mmd_path)

def test_MermaidCheker_setup_information():
    from scripts.MermaidChecker import ConfigCls, MermaidCheker
    confg_file = ConfigCls(segmentor_config=segment_define, checker_config=checker_config)

    mermaid_checker = MermaidCheker(
        config=confg_file
    )

    output = mermaid_checker.soft_check(mmd_path)

def test_using_mermaid_code():
    from scripts.MermaidChecker import ConfigCls, MermaidCheker
    confg_file = ConfigCls(segmentor_config=segment_define, checker_config=checker_config)

    mermaid_checker = MermaidCheker(
        config=confg_file
    )
    mermaid_path = mermaid_checker.transfer_mmd_code_string_to_temp_file(mermaid_code)

    output = mermaid_checker.soft_check(mermaid_path)

def test_hard_check():
    from scripts.MermaidChecker import ConfigCls, MermaidCheker
    confg_file = ConfigCls(segmentor_config=segment_define, checker_config=checker_config)

    mermaid_checker = MermaidCheker(
        config=confg_file
    )
    mermaid_path = mermaid_checker.transfer_mmd_code_string_to_temp_file(mermaid_code)

    output = mermaid_checker.hard_check(mermaid_path)
    

def test_defined_rules_for_custom():
    ...

def test_defined_rules_for_ensemble():
    ...

def test_defined_rules_for_interface():
    ...
