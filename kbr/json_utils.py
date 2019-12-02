#!/usr/bin/env python3
""" 
 utils for validating json objects conforms to a template 
 
 
 Kim Brugger (05 Apr 2019), contact: kim.brugger@uib.no
"""

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json

import typing



def _dict_validation(json_body:dict, template:dict) -> bool:

    for key in template.keys():
        if key not in json_body:
            raise KeyError
        
        if not isinstance(json_body[key], type(template[key])):
            print("Key value error: Expected {}, got a {}".format( type(template[key]), type(json_body[key])))
            raise AttributeError
        
        if isinstance(json_body[ key ], dict):
            _dict_validation(json_body[ key ], template[ key ])
                
    return True


def _list_validation(json_body:list, template:dict) -> bool:

    for entry in json_body:
        _dict_validation( entry, template)

    return True



@typing.overload
def validate_json(json_body:dict, template:dict) -> bool:
    ...

@typing.overload
def validate_json(json_body:list, template:dict) -> bool:
    ...


def validate_json(json_body, template:dict) -> bool:

    if isinstance(json_body, list):
        return _list_validation( json_body, template)
    elif isinstance(json_body, dict):
        return _dict_validation( json_body, template)
    else:
        raise TypeError



def read(filename:str) -> {}:
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def write (filename:str, data:dict) -> None:
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
