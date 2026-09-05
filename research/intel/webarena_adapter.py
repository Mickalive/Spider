"""
WebArena Accessibility Tree Adapter for SPIDER Fragment Extraction

Parses WebArena's split observation channels (formatted indented string + obs_nodes_info metadata)
and extracts reusable fragments with identity, hierarchy, attributes, and text.

WebArena observation format:
- obs["text"]: formatted indented string with element IDs, roles, names, properties
  Example: "[4] button \"Submit\" focused: True"
  Indentation encodes hierarchy.
- obs_nodes_info: dict mapping element ID to {backend_id, union_bound, text}
- obs["image"]: base64 screenshot (not used for extraction)

This adapter recomposes the split channels and extracts elements.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExtractedElement:
    """A single element extracted from WebArena accessibility tree."""
    element_id: int
    role: str
    name: str
    properties: dict[str, str]  # e.g. {"focused": "True", "expanded": "False"}
    parent_id: int | None
    children_ids: list[int] = field(default_factory=list)
    backend_id: int | None = None
    union_bound: list[float] | None = None
    text: str = ""
    depth: int = 0


# Regex to parse element lines like:
# [4] button "Submit" focused: True expanded: False
# [0] RootWebArea '' 
_ELEMENT_RE = re.compile(
    r'^(\s*)\[(\d+)\]\s+(\S+)\s+"([^"]*)"'
    r'(?:\s+(.*))?$'
)

# Property parsing: "focused: True" -> ("focused", "True")
_PROPERTY_RE = re.compile(r'(\w+):\s*(\S+)')

# Role normalization: WebArena uses ARIA roles
_ROLE_MAP = {
    "RootWebArea": "root",
    "WebArea": "root",
    "link": "link",
    "button": "button",
    "textbox": "textbox",
    "checkbox": "checkbox",
    "combobox": "combobox",
    "listbox": "listbox",
    "menuitem": "menuitem",
    "menuitemcheckbox": "menuitemcheckbox",
    "menubar": "menubar",
    "menu": "menu",
    "navigation": "navigation",
    "img": "img",
    "heading": "heading",
    "text": "text",
    "StaticText": "text",
    "group": "group",
    "list": "list",
    "listitem": "listitem",
    "tab": "tab",
    "tablist": "tablist",
    "tabpanel": "tabpanel",
    "tree": "tree",
    "treeitem": "treeitem",
    "article": "article",
    "region": "region",
    "dialog": "dialog",
    "alertdialog": "alertdialog",
    "alert": "alert",
    "status": "status",
    "progressbar": "progressbar",
    "slider": "slider",
    "spinbutton": "spinbutton",
    "scrollbar": "scrollbar",
    "separator": "separator",
    "toolbar": "toolbar",
    "tabpanel": "tabpanel",
    "main": "main",
    "banner": "banner",
    "contentinfo": "contentinfo",
    "complementary": "complementary",
    "form": "form",
    "search": "search",
    "table": "table",
    "row": "row",
    "cell": "cell",
    "columnheader": "columnheader",
    "rowheader": "rowheader",
    "grid": "grid",
    "figure": "figure",
    "caption": "caption",
    "mark": "mark",
    "abbr": "abbr",
    "time": "time",
    "code": "code",
    "math": "math",
    "presentation": "presentation",
    "none": "none",
}


def normalize_role(role: str) -> str:
    """Normalize ARIA role to lowercase canonical form."""
    return _ROLE_MAP.get(role, role.lower())


def parse_accessibility_tree(
    text: str,
    obs_nodes_info: dict[int, dict[str, Any]] | None = None,
) -> list[ExtractedElement]:
    """
    Parse a WebArena accessibility tree formatted string into extracted elements.

    Args:
        text: The formatted indented string from obs["text"]
        obs_nodes_info: Optional metadata dict mapping element ID to
            {backend_id, union_bound, text}

    Returns:
        List of ExtractedElement objects with hierarchy reconstructed from indentation.
    """
    if obs_nodes_info is None:
        obs_nodes_info = {}

    lines = text.strip().split("\n")
    elements: list[ExtractedElement] = []
    stack: list[tuple[int, int]] = []  # (indent_level, element_id)

    for line in lines:
        if not line.strip():
            continue

        match = _ELEMENT_RE.match(line)
        if not match:
            continue

        indent_str, id_str, role_raw, name, props_str = match.groups()
        indent_level = len(indent_str)
        element_id = int(id_str)
        role = normalize_role(role_raw)

        # Parse properties
        properties: dict[str, str] = {}
        if props_str:
            for prop_match in _PROPERTY_RE.finditer(props_str):
                prop_name, prop_val = prop_match.groups()
                properties[prop_name] = prop_val

        # Get metadata from obs_nodes_info
        meta = obs_nodes_info.get(element_id, {})
        backend_id = meta.get("backend_id")
        union_bound = meta.get("union_bound")
        meta_text = meta.get("text", "")

        # Determine parent from indentation stack
        parent_id: int | None = None
        while stack and stack[-1][0] >= indent_level:
            stack.pop()
        if stack:
            parent_id = stack[-1][1]

        elem = ExtractedElement(
            element_id=element_id,
            role=role,
            name=name,
            properties=properties,
            parent_id=parent_id,
            backend_id=backend_id,
            union_bound=union_bound,
            text=meta_text if meta_text else name,
            depth=indent_level,
        )
        elements.append(elem)
        stack.append((indent_level, element_id))

    # Second pass: populate children_ids
    parent_to_children: dict[int | None, list[int]] = {}
    for elem in elements:
        siblings = parent_to_children.setdefault(elem.parent_id, [])
        siblings.append(elem.element_id)

    # Rebuild elements with children
    result = []
    for elem in elements:
        children = parent_to_children.get(elem.element_id, [])
        result.append(ExtractedElement(
            element_id=elem.element_id,
            role=elem.role,
            name=elem.name,
            properties=elem.properties,
            parent_id=elem.parent_id,
            children_ids=children,
            backend_id=elem.backend_id,
            union_bound=elem.union_bound,
            text=elem.text,
            depth=elem.depth,
        ))

    return result


def extract_fragments_from_observation(
    obs_text: str,
    obs_nodes_info: dict[int, dict[str, Any]] | None = None,
) -> list[ExtractedElement]:
    """
    High-level entry point: extract fragments from a WebArena observation.

    This recomposes the split observation channels (text + metadata) and
    extracts elements with full identity, hierarchy, attributes, and text.
    """
    return parse_accessibility_tree(obs_text, obs_nodes_info)
