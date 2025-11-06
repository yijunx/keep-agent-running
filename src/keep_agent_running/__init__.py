"""
Keep Agent Running - Project Runtime Engine

A DFS/BFS-based project runtime engine that orchestrates complex problem-solving
through task decomposition, virtual environments, and collaborative execution.
"""

from .config import settings
from .utils import LLMConfig, make_output_into_pydantic_models, make_output_into_pydantic_model_list

__version__ = "0.1.0"
__all__ = ["settings", "LLMConfig", "make_output_into_pydantic_models", "make_output_into_pydantic_model_list"]