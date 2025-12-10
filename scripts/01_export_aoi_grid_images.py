"""
Generate Earth Engine asset images for ecosystem assessments.
"""

from gee_redlist.ee_rle import export_fractional_coverage_on_aoo_grid
from gee_redlist.ee_rle import create_asset_folder
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
        create_asset_folder(folder_path)

        # Create the binary image for this ecosystem
        class_img = ee.Image(
            gee_project_path + classified_image['asset_id']).eq(ecosystem['id']
        ).selfMask()
        asset_id = f"{folder_path}/a00_grid"
        print(f'Exporting {asset_id}')

        # Check if the asset already exists before exporting
        try:
            ee.data.getAsset(asset_id)
            print(f"Asset {asset_id} already exists. Skipping export.")
        except ee.EEException:
            export_fractional_coverage_on_aoo_grid(
                class_img=class_img,
                asset_id=asset_id,
                export_description=f"AOO_grid_image_for_{ecosystem['code']}",
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
