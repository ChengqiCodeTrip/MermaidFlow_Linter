import regex as re
from pathlib import Path
import json
from collections import defaultdict


def read_though_mmd(file_path: Path):
    with open(file_path, "rb") as f:
        for line in f:
            # Decode the binary line to string
            line = line.decode("utf-8").strip()
            yield line


def extract_pattern(config_path: Path):
    with open(config_path, "r") as f:
        segment_config = json.load(f)

    # Create a dictionary mapping type_name to its regex pattern
    pattern_for_each_segment = {}
    for segment in segment_config:
        type_name = segment.get("line_type_name")
        pattern = segment.get("pattern")
        if type_name and pattern:
            # Compile the regex pattern for better performance
            pattern_for_each_segment[type_name] = re.compile(pattern)
    return pattern_for_each_segment


class MermaidSegmentor:
    def __init__(self, config: Path):
        self.pattern_for_each_segment = extract_pattern(config)

    def _classify_lines(self, file_path: Path) -> dict:
        segmentations = defaultdict(list)

        for line in read_though_mmd(file_path):
            classify_counter = 0
            for segment_name, pattern in self.pattern_for_each_segment.items():
                if pattern.match(line):
                    segmentations[segment_name].append(line)
                    classify_counter += 1

            assert classify_counter > 0, f"Line '{line}' doesn't belong to any defined type, please check your pattern definitions whether complete"

            assert classify_counter <= 1, (
                f"Line '{line}' has been classified into {classify_counter} categories, expected at most 1"
            )
        return segmentations

    """
    Read through the Mermiad code and analysis each line of it to map into given segmentation type
    """

    def __call__(self, file_path: Path) -> dict:
        assert file_path.suffix == ".mmd"

        self.segmentations = self._classify_lines(file_path=file_path)
        return self.segmentations
