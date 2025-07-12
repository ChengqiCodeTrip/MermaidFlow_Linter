# MermaidFlow_Linter package initialization
# This package provides tools for linting and validating Mermaid flowchart diagrams

from .scripts.MermaidChecker import MermaidCheker, ConfigCls, OperatorInfo, SegmentParts, ConnectionInfo
from pathlib import Path

__version__ = "0.1.0"
__author__ = "Chengqi"
__all__ = ["MermaidCheker", "ConfigCls", "OperatorInfo", "SegmentParts", "ConnectionInfo"]

# Default configuration paths
DEFAULT_SEGMENT_CONFIG = Path(__file__).parent / "config" / "sgement_config.json"
DEFAULT_CHECKER_CONFIG = Path(__file__).parent / "config" / "checker_config.json"

