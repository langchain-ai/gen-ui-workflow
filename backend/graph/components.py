"""
Opinionated component library for GenUI.
Defines available components and their schemas.
"""

from typing import Dict, Any, List, Literal
from enum import Enum


class ComponentType(str, Enum):
    """Available component types in the GenUI library."""
    # Layout
    RAIL = "rail"  # Sidebar/navigation rail
    STACK = "stack"  # Vertical stack container
    CLUSTER = "cluster"  # Horizontal cluster/row
    GRID = "grid"  # Grid layout
    DIVIDER = "divider"  # Visual separator

    # Content
    CARD = "card"  # Card container with optional header/footer
    PANEL = "panel"  # Simple bordered container
    TABS = "tabs"  # Tabbed interface
    ACCORDION = "accordion"  # Collapsible sections

    # Typography
    HEADER = "header"  # Page/section header
    TEXT = "text"  # Body text
    LABEL = "label"  # Form label or small text
    CODE = "code"  # Code block

    # Media
    IMAGE = "image"  # Image component
    ICON = "icon"  # Icon component
    AVATAR = "avatar"  # User avatar

    # Interactive
    BUTTON = "button"  # Button
    INPUT = "input"  # Text input
    SELECT = "select"  # Dropdown select
    CHECKBOX = "checkbox"  # Checkbox
    TOGGLE = "toggle"  # Toggle switch
    SLIDER = "slider"  # Range slider

    # Data Display
    TABLE = "table"  # Data table
    LIST = "list"  # Vertical list
    STAT = "stat"  # Stat/metric display
    BADGE = "badge"  # Badge/tag
    PROGRESS = "progress"  # Progress bar
    CHART = "chart"  # Chart component

    # Navigation
    BREADCRUMB = "breadcrumb"  # Breadcrumb navigation
    MENU = "menu"  # Menu component
    LINK = "link"  # Hyperlink


