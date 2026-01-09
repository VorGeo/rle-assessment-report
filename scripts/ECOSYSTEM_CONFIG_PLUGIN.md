# Ecosystem Config MyST Plugin

A MyST-MD plugin for preprocessing and accessing ecosystem YAML configuration files within your documentation.

## Features

- **Transform**: Automatically loads ecosystem configuration into page frontmatter
- **Directive**: Display ecosystem configuration data in various formats
- **Role**: Inline access to specific configuration fields

## Installation

1. The plugin is located at `scripts/ecosystem_config_plugin.py`
2. Add it to your `myst.yml`:

```yaml
project:
  plugins:
    - scripts/ecosystem_config_plugin.py
```

## Usage

### 1. Transform (Automatic Data Injection)

Add an `ecosystem_id` to your document's frontmatter to automatically load the configuration:

```markdown
---
title: My Ecosystem Assessment
ecosystem_id: MMR-T1.1.1
---

# Assessment Content

The ecosystem data is now available in frontmatter under the `ecosystem` key.
```

### 2. Directive (Display Configuration)

Use the `ecosystem-config` directive to display configuration data:

#### Display entire config as YAML

```markdown
:::{ecosystem-config} MMR-T1.1.1
:format: yaml
:::
```

#### Display specific field

```markdown
:::{ecosystem-config} MMR-T1.1.1
:field: ecosystem_names_local
:::
```

#### Display as JSON

```markdown
:::{ecosystem-config} MMR-T1.1.1
:field: criteria_status
:format: json
:::
```

### 3. Role (Inline Field Access)

Access specific fields inline using the `eco` role:

```markdown
The ecosystem name is {eco}`MMR-T1.1.1:ecosystem_name`.

The country is {eco}`MMR-T1.1.1:country_name`.

Local names: {eco}`MMR-T1.1.1:ecosystem_names_local`
```

#### Nested field access

Use dot notation for nested fields:

```markdown
AOO status: {eco}`MMR-T1.1.1:criteria_status.B.B1`

Asset ID: {eco}`MMR-T1.1.1:ecosystem_image.asset_id`
```

## Configuration File Structure

The plugin expects YAML files in `config/ecosystem_config/` with the following naming pattern:

```
config/ecosystem_config/{ecosystem_id}.yaml
```

For example:
- `config/ecosystem_config/MMR-T1.1.1.yaml`
- `config/ecosystem_config/MMR-T1.1.3.yaml`

## Special Field Formatting

The `ecosystem_names_local` field is automatically formatted with citations:

```yaml
ecosystem_names_local:
  - name: Tropical rainforest
    reference: "@kress2003checklist"
  - name: Lowland evergreen rainforest
    reference: "@connette2016mapping"
```

Output: `Tropical rainforest [@kress2003checklist], Lowland evergreen rainforest [@connette2016mapping]`

## Error Handling

If the plugin encounters an error:
- **Directive**: Displays a danger admonition with the error message
- **Role**: Shows `[Error: message]` inline
- **Transform**: Logs a warning to stderr but doesn't fail the build

## Examples

### Example 1: Using Transform in Frontmatter

```markdown
---
title: Tanintharyi Island Rainforest Assessment
ecosystem_id: MMR-T1.1.1
---

# {frontmatter.ecosystem.ecosystem_name}

**Country:** {frontmatter.ecosystem.country_name}

**IUCN Status:** {frontmatter.ecosystem.iucn_status}
```

### Example 2: Displaying Criteria Status

```markdown
## Assessment Criteria

:::{ecosystem-config} MMR-T1.1.1
:field: criteria_status
:format: yaml
:::
```

### Example 3: Inline Citations

```markdown
This ecosystem is also known as {eco}`MMR-T1.1.1:ecosystem_names_local` in the literature.
```

## Development

### Testing the Plugin

Test the plugin directly from command line:

```bash
# Print plugin spec
./scripts/ecosystem_config_plugin.py

# Test directive
echo '{"arg": "MMR-T1.1.1", "options": {"field": "ecosystem_name"}}' | \
  ./scripts/ecosystem_config_plugin.py --directive

# Test role
echo '{"value": "MMR-T1.1.1:country_name"}' | \
  ./scripts/ecosystem_config_plugin.py --role

# Test transform
echo '{"frontmatter": {"ecosystem_id": "MMR-T1.1.1"}}' | \
  ./scripts/ecosystem_config_plugin.py --transform
```

### Modifying the Plugin

After making changes to the plugin source code, restart the MyST development server to see updates:

```bash
quarto preview  # or myst start
```

## Troubleshooting

**Issue**: Plugin not found

- Ensure the script is executable: `chmod +x scripts/ecosystem_config_plugin.py`
- Check the path in `myst.yml` is correct

**Issue**: Config file not found

- Verify the YAML file exists at `config/ecosystem_config/{ecosystem_id}.yaml`
- Check that the ecosystem ID in your directive/role matches the filename

**Issue**: Invalid YAML

- Validate your YAML syntax using a YAML linter
- Ensure all required fields are present in the config file
