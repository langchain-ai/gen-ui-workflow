from typing import TypedDict, List, Dict, Any, Optional, Annotated, Union
from typing_extensions import TypeGuard


class ComponentNode(TypedDict, total=False):
    """
    A component node that can either be concrete or contain an idea to expand.

    If 'idea' is present, this component needs expansion (spawn new LLM call).
    If 'idea' is None, this is a concrete/final component.
    """

    id: str  # Required
    type: str  # Required
    parent_id: Optional[str]  # Required
    props: Dict[str, Any]  # Required
    idea: Optional[str]  # Optional - high-level description to expand into children
    children: List["ComponentNode"]  # Required


class SetTree(TypedDict, total=False):
    """Sets or replaces the entire component tree."""

    component_tree: Optional[ComponentNode]


class AddChildren(TypedDict):
    """Adds children to a specific component in the tree."""

    component_id: str
    children: List[ComponentNode]


# Union of all possible update types
ComponentTreeUpdate = Union[SetTree, AddChildren]


def _is_set_tree(update: ComponentTreeUpdate) -> TypeGuard[SetTree]:
    """Type guard to check if update is SetTree."""
    return "component_tree" in update


def _is_add_children(update: ComponentTreeUpdate) -> TypeGuard[AddChildren]:
    """Type guard to check if update is AddChildren."""
    return "component_id" in update and "children" in update


def merge_component_updates(
    existing: Optional[ComponentNode], updates: List[ComponentTreeUpdate]
) -> Optional[ComponentNode]:
    """
    Reducer function to merge component updates into the tree.

    Updates can be:
    1. SetTree: {"component_tree": ComponentNode} - Sets the entire tree
    2. AddChildren: {"component_id": str, "children": []} - Merges children into component

    This gets called automatically by LangGraph when multiple nodes return updates.
    """
    if not updates:
        return existing

    # Start with existing tree or None
    tree: Optional[ComponentNode] = existing

    for update in updates:
        if _is_set_tree(update):
            # Set/replace the entire tree
            tree_update = update.get("component_tree")
            if tree is None and tree_update is not None:
                tree = tree_update
            elif tree_update is not None:
                # Root should only be set once, but handle gracefully
                tree = tree_update
        elif _is_add_children(update):
            # Add children to a specific component
            component_id = update["component_id"]
            children = update["children"]
            if tree:
                tree = _insert_children(tree, component_id, children)

    return tree


def _insert_children(
    tree: ComponentNode, component_id: str, children: List[ComponentNode]
) -> ComponentNode:
    """
    Insert children into a component by ID and mark it as complete.
    Recursively searches the tree.
    """
    if tree["id"] == component_id:
        # Found the target - update it and clear the idea
        updated: ComponentNode = {
            **tree,
            "children": children,
            "idea": None,  # Clear idea once expanded
        }
        return updated

    # Recurse into children
    if tree.get("children"):
        return {
            **tree,
            "children": [
                _insert_children(child, component_id, children)
                for child in tree["children"]
            ],
        }

    return tree


class GraphState(TypedDict):
    """State for the GenUI workflow graph."""

    # Input
    user_prompt: str

    # Component tree (uses custom reducer to merge updates)
    component_tree: Annotated[Optional[ComponentNode], merge_component_updates]

    # Error handling
    error: Optional[str]