# Component schemas defining required/optional props
COMPONENT_SCHEMAS: Dict[ComponentType, Dict[str, Any]] = {
    # Layout
    ComponentType.RAIL: {
        "props": {
            "position": {"type": "string", "enum": ["left", "right"], "default": "left"},
            "width": {"type": "string", "default": "240px"},
            "collapsible": {"type": "boolean", "default": False},
        },
        "allows_children": True,
        "description": "Sidebar navigation rail for app navigation"
    },
    ComponentType.STACK: {
        "props": {
            "gap": {"type": "string", "default": "1rem"},
            "align": {"type": "string", "enum": ["start", "center", "end", "stretch"], "default": "stretch"},
        },
        "allows_children": True,
        "description": "Vertical stack layout"
    },
    ComponentType.CLUSTER: {
        "props": {
            "gap": {"type": "string", "default": "1rem"},
            "justify": {"type": "string", "enum": ["start", "center", "end", "between", "around"], "default": "start"},
            "align": {"type": "string", "enum": ["start", "center", "end", "baseline"], "default": "center"},
            "wrap": {"type": "boolean", "default": True},
        },
        "allows_children": True,
        "description": "Horizontal cluster/row layout"
    },
    ComponentType.GRID: {
        "props": {
            "columns": {"type": "number", "default": 12},
            "gap": {"type": "string", "default": "1rem"},
            "minColumnWidth": {"type": "string", "default": "250px"},
        },
        "allows_children": True,
        "description": "Responsive grid layout"
    },
    ComponentType.DIVIDER: {
        "props": {
            "orientation": {"type": "string", "enum": ["horizontal", "vertical"], "default": "horizontal"},
            "spacing": {"type": "string", "default": "1rem"},
        },
        "allows_children": False,
        "description": "Visual divider/separator"
    },

    # Content
    ComponentType.CARD: {
        "props": {
            "variant": {"type": "string", "enum": ["outlined", "elevated", "filled"], "default": "outlined"},
            "padding": {"type": "string", "default": "1rem"},
            "header": {"type": "string", "optional": True},
            "footer": {"type": "string", "optional": True},
        },
        "allows_children": True,
        "description": "Card container with optional header and footer"
    },
    ComponentType.PANEL: {
        "props": {
            "padding": {"type": "string", "default": "1rem"},
            "rounded": {"type": "boolean", "default": True},
        },
        "allows_children": True,
        "description": "Simple bordered container"
    },
    ComponentType.TABS: {
        "props": {
            "tabs": {"type": "array", "required": True},
            "defaultTab": {"type": "string", "optional": True},
        },
        "allows_children": True,
        "description": "Tabbed interface"
    },
    ComponentType.ACCORDION: {
        "props": {
            "items": {"type": "array", "required": True},
            "allowMultiple": {"type": "boolean", "default": False},
        },
        "allows_children": False,
        "description": "Collapsible accordion sections"
    },

    # Typography
    ComponentType.HEADER: {
        "props": {
            "level": {"type": "number", "enum": [1, 2, 3, 4, 5, 6], "default": 1},
            "text": {"type": "string", "required": True},
        },
        "allows_children": False,
        "description": "Page or section header"
    },
    ComponentType.TEXT: {
        "props": {
            "content": {"type": "string", "required": True},
            "size": {"type": "string", "enum": ["xs", "sm", "base", "lg", "xl"], "default": "base"},
            "weight": {"type": "string", "enum": ["normal", "medium", "bold"], "default": "normal"},
        },
        "allows_children": False,
        "description": "Body text content"
    },
    ComponentType.LABEL: {
        "props": {
            "text": {"type": "string", "required": True},
            "htmlFor": {"type": "string", "optional": True},
        },
        "allows_children": False,
        "description": "Form label or small text"
    },
    ComponentType.CODE: {
        "props": {
            "code": {"type": "string", "required": True},
            "language": {"type": "string", "optional": True},
            "lineNumbers": {"type": "boolean", "default": False},
        },
        "allows_children": False,
        "description": "Code block with syntax highlighting"
    },

    # Media
    ComponentType.IMAGE: {
        "props": {
            "src": {"type": "string", "required": True},
            "alt": {"type": "string", "required": True},
            "width": {"type": "string", "optional": True},
            "height": {"type": "string", "optional": True},
            "objectFit": {"type": "string", "enum": ["contain", "cover", "fill"], "default": "cover"},
        },
        "allows_children": False,
        "description": "Image component"
    },
    ComponentType.ICON: {
        "props": {
            "name": {"type": "string", "required": True},
            "size": {"type": "string", "default": "1em"},
            "color": {"type": "string", "optional": True},
        },
        "allows_children": False,
        "description": "Icon component"
    },
    ComponentType.AVATAR: {
        "props": {
            "src": {"type": "string", "optional": True},
            "name": {"type": "string", "required": True},
            "size": {"type": "string", "enum": ["sm", "md", "lg", "xl"], "default": "md"},
        },
        "allows_children": False,
        "description": "User avatar with fallback to initials"
    },

    # Interactive
    ComponentType.BUTTON: {
        "props": {
            "text": {"type": "string", "required": True},
            "variant": {"type": "string", "enum": ["primary", "secondary", "outline", "ghost", "danger"], "default": "primary"},
            "size": {"type": "string", "enum": ["sm", "md", "lg"], "default": "md"},
            "disabled": {"type": "boolean", "default": False},
            "icon": {"type": "string", "optional": True},
        },
        "allows_children": False,
        "description": "Button component"
    },
    ComponentType.INPUT: {
        "props": {
            "type": {"type": "string", "enum": ["text", "email", "password", "number", "tel", "url"], "default": "text"},
            "placeholder": {"type": "string", "optional": True},
            "label": {"type": "string", "optional": True},
            "required": {"type": "boolean", "default": False},
            "disabled": {"type": "boolean", "default": False},
        },
        "allows_children": False,
        "description": "Text input field"
    },
    ComponentType.SELECT: {
        "props": {
            "options": {"type": "array", "required": True},
            "label": {"type": "string", "optional": True},
            "placeholder": {"type": "string", "optional": True},
            "multiple": {"type": "boolean", "default": False},
        },
        "allows_children": False,
        "description": "Dropdown select"
    },
    ComponentType.CHECKBOX: {
        "props": {
            "label": {"type": "string", "required": True},
            "checked": {"type": "boolean", "default": False},
            "disabled": {"type": "boolean", "default": False},
        },
        "allows_children": False,
        "description": "Checkbox input"
    },
    ComponentType.TOGGLE: {
        "props": {
            "label": {"type": "string", "optional": True},
            "checked": {"type": "boolean", "default": False},
            "disabled": {"type": "boolean", "default": False},
        },
        "allows_children": False,
        "description": "Toggle switch"
    },
    ComponentType.SLIDER: {
        "props": {
            "min": {"type": "number", "default": 0},
            "max": {"type": "number", "default": 100},
            "step": {"type": "number", "default": 1},
            "value": {"type": "number", "optional": True},
            "label": {"type": "string", "optional": True},
        },
        "allows_children": False,
        "description": "Range slider"
    },

    # Data Display
    ComponentType.TABLE: {
        "props": {
            "columns": {"type": "array", "required": True},
            "data": {"type": "array", "required": True},
            "sortable": {"type": "boolean", "default": False},
            "striped": {"type": "boolean", "default": True},
        },
        "allows_children": False,
        "description": "Data table"
    },
    ComponentType.LIST: {
        "props": {
            "items": {"type": "array", "required": True},
            "ordered": {"type": "boolean", "default": False},
            "spacing": {"type": "string", "default": "0.5rem"},
        },
        "allows_children": False,
        "description": "Vertical list"
    },
    ComponentType.STAT: {
        "props": {
            "label": {"type": "string", "required": True},
            "value": {"type": "string", "required": True},
            "change": {"type": "string", "optional": True},
            "trend": {"type": "string", "enum": ["up", "down", "neutral"], "optional": True},
        },
        "allows_children": False,
        "description": "Stat/metric display"
    },
    ComponentType.BADGE: {
        "props": {
            "text": {"type": "string", "required": True},
            "variant": {"type": "string", "enum": ["default", "success", "warning", "error", "info"], "default": "default"},
            "size": {"type": "string", "enum": ["sm", "md", "lg"], "default": "md"},
        },
        "allows_children": False,
        "description": "Badge or tag"
    },
    ComponentType.PROGRESS: {
        "props": {
            "value": {"type": "number", "required": True},
            "max": {"type": "number", "default": 100},
            "label": {"type": "string", "optional": True},
            "showValue": {"type": "boolean", "default": True},
        },
        "allows_children": False,
        "description": "Progress bar"
    },
    ComponentType.CHART: {
        "props": {
            "type": {"type": "string", "enum": ["line", "bar", "pie", "area", "scatter"], "required": True},
            "data": {"type": "array", "required": True},
            "xAxis": {"type": "string", "optional": True},
            "yAxis": {"type": "string", "optional": True},
        },
        "allows_children": False,
        "description": "Chart visualization"
    },

    # Navigation
    ComponentType.BREADCRUMB: {
        "props": {
            "items": {"type": "array", "required": True},
            "separator": {"type": "string", "default": "/"},
        },
        "allows_children": False,
        "description": "Breadcrumb navigation"
    },
    ComponentType.MENU: {
        "props": {
            "items": {"type": "array", "required": True},
            "orientation": {"type": "string", "enum": ["horizontal", "vertical"], "default": "vertical"},
        },
        "allows_children": False,
        "description": "Menu component"
    },
    ComponentType.LINK: {
        "props": {
            "href": {"type": "string", "required": True},
            "text": {"type": "string", "required": True},
            "external": {"type": "boolean", "default": False},
        },
        "allows_children": False,
        "description": "Hyperlink"
    },
}


