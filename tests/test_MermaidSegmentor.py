from pathlib import Path

def test_read_line():
    from scripts.MermaidSegmentor import MermaidSegmentor

    mmd_path = Path("/Users/archy/Documents/MermaidFlow_Linter/tests/graph.mmd")
    segment_define = Path("/Users/archy/Documents/MermaidFlow_Linter/config/sgement_config.json")
    
    segmentor = MermaidSegmentor(config=segment_define)
    segmentor(mmd_path)
