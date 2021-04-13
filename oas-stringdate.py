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
                if (prop == 'datePublished' or prop == 'dateCreated'):
                    data['components']['schemas'][rname]['properties'][prop]['items'] = {'type': 'string'}
                    #resource[prop] = {'type': 'string'}
                    print('Changed type of ' + prop + ' from ' + rname)

    with open('./openapi-string-dates.yaml', 'w') as output:
        output.write(yaml.dump(data, default_flow_style=False))