def get_component_schema(component_type: ComponentType) -> Dict[str, Any]:
    """Get schema for a component type."""
    return COMPONENT_SCHEMAS.get(component_type, {})


def get_all_component_types() -> List[str]:
    """Get list of all available component types."""
    return [ct.value for ct in ComponentType]


def allows_children(component_type: ComponentType) -> bool:
    """Check if a component type can have children."""
    schema = get_component_schema(component_type)
    return schema.get("allows_children", False)


def get_component_library_description() -> str:
    """Generate a description of the component library for LLM."""
    lines = ["Available GenUI Components:\n"]

    categories = {
        "Layout": [ComponentType.RAIL, ComponentType.STACK, ComponentType.CLUSTER, ComponentType.GRID, ComponentType.DIVIDER],
        "Content": [ComponentType.CARD, ComponentType.PANEL, ComponentType.TABS, ComponentType.ACCORDION],
        "Typography": [ComponentType.HEADER, ComponentType.TEXT, ComponentType.LABEL, ComponentType.CODE],
        "Media": [ComponentType.IMAGE, ComponentType.ICON, ComponentType.AVATAR],
        "Interactive": [ComponentType.BUTTON, ComponentType.INPUT, ComponentType.SELECT, ComponentType.CHECKBOX, ComponentType.TOGGLE, ComponentType.SLIDER],
        "Data Display": [ComponentType.TABLE, ComponentType.LIST, ComponentType.STAT, ComponentType.BADGE, ComponentType.PROGRESS, ComponentType.CHART],
        "Navigation": [ComponentType.BREADCRUMB, ComponentType.MENU, ComponentType.LINK],
    }

    for category, types in categories.items():
        lines.append(f"\n{category}:")
        for ct in types:
            schema = get_component_schema(ct)
            children_note = " (can contain children)" if schema.get("allows_children") else ""
            lines.append(f"  - {ct.value}: {schema.get('description', '')}{children_note}")

    return "\n".join(lines)
