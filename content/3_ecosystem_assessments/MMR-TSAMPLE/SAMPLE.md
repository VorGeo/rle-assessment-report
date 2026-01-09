---
kernelspec:
  name: python3
  display_name: Python 3
  language: python
---

```{code-cell} python
import gee_redlist
print(f'{gee_redlist.__version__ = }')
```

```{code-cell} python
from IPython.display import Markdown, display

country_name = 'Myanmar'
ecosystem_name = 'Tropical forest'
ecosystem_names_local = [{'name': 'Ecosystem Name 1', 'reference': '@bibtexReference1'}, {'name': 'Ecosystem Name 2', 'reference': '@bibtexReference2'}]
authors = ['J. Smith', 'J. Pérez']
biome = 'Tropical and subtropical forests (T1)'
functional_group = 'T1.1'
global_classification = 'MMR-TSAMPLE'
ecosystem_photo = 'images/MMR-TSAMPLE_photo.png'
ecosystem_map = 'images/MMR-TSAMPLE_map.png'
ecosystem_image = {
    'asset_id': 'projects/goog-rle-assessments/assets/mm_ecosys_v7b',
    'pixel_value': '53'
}
iucn_status = 'Endangered'
```

<!-- Title -->
## Tropical forest

<!-- Authors -->
{span .parameter}`Authors:`&nbsp;
J. Smith, J. Pérez

<!-- Local ecosystem names -->
{span .parameter}``{eco}`MMR-TSAMPLE:country_name` ecosystem names:``&nbsp;Ecosystem Name 1 [@bibtexReference1], Ecosystem Name 2 [@bibtexReference2]

<!-- Biome -->
{span .parameter}`Biome:`&nbsp;
Tropical and subtropical forests (T1)

<!-- Functional Group -->
{span .parameter}`Functional Group:`&nbsp;
T1.1

<!-- Global classification -->
{span .parameter}`Global classification:`&nbsp;
MMR-TSAMPLE

<!-- IUCN Status -->
{span .parameter}`IUCN Status:`&nbsp;
Endangered

<!-- Ecosystem Photo -->
{span .parameter}`Ecosystem Photo:`&nbsp;  
::: {important} Unable to find ecosystem photo image
Unable to find ecosystem photo image named:

**content/3_ecosystem_assessments/MMR-TSAMPLE/images/MMR-TSAMPLE_photo.png**
:::   

<!-- Ecosystem Map -->
{span .parameter}`Ecosystem Map:`&nbsp;  
::: {important} Unable to find ecosystem map image
Unable to find ecosystem photo image named:

**content/3_ecosystem_assessments/MMR-TSAMPLE/images/MMR-TSAMPLE_map.png**
:::     

<!-- Description -->
{span .parameter}`Description:`&nbsp;
The ecosystem description goes here.


<!-- Distribution -->
{span .parameter}`Distribution:`&nbsp;
The ecosystem distribution text goes here.


<!-- Characteristic Native Biota -->
{span .parameter}`Characteristic Native Biota:`&nbsp;
The ecosystem's characteristic native biota text goes here.


<!-- Abiotic environment -->
{span .parameter}`Abiotic environment:`&nbsp;
The ecosystem's abiotic environment text goes here.


<!-- Key processes and interactions -->
{span .parameter}`Key processes and interactions:`&nbsp;
The ecosystem's key processes and interactions text goes here.


<!-- Major threats -->
{span .parameter}`Major threats:`&nbsp;
The ecosystem's major threats text goes here.


<!-- Ecosystem collapse definition -->
{span .parameter}`Ecosystem collapse definition:`&nbsp;
The ecosystem's ecosystem collapse definition text goes here.


<!-- Assessment summary -->
{span .parameter}`Assessment summary:`&nbsp;
**The ecosystem's assessment summary text goes here.
**

<!-- Assessment information -->
{span .parameter}`Assessment information:`&nbsp;
<table class="criteria-table">
  <thead>
    <tr>
      <th colspan="2">Criteria</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4">Criterion A</td>
      <td>A1</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>A2a</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>A2b</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>A3</td>
      <td>NE</td>
    </tr>
    <tr>
      <td rowspan="4">Criterion B</td>
      <td>B1</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>B2</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>subcriteria</td>
      <td>['subcriteria1', 'subcriteria2', '...']</td>
    </tr>
    <tr>
      <td>B3</td>
      <td>NE</td>
    </tr>
    <tr>
      <td rowspan="4">Criterion C</td>
      <td>C1</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>C2a</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>C2b</td>
      <td>NE</td>
    </tr>
    <tr>
      <td>C3</td>
      <td>NE</td>
    </tr>
    <tr>
      <td rowspan="4">Criterion D</td>
      <td>D1</td>
      <td>NE</td>
    </tr>
    <tr>
        <td>D2a</td>
        <td>NE</td>
      </tr>
      <tr>
        <td>D2b</td>
        <td>NE</td>
      </tr>
      <tr>
        <td>D3</td>
        <td>NE</td>
      </tr>
      <tr>
        <td>Criterion E</td>
        <td>E</td>
        <td>NE</td>
      </tr>
    </tbody>
  </table>

<!-- Assessment outcome -->
{span .parameter}`Assessment outcome:`&nbsp;
**The ecosystem's assessment outcome text goes here.
**

<!-- Year published -->
{span .parameter}`Year published:`&nbsp;
1999


<!-- Date assessed -->
{span .parameter}`Date assessed:`&nbsp;
24th January 2000

<!-- Assessment credits -->
{span .parameter}`Assessment credits:`&nbsp;

Assessed by: Jane Smith

Reviewed by: Jose Pérez

Contributions by: Kevin Bacon

<!-- Criterion A -->
{span .parameter}`Criterion A:`&nbsp;
The ecosystem's criterion A description text goes here.


<!-- Criterion B -->
{span .parameter}`Criterion B:`&nbsp;
{'text': "The ecosystem's criterion B description text goes here."}

{span .parameter}`TEST:`&nbsp;
```{code-cell} python
import ee
from gee_redlist.ee_rle import make_eoo, area_km2
from google.auth import default

# Use Application Default Credentials (ADC) from GOOGLE_APPLICATION_CREDENTIALS
# This works both locally (after gcloud auth) and in CI/CD (with Workload Identity)
credentials, _ = default(scopes=[
    'https://www.googleapis.com/auth/earthengine',
    'https://www.googleapis.com/auth/cloud-platform'
])
ee.Initialize(credentials=credentials, project='goog-rle-assessments')

asset_id = ecosystem_image['asset_id']
pixel_value = int(ecosystem_image['pixel_value'])

ee_image = (
    ee.Image(ecosystem_image['asset_id'])
      .eq(pixel_value)
      .selfMask()
)
print(f'ee_image: {ee_image.getInfo()}')

eoo_polygon = make_eoo(ee_image)
print(f'EOO area: {area_km2(eoo_polygon).getInfo()} km²')
```

<!-- Criterion C -->
{span .parameter}`Criterion C:`&nbsp;
The ecosystem's criterion C description text goes here.


<!-- Criterion D -->
{span .parameter}`Criterion D:`&nbsp;
The ecosystem's criterion D description text goes here.


<!-- Criterion E -->
{span .parameter}`Criterion E:`&nbsp;
The ecosystem's criterion E description text goes here.
