#!/usr/bin/env python3

from __future__ import print_function
import modelcatalog
from modelcatalog.rest import ApiException
import json
import ast


from pathlib import Path
from queries.mcat import ModelCatalog
import yaml
import click



@click.group()
def cli():
    pass

@click.command()
@click.argument(
    "softwareconfig_id",
    type=str,
)
@click.option(
    "--output",
    "-o",    
    type=click.Path(file_okay=False, dir_okay=True, writable=True, exists=False),
    default='.'
)
def runsetup(softwareconfig_id, output):
    # create an instance of the API class
    queryManager = ModelCatalog()
    queryManager.setUp()
    api_instance = modelcatalog.SoftwareConfigurationApi()
    username = 'mint@isi.edu' # str | Username to query (optional)
    softwareconfig_dir = '{}/{}'.format(output, softwareconfig_id)
    p = Path(softwareconfig_dir)
    p.mkdir(parents=True, exist_ok=True)


    api_response = api_instance.softwareconfigurations_id_get(softwareconfig_id , username=username)
    for setup in api_response.has_setup:
        setup_name = setup.id.split("/")[-1]
        print("found {}".format(setup_name))
        resource = queryManager.test_get_one_setup_custom(setup_name)
        setup_file_name = "{}.yaml".format(setup_name)
        setup_file_path = Path(p/setup_file_name)
        with open(setup_file_path, 'w') as setup_file:
            yaml.dump(resource, setup_file, allow_unicode=True)

if __name__ == "__main__":
    runsetup()
