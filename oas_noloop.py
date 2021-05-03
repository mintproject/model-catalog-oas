#!/usr/bin/env python3
"""Script to remove circular references

Example:

$ python3 oas_noloop.py input.yaml output.yaml
"""

import argparse
from pathlib import Path
import logging
import yaml

def create_parser():
    """Create the argument parse

    Returns:
        [Parser]: Returns a argument parser
    """
    temporal_parser = argparse.ArgumentParser()
    temporal_parser.add_argument('input', type=Path)
    temporal_parser.add_argument('output', help='Output file', type=Path)
    return temporal_parser


def remove_circular_refernces(spec_input: Path, spec_output: Path):
    """Remove the circular references from OpenAPI spec and write a new one

    Args:
        spec_input (Path): the input spec
        spec_output (Path): the output spec
    """
    if not spec_input.exists():
        logging.error("The input file does not exists")
        exit(1)
    if spec_output.exists():
        logging.error("The output file exists")
        exit(1)

    with open(spec_input) as spec_temp:
        data = yaml.load(spec_temp)
        if ('components' in data and 'schemas' in data['components']):
            schemas = data['components']['schemas']
            for rname in schemas:
                resource = schemas[rname]
                if 'properties' in resource:
                    for prop in resource['properties']:
                        attrs = resource['properties'][prop]
                        if 'type' in attrs and attrs['type'] == 'array':
                            if 'anyOf' in attrs['items']:
                                pass
                                # items is an array, if has some ref change it to object.
                            elif '$ref' in attrs['items']:
                                data['components']['schemas'][rname]['properties'][prop]['items'] =\
                                    {'type': 'object'}
                            else:
                                if 'type' in attrs['items'] and attrs['items']['type'] == 'string':
                                    pass
                                else:
                                    print(rname, prop, attrs['items'])

        with open(spec_output, 'w') as output:
            output.write(yaml.dump(data, default_flow_style=False))

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    remove_circular_refernces(args.input, args.output)
