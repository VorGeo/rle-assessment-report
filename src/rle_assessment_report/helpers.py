"""Helper functions for RLE assessment scripts."""

import yaml
import ee
from google.auth import default


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