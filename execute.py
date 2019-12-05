#!/usr/bin/env python3

from pathlib import Path
from queries.mcat import ModelCatalog
from zipfile import ZipFile
import tempfile
import requests
import os
import click



ignore_dirs = ["__MACOSX"]

def download_extract_zip(url, _dir):
    temp = tempfile.NamedTemporaryFile(prefix="component_")
    content = download_file(url)
    temp.write(content)
    with ZipFile(temp.name, 'r') as zip:
        zip.extractall(_dir)
    directories = os.listdir(_dir)
    if isinstance(directories, list):
        try:
            for ignore_dir in ignore_dirs:
                directories.remove(ignore_dir)
        except:
            pass

    if len(directories) == 1:
        return os.path.join(_dir, directories[0])
    else:
        raise ValueError("The zipfile must has one directory.")

def download_file(url):
    r = requests.get(url, allow_redirects=True)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError(r)
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException(r)
    return r.content

def download_data_file(url, _dir):
    print("downloading {}".format(url))
    filename = url.split('/')[-1]
    filepath = os.path.join(_dir, filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    return filepath, filename





def build_input(inputs, _dir):
    line =  ""
    files_inputs = []
    for _input in inputs:
        if not "hasFixedResource" in _input:
            print("fail:")
            exit(1)
        url = _input["hasFixedResource"][0]["value"][0]
        file_path, file_name = download_data_file(url, _dir)
        position = _input["position"][0]
        line += " -i{} {}".format(position, file_name)
    return line


def build_output(outputs):
    line =  ""
    for _output in outputs:
        if not "label" in _output:
            print("fail:")
            exit(1)
        label = _output["label"][0]
        extension = _output["hasFormat"][0]
        position = _output["position"][0]
        line += " -o{} {}.{}".format(position, label, extension)
    return line

def build_parameter(parameters):
    line =  ""
    for _parameter in parameters:
        if not "label" in _parameter:
            print("fail:")
            exit(1)
        value = _parameter["hasDefaultValue"][0]
        position = _parameter["position"][0]
        line += " -o{} {}.{}".format(position, value)
    return line

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
    inputs = resource[0]["hasInput"]
    parameters = resource[0]["hasParameter"] if "hasParameter" in resource[0] else None
    outputs = resource[0]["hasOutput"]
    component_url = resource[0]["hasComponentLocation"][0]
    has_software_image = resource[0]["hasSoftwareImage"][0]['label'][0]

    line = "singularity exec docker://{} ./run ".format(has_software_image)
    _dir = Path("executions/")
    _dir.mkdir(parents=True, exist_ok=True)
    component_dir = download_extract_zip(component_url, _dir)
    path = Path(component_dir)
    src_path = path / "src"

    if inputs:
        l = build_input(inputs, src_path)
        line += " {}".format(l)
    if outputs:
        l = build_output(outputs)
        line += " {}".format(l)
    if parameters is not None:
        build_parameter(parameters)
        line += " {}".format(l)
    print("cd {} ".format(src_path))
    print(line)

if __name__ == "__main__":
    runsetup()