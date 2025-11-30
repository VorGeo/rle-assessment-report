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
import matplotlib as mpl
import os
import ee
from google.auth import default

import gee_redlist
from gee_redlist import create_country_map

print(f'{gee_redlist.__version__=}')

def path_exists(*paths):
    base_dir = os.getcwd()
    return os.path.exists(os.path.join(base_dir, *paths))

def load_yaml(yaml_path):
    """Load YAML configuration file."""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def load_template(template_path):
    """Load QMD template file."""
    with open(template_path, 'r') as f:
        return f.read()


def render_qmd(
    template_content,
    ecosystem_data,
    country_data,
):
    """Render template with data using Jinja2."""
    template = Template(template_content)
    return template.render(
        params=ecosystem_data | country_data,
        path_exists=path_exists,
        base_dir=os.getcwd()
    )

def create_ecosystem_map(country_code, ecosystem_data, output_path):
    """Create an ecosystem map using the ecosystem image asset ID and pixel value."""
    # print(f"DEBUG: {data=}")

    # Use Application Default Credentials (ADC) from GOOGLE_APPLICATION_CREDENTIALS
    # This works both locally (after gcloud auth) and in CI/CD (with Workload Identity)
    credentials, _ = default(scopes=[
        'https://www.googleapis.com/auth/earthengine',
        'https://www.googleapis.com/auth/cloud-platform'
    ])
    ee.Initialize(credentials=credentials, project='goog-rle-assessments')

    ee_image = (
        ee.Image(ecosystem_data['ecosystem_image']['asset_id'])
          .eq(ecosystem_data['ecosystem_image']['pixel_value'])
          .selfMask()
    )

    create_country_map(
        country_code=country_code,
        output_path=output_path,
        ee_image=ee_image,
        clip_ee_image=True,
        show_border=True,
        geometry_kwargs={
            'linewidth': 0.5,
            'edgecolor': 'grey',
        },
        image_cmap=mpl.colors.ListedColormap(['red']),
    )

def main():
    # Setup paths
    ecosystem_config_dir = Path('config/ecosystem_config')
    template_path = Path('content_templates/TEMPLATE_ecosystem_assessment.jinja')
    output_dir = Path('ecosystem_assessments')
    output_images_dir = Path('images')

    # Load country-level data
    country_config_path = Path('config/country_config.yaml')
    country_data = load_yaml(country_config_path)

    # Load ecosystem assessment template
    template_content = load_template(template_path)

    # Process each YAML file
    yaml_files = list(ecosystem_config_dir.glob('*.yaml'))
    print(f"Found {len(yaml_files)} YAML configuration files")

    for yaml_file in yaml_files:
        print(f"Processing {yaml_file.name}...")

        # Load YAML data for the current ecosystem
        ecosystem_data = load_yaml(yaml_file)

        output_folder = Path(output_dir, ecosystem_data['global_classification'])
        # Create parent directory if it doesn't exist
        output_folder.mkdir(parents=True, exist_ok=True)

        map_path = output_folder / f"{yaml_file.stem}_map.png"
        if not map_path.exists():
            print(f"Creating ecosystem map: {map_path}")
            try:
                create_ecosystem_map(
                    country_code=country_data['country_code'],
                    ecosystem_data=ecosystem_data,
                    output_path=map_path
                )
            except Exception as e:
                print(f"Warning: Failed to create ecosystem map: {e}")
                print("Continuing with template rendering...")
        else:
            print(f"Ecosystem map already exists: {map_path}")

        print("Rendering template...")
        rendered_content = render_qmd(
            template_content=template_content,
            ecosystem_data=ecosystem_data,
            country_data=country_data,
        )

        # Write output file
        print("Writing output file...")
        file_path = Path(
            output_folder,
            f"{yaml_file.stem}.qmd"
        )
        with open(file_path, 'w') as f:
            f.write(rendered_content)

        print(f"  Created {file_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
