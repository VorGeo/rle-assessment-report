#!/usr/bin/env -S pixi run python
"""
MyST-MD plugin for preprocessing ecosystem YAML configuration files.

This plugin loads ecosystem configuration from YAML files and makes the data
available to MyST documents through transforms and directives.
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Any, Dict, List

# Plugin specification for MyST
PLUGIN_SPEC = {
    "name": "ecosystem-config-plugin",
    "transforms": [
        {
            "name": "ecosystem-config",
            "doc": "Load ecosystem configuration from YAML files and inject data into page frontmatter"
        }
    ],
    "directives": [
        {
            "name": "ecosystem-config",
            "doc": "Load and display ecosystem configuration data",
            "alias": ["eco-config"],
            "arg": {
                "type": "string",
                "doc": "Ecosystem ID (e.g., MMR-T1.1.1)",
                "required": True
            },
            "options": {
                "field": {
                    "type": "string",
                    "doc": "Specific field to display (optional)"
                },
                "format": {
                    "type": "string",
                    "doc": "Output format: yaml, json, or markdown (default: markdown)"
                }
            }
        }
    ],
    "roles": [
        {
            "name": "eco",
            "doc": "Inline ecosystem configuration field reference",
            "alias": ["ecosystem"],
            "body": {
                "type": "string",
                "required": True
            }
        }
    ]
}


def load_ecosystem_config(ecosystem_id: str) -> Dict[str, Any]:
    """
    Load ecosystem configuration from YAML file.

    Args:
        ecosystem_id: The ecosystem identifier (e.g., MMR-T1.1.1)

    Returns:
        Dictionary containing the ecosystem configuration
    """
    config_path = Path(f"config/ecosystem_config/{ecosystem_id}.yaml")

    if not config_path.exists():
        raise FileNotFoundError(f"Ecosystem config not found: {config_path}")

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def format_ecosystem_names_local(names_data: List[Dict[str, str]]) -> str:
    """
    Format the ecosystem_names_local field as markdown with citations.

    Args:
        names_data: List of dicts with 'name' and 'reference' keys

    Returns:
        Formatted markdown string with citations
    """
    if not names_data:
        return ""

    citations = ", ".join([
        f"{item['name']} [{item['reference']}]"
        for item in names_data
    ])
    return citations


def run_directive(directive_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Execute the ecosystem-config directive.

    Args:
        directive_data: Directive data from MyST containing args and options

    Returns:
        List of AST nodes to insert
    """
    ecosystem_id = directive_data.get("arg")
    field = directive_data.get("options", {}).get("field")
    output_format = directive_data.get("options", {}).get("format", "markdown")

    try:
        config = load_ecosystem_config(ecosystem_id)

        # If specific field requested, extract it
        if field:
            data = config.get(field)
        else:
            data = config

        # Format output based on requested format
        if output_format == "json":
            output_text = json.dumps(data, indent=2)
            return [{
                "type": "code",
                "lang": "json",
                "value": output_text
            }]
        elif output_format == "yaml":
            output_text = yaml.dump(data, default_flow_style=False)
            return [{
                "type": "code",
                "lang": "yaml",
                "value": output_text
            }]
        else:  # markdown format
            # Special handling for ecosystem_names_local
            if field == "ecosystem_names_local" and isinstance(data, list):
                output_text = format_ecosystem_names_local(data)
            elif isinstance(data, (dict, list)):
                output_text = yaml.dump(data, default_flow_style=False)
            else:
                output_text = str(data)

            return [{
                "type": "paragraph",
                "children": [{
                    "type": "text",
                    "value": output_text
                }]
            }]

    except Exception as e:
        # Return error message as admonition
        return [{
            "type": "admonition",
            "kind": "danger",
            "children": [{
                "type": "paragraph",
                "children": [{
                    "type": "text",
                    "value": f"Error loading ecosystem config: {str(e)}"
                }]
            }]
        }]


def run_role(role_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Execute the eco inline role.

    Format: {eco}`MMR-T1.1.1:field_name`

    Args:
        role_data: Role data from MyST containing the value or body

    Returns:
        List of AST nodes to insert inline
    """
    # MyST may pass the content as "value" or "body"
    value = role_data.get("body", role_data.get("value", ""))

    try:
        # Parse the role value: ecosystem_id:field_name
        if ":" in value:
            ecosystem_id, field_name = value.split(":", 1)
        else:
            raise ValueError("Role format should be: {eco}`ecosystem_id:field_name`")

        config = load_ecosystem_config(ecosystem_id)

        # Support nested field access with dot notation
        field_parts = field_name.split(".")
        data = config
        for part in field_parts:
            data = data[part]

        # Format the output
        if isinstance(data, list) and field_name == "ecosystem_names_local":
            text = format_ecosystem_names_local(data)
        else:
            text = str(data)

        return [{
            "type": "text",
            "value": text
        }]

    except Exception as e:
        return [{
            "type": "text",
            "value": f"[Error: {str(e)}]"
        }]


def run_transform(ast_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform AST to inject ecosystem configuration data.

    This transform looks for frontmatter with ecosystem_id and loads
    the corresponding configuration into the page data.

    Args:
        ast_data: The MyST AST as a dictionary

    Returns:
        Modified AST with ecosystem data injected
    """
    # Check if the document has frontmatter with ecosystem_id
    frontmatter = ast_data.get("frontmatter", {})
    ecosystem_id = frontmatter.get("ecosystem_id")

    if ecosystem_id:
        try:
            config = load_ecosystem_config(ecosystem_id)

            # Inject the config into frontmatter under 'ecosystem' key
            if "frontmatter" not in ast_data:
                ast_data["frontmatter"] = {}

            ast_data["frontmatter"]["ecosystem"] = config

        except Exception as e:
            # Log error but don't fail the build
            print(f"Warning: Failed to load ecosystem config for {ecosystem_id}: {e}",
                  file=sys.stderr)

    return ast_data


def main():
    """Main entry point for the plugin."""
    import argparse

    parser = argparse.ArgumentParser(description="Ecosystem Config MyST Plugin")
    parser.add_argument("--role", action="store_true", help="Execute as a role")
    parser.add_argument("--directive", action="store_true", help="Execute as a directive")
    parser.add_argument("--transform", action="store_true", help="Execute as a transform")
    # Accept any additional arguments that MyST might pass
    parser.add_argument("directive_name", nargs="?", help="Directive name (ignored)")

    args = parser.parse_args()

    # Execute the appropriate function based on argument
    if args.directive or args.role or args.transform:
        # Read input from stdin when executing a function
        input_data = json.load(sys.stdin)

        if args.directive:
            result = run_directive(input_data)
        elif args.role:
            result = run_role(input_data)
        elif args.transform:
            result = run_transform(input_data)
    else:
        # No argument provided - print plugin spec
        result = PLUGIN_SPEC

    # Write output to stdout
    json.dump(result, sys.stdout, indent=2)
    print()  # Add newline for readability


if __name__ == "__main__":
    main()
