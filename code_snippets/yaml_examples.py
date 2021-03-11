#!/usr/bin/env python3
# coding: utf-8

# $Id: Yaml.py 2777 2020-01-09 14:14:08Z ltaulell $
# SPDX-License-Identifier: CECILL-B

"""
Some Yaml functions, often use in psmn's python scripts

    http://pyyaml.org/wiki/PyYAMLDocumentation

"""

import yaml
import sys


def load_yaml_file(yamlfile):
    """ load data from a yaml file, using safe_load, return a dict{}.

    yamlfile is mandatory. Throw yaml errors, if any.

    import sys
    import yaml
    """
    try:
        with open(yamlfile, 'r') as fichier:
            contenu = yaml.safe_load(fichier)
            return(contenu)
    except IOError:
        print("Unable to open file: {}".format(fichier.name))
        sys.exit(1)
    except yaml.YAMLError as erreur:
        if hasattr(erreur, 'problem_mark'):
            mark = erreur.problem_mark
            # print("YAML error position: (%s:%s) in" % (mark.line + 1, mark.column + 1), fichier.name)
            print('YAML error position: ({}:{}) in {}'.format(mark.line + 1, mark.column + 1, fichier.name))
        sys.exit(1)


def load_dict(yamlfile):
    """ load data from a yaml file, using safe_load, return a dict{}.
    yamlfile is mandatory, no yaml error properly handled

    import sys
    import yaml
    """
    try:
        with open(yamlfile, 'r') as fichier:
            yamlcontenu = yaml.safe_load(fichier)
            return(yamlcontenu)
    except IOError:
        print("Unable to open file: {}".format(fichier.name))
        sys.exit(1)


def save_yaml_file(yamlfile, data):
    """ save data{dict} into yamlfile

    Filename is mandatory. Data must be a dict{}.

    import sys
    import yaml
    """
    try:
        with open(yamlfile, 'wt', encoding='utf-8') as fichier:
            fichier.write("%YAML 1.1\n---\n")
            yaml.safe_dump(data, stream=fichier, encoding='utf-8', canonical=False, default_flow_style=False, default_style='')
    except EnvironmentError as e:
        print("Environment Error: {} {} {}".format(e.strerror, e.errno, e.filename))
        sys.exit(1)
    except yaml.YAMLError as erreur:
        print("YAML error {}, {}".format(erreur, fichier.name))
        sys.exit(1)
