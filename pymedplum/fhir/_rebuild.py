"""Central registry for handling model rebuilding with circular references.

This module provides a centralized approach to resolving forward references
in Pydantic models with circular dependencies. Models register themselves
upon module import, and are rebuilt after all modules are loaded.
"""

from typing import Any

# Global namespace that collects all models
_models_namespace: dict[str, Any] = {}


def register_model(name: str, model: Any) -> None:
    """Register a model to be available for forward reference resolution.

    Args:
        name: The name of the model class
        model: The model class itself
    """
    _models_namespace[name] = model


def rebuild_all_models() -> None:
    """Rebuild all registered models with the complete namespace.

    This resolves all forward references by providing each model with
    a namespace containing all registered models.
    """
    for model in _models_namespace.values():
        if hasattr(model, "model_rebuild"):
            # Pass the complete namespace for resolving forward references
            model.model_rebuild(_types_namespace=_models_namespace)
