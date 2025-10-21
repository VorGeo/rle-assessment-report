#!/usr/bin/env python3
"""
Build ecosystem assessment QMD files from YAML templates.

For each YAML file in ecosystem_config/, generates a corresponding QMD file
in ecosystem_assessments/ using the TEMPLATE_ecosystem_assessment.qmd template
and populating Jinja2 variables with YAML data.
"""

import yaml
from pathlib import Path
from jinja2 import Template


def load_yaml(yaml_path):
    """Load YAML configuration file."""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def load_template(template_path):
    """Load QMD template file."""
    with open(template_path, 'r') as f:
        return f.read()


def render_qmd(template_content, data):
    """Render template with data using Jinja2."""
    template = Template(template_content)
    return template.render(params=data)


def main():
    # Setup paths
    config_dir = Path('ecosystem_config')
    template_path = Path('ecosystem_assessments/TEMPLATE_ecosystem_assessment.qmd')
    output_dir = Path('ecosystem_assessments')

    # Load template
    template_content = load_template(template_path)

    # Process each YAML file
    yaml_files = list(config_dir.glob('*.yaml'))
    print(f"Found {len(yaml_files)} YAML configuration files")

    for yaml_file in yaml_files:
        # Skip template files if any
        if 'TEMPLATE' in yaml_file.name:
            continue

        print(f"Processing {yaml_file.name}...")

        # Load YAML data
        data = load_yaml(yaml_file)

        # Use global_classification as the output filename
        output_filename = f"{data.get('global_classification', yaml_file.stem)}.qmd"
        output_path = output_dir / output_filename

        # Render template with data
        rendered_content = render_qmd(template_content, data)

        # Write output file
        with open(output_path, 'w') as f:
            f.write(rendered_content)

        print(f"  Created {output_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
