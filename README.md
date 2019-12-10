# mint_setup_runner

## Installation

```
pip install -r requirements.txt
```

## CLI

`mint_setup_runner` downloads the setup and write them as YAML files.

To obtain the `setups` (`ConfigurationSetup`) of a `SoftwareConfiguration,` we must pass the id of the resource.

For example, the `SoftwareConfiguration` `https://w3id.org/okn/i/mint/topoflow_cfg_simple_Awash` has the id `topoflow_cfg_simple_Awash`.

The option `-o` defines the output directory.

```python
python generate_setup.py -o setups topoflow_cfg_simple
```

`ConfigurationSetup` and `SoftwareConfiguration` are defined at the [The Software Description Ontology](https://knowledgecaptureanddiscovery.github.io/SoftwareDescriptionOntology/release/1.3.0/index-en.html#ConfigurationSetup)
~
