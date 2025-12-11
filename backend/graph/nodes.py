"""
Unified node implementation for recursive idea expansion with map-reduce.
"""

from typing import Any, Dict, List, Optional, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import Send, END
from .state import GraphState, ComponentNode, ComponentTreeUpdate, SetTree, AddChildren
from .components import get_component_library_description


class ComponentListOutput(TypedDict):
    """Output schema for component list generation."""

    components: List[ComponentNode]


def create_expansion_prompt(
    idea: str,
    component_id: Optional[str] = None,
    parent_context: str = "",
) -> str:
    """
    Create prompt for expanding an idea into components.

    The idea itself defines the scope - no need to treat root vs child differently.
    """
    component_library = get_component_library_description()

    # Build context section
    if parent_context:
        context_section = f"""Context: {parent_context}

Expand this idea: "{idea}"
"""
    else:
        context_section = f"""Expand this idea: "{idea}"
"""

    # ID prefix for nested components
    id_prefix = f"{component_id}-" if component_id else ""

    return f"""{context_section}

{component_library}

YOUR TASK:
Generate a list of components that fulfill this idea. You MUST use the recursive "idea" pattern to break down complex UIs into manageable pieces.

CRITICAL: When to use "idea" field (USE LIBERALLY):
1. ANY section that could have its own internal structure
2. ANY data display (charts, tables, lists with multiple items)
3. ANY repeated patterns (cards in a grid, items in a list)
4. ANY complex interactive elements (forms, dialogs, multi-step flows)
5. When you're not sure of exact content/layout details

Only create concrete children for SIMPLE elements:
- Single text labels, headers, buttons
- Simple icons or images with known props
- Basic layout wrappers (stack, cluster, grid)

COMPONENT STRUCTURE:
Each component MUST have:
- id: unique identifier with prefix "{id_prefix}" (e.g., "{id_prefix}stack-1")
- type: exact type from GenUI library
- props: minimal props only (don't over-specify)
- idea: (CRITICAL) use this to defer complexity to recursive expansion
- children: (optional) ONLY for simple, obvious nested elements

GOOD EXAMPLES (notice heavy use of "idea"):
{{
  "id": "{id_prefix}dashboard",
  "type": "stack",
  "props": {{"gap": "2rem"}},
  "children": [
    {{"id": "{id_prefix}header", "type": "header", "props": {{"level": 1, "text": "Dashboard"}}}},
    {{
      "id": "{id_prefix}metrics",
      "type": "grid",
      "props": {{"columns": 3}},
      "idea": "three metric cards showing revenue, users, and growth"
    }},
    {{
      "id": "{id_prefix}charts",
      "type": "stack",
      "props": {{}},
      "idea": "sales chart and user activity chart"
    }}
  ]
}}

BAD EXAMPLE (too concrete, no delegation):
{{
  "id": "{id_prefix}dashboard",
  "type": "stack",
  "children": [
    {{"id": "{id_prefix}card1", "type": "card", "children": [...]}},  ❌ Should use "idea"
    {{"id": "{id_prefix}card2", "type": "card", "children": [...]}},  ❌ Should use "idea"
  ]
}}

Now generate components. Remember: USE "idea" LIBERALLY to delegate complexity!
"""


def expand_component(state: Dict[str, Any]) -> ComponentTreeUpdate:
    """
    Unified node that expands an idea into components.

    This node handles BOTH:
    1. Root expansion (state has user_prompt, no component_id)
       Returns: SetTree
    2. Child expansion (state has component_id, component_type, idea from Send)
       Returns: AddChildren

    Returns simple updates that the reducer merges into the tree automatically.
    """
    # Determine if this is root or child expansion
    is_root = "component_id" not in state

    if is_root:
        # Root expansion - create top-level structure
        idea = state["user_prompt"]
        component_id = "root"
        parent_context = ""
    else:
        # Child expansion from Send
        component_id = state["component_id"]
        idea = state["idea"]
        parent_context = state.get("parent_context", "")

    print(f"Expanding {'ROOT' if is_root else component_id}: {idea[:60]}...")

    # Generate expansion using structured output
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0.7)
    llm_with_structure = llm.with_structured_output(ComponentListOutput)

    prompt = create_expansion_prompt(idea, component_id, parent_context)

    messages = [
        SystemMessage(
            content="""You are a GenUI component architect. You expand ideas into component structures.

Key principles:
- Stay focused on the current scope
- Use "idea" fields to delegate complexity
- Generate simple children directly
- Let recursion handle the details"""
        ),
        HumanMessage(content=prompt),
    ]

    response = llm_with_structure.invoke(messages)
    components = response["components"]
    print(f"Generated {len(components)} components")

    # Return simple update - let the reducer merge it
    if is_root:
        # For root, return the complete tree
        result_tree: Optional[ComponentNode]

        if len(components) == 1:
            result_tree = components[0]
        elif len(components) > 1:
            # Multiple roots - wrap in container
            result_tree = ComponentNode(
                id="root",
                type="stack",
                parent_id=None,
                props={"gap": "2rem"},
                idea=None,
                children=components,
            )
        else:
            result_tree = None

        # Return SetTree - reducer sets the entire tree
        return SetTree(component_tree=result_tree)
    else:
        # Return AddChildren - reducer merges children into component
        return AddChildren(component_id=component_id, children=components)


def should_continue_expansion(state: GraphState):
    """
    Decide whether to continue expanding ideas or finish.

    Returns:
        List[Send] if there are pending ideas (for parallel expansion)
        END if all ideas are resolved
    """
    tree = state.get("component_tree")
    print(f"Checking for pending ideas...")
    if not tree:
        return END

    # Collect all pending ideas
    sends = []

    def traverse(node: ComponentNode, context_path: List[str]):
        if node.get("idea"):
            sends.append(
                Send(
                    "expand_component",
                    {
                        "component_id": node["id"],
                        "component_type": node["type"],
                        "idea": node["idea"],
                        "parent_context": " > ".join(context_path),
                    },
                )
            )
        new_context = context_path + [f"{node['type']}:{node['id']}"]
        for child in node.get("children", []):
            traverse(child, new_context)

    traverse(tree, [])

    if sends:
        print(f"Found {len(sends)} pending ideas to expand in parallel")
        return sends
    else:
        print("No more ideas, ending")
        return END
