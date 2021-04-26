#!/usr/bin/env python3
import yaml

st = open('model-catalog/servers/openapi.yaml')
data = yaml.load(st);

if ('components' in data and 'schemas' in data['components']):
    schemas = data['components']['schemas']
    for rname in schemas:
        resource = schemas[rname]
        if ('properties' in resource):
            for prop in resource['properties']:
                attrs = resource['properties'][prop]
                if ('type' in attrs and attrs['type'] == 'array'):
                    if ('anyOf' in attrs['items']):
                        pass
                        # items is an array, if has some ref change it to object.
                    elif ('$ref' in attrs['items']):
                        data['components']['schemas'][rname]['properties'][prop]['items'] = {'type': 'object'}
                    else:
                        if ('type' in attrs['items'] and attrs['items']['type'] == 'string'):
                            pass
                        else:
                            print(rname, prop, attrs['items'])

    with open('./oas-noref.yaml', 'w') as output:
        output.write(yaml.dump(data, default_flow_style=False))
