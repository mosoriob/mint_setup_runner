#!/usr/bin/env python3

from pathlib import Path
from queries.mcat import ModelCatalog
import yaml
import click

@click.group()
def cli():
    pass

@click.command()
@click.option(
    "--setup",
    "-s",
    type=str,
)
def runsetup(setup):
    modelcatalog = ModelCatalog()
    modelcatalog.setUp()
    resource = modelcatalog.test_get_one_setup_custom(setup)
    setup_file_name = "{}.yaml".format(setup)
    with open(setup_file_name, 'w') as setup_file:
        yaml.dump(resource, setup_file, allow_unicode=True)

if __name__ == "__main__":
    runsetup()
