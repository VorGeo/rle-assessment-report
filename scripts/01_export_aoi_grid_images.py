"""
Generate Earth Engine asset images for ecosystem assessments.
"""

from gee_redlist.ee_rle import export_fractional_coverage_on_aoo_grid, ensure_asset_folder_exists
from google.auth import default
import yaml
import ee


COUNTRY_CONFIG_PATH = 'config/country_config.yaml'

def load_yaml(yaml_path):
    """Load YAML configuration file."""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def initialize_ee():
    """Initialize Earth Engine."""
    credentials, _ = default(scopes=[
        'https://www.googleapis.com/auth/earthengine',
        'https://www.googleapis.com/auth/cloud-platform'
    ])
    ee.Initialize(credentials=credentials, project='goog-rle-assessments')

def process_classified_image(
    gee_project_path,
    classified_image
    ):
    """Process the classified image."""

    for ecosystem in classified_image['classes']:
        # Ensure the ecosystem folder exists
        folder_path = f"{gee_project_path}{ecosystem['code'].replace('.', '_')}"
        was_created = ensure_asset_folder_exists(folder_path)
        if was_created:
            print(f'Created folder: {folder_path}')
        else:
            print(f'Folder already exists: {folder_path}')

        # Create the binary image for this ecosystem
        class_img = ee.Image(
            gee_project_path + classified_image['asset_id']).eq(ecosystem['id']
        ).selfMask()
        asset_id = f"{folder_path}/a00_grid"
        print(f'Exporting {asset_id}')

        # Export (with create_folder=False since we already created it)
        export_fractional_coverage_on_aoo_grid(
            class_img=class_img,
            asset_id=asset_id,
            export_description=f"AOO_grid_image_for_{ecosystem['code']}",
            create_folder=False,
        )

def main():
    """Main function to export AOO grid images."""
    country_config = load_yaml(COUNTRY_CONFIG_PATH)
    country_code = country_config['country_code']
    print(f"Exporting AOO grid images for country: {country_code}")

    print(f"{country_config=}")
 
    initialize_ee()
    process_classified_image(
        gee_project_path=country_config['gee_project_path'],
        classified_image=country_config['classified_image']
    )


if __name__ == "__main__":
    main()
