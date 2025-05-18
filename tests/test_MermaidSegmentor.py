from pathlib import Path
mmd_path = Path("/Users/archy/Documents/MermaidFlow_Linter/tests/graph.mmd")
segment_define = Path("/Users/archy/Documents/MermaidFlow_Linter/config/sgement_config.json")
checker_config = Path("/Users/archy/Documents/MermaidFlow_Linter/config/checker_config.json")

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

    output = mermaid_checker(mmd_path)

def test_defined_rules_for_custom():
    ...

def test_defined_rules_for_ensemble():
    ...

def test_defined_rules_for_interface():
    ...
