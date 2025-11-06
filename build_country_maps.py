"""
Generate country map images for ecosystem assessments.

This script checks if country_map.png exists in the images folder.
If not, it uses gee-redlist-python to create a PNG map and save it.
"""

import os
from pathlib import Path

# Configuration
IMAGES_DIR = Path("images")
MAP_FILENAME = "country_map.png"
map_path = IMAGES_DIR / MAP_FILENAME


def check_map_exists() -> bool:
    """Check if the country map already exists."""
    return map_path.exists()


def create_country_map():
    """Create a country map using gee-redlist-python."""
    try:
        # Import from gee-redlist-python
        # Note: This package may need to be installed via pip
        from gee_redlist import create_country_map

        print(f"Creating country map: {map_path}")

        # TODO: Update with actual country code and parameters
        country_name = "Myanmar"

        # Create the map
        # Note: Adjust parameters based on gee-redlist-python API
        map_image = create_country_map(
            country_name=country_name,
            output_path=map_path,
            # Add additional parameters as needed
        )
        print(f'{map_image=}')

        print(f"✓ Country map saved to: {map_path}")
        return map_path

    except ImportError:
        print("Error: gee-redlist-python package not found.")
        print("Install with: pip install git+https://github.com/VorGeo/gee-redlist-python")
        raise
    except Exception as e:
        print(f"Error creating country map: {e}")
        raise


def main():
    """Main function to check and create country map if needed."""
    if check_map_exists():
        print(f"✓ Country map already exists: {map_path}")
    else:
        print(f"Country map not found: {map_path}")
        create_country_map()


if __name__ == "__main__":
    main()
