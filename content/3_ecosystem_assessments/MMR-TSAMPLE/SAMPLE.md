```{code-cell} python
:tags: [hide-cell]

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

## Tropical forest

**Authors:** {eval}`", ".join(authors)`

```{code-cell} python
:tags: [hide-cell]

ecosystem_name_str = Markdown(", ".join([
    f"{ecosystem_name['name']} [{ecosystem_name['reference']}]"
    for ecosystem_name in ecosystem_names_local
]))
```

**{eval}`country_name` ecosystem names:** {eval}`ecosystem_name_str`

**Biome:** Tropical and subtropical forests (T1)

**Functional Group:** T1.1

**Global classification:** MMR-TSAMPLE

**IUCN Status:** Endangered

**Ecosystem Photo**

```{warning}
Unable to find ecosystem photo image named: **ecosystem_assessments/MMR-TSAMPLE/images/MMR-TSAMPLE_photo.png**
```

**Ecosystem Map**

```{warning}
Unable to find ecosystem map image named: **ecosystem_assessments/MMR-TSAMPLE/images/MMR-TSAMPLE_map.png**
```

**Description**

The ecosystem description goes here.

**Distribution**

The ecosystem distribution text goes here.

**Characteristic Native Biota**

The ecosystem's characteristic native biota text goes here.

**Abiotic environment**

The ecosystem's abiotic environment text goes here.

**Key processes and interactions**

The ecosystem's key processes and interactions text goes here.

**Major threats**

The ecosystem's major threats text goes here.

**Ecosystem collapse definition**

The ecosystem's ecosystem collapse definition text goes here.

**Assessment summary**

The ecosystem's assessment summary text goes here.

**Assessment information**

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

**Assessment outcome**

The ecosystem's assessment outcome text goes here.

**Year published**

1999

**Date assessed**

24th January 2000

**Assessment credits**

Assessed by: Jane Smith

Reviewed by: Jose Pérez

Contributions by: Kevin Bacon

**Criterion A**

The ecosystem's criterion A description text goes here.

**Criterion B**

The ecosystem's criterion B description text goes here.

**Criterion C**

The ecosystem's criterion C description text goes here.

**Criterion D**

The ecosystem's criterion D description text goes here.

**Criterion E**

The ecosystem's criterion E description text goes here.
