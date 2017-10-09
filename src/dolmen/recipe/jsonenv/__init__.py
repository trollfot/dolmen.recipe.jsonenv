# -*- coding: utf-8 -*-

import os
import json
import sys
import zc.recipe.egg


_oprp = getattr(os.path, 'realpath', lambda path: path)


def realpath(path):
    return os.path.normcase(os.path.abspath(_oprp(path)))


def extract_config(options):
    conf = {}
    for k, v in options.items():
        if k.startswith('conf-'):
            _, name, key = k.split('-', 3)
            section = conf.setdefault(name, {})
            section[key] = v
    return conf


def extract_paths(eggs):
    requirements, ws = eggs.working_set()
    eggs_paths = [dist.location for dist in ws]
    unique_egg_paths = []  # order preserving unique
    for p in eggs_paths:
        if p not in unique_egg_paths:
            unique_egg_paths.append(p)
    return list(map(realpath, unique_egg_paths))


class JSONDump(object):
    """Dump a useable app config in a JSON format.
    """

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.name = name
        self.buildout = buildout
        self.options = options

    def jsonify(self):
        """Create a json structure containing the needed eggs' paths
        """
        path = self.buildout['buildout']['directory']
        fname = self.options.get('output', 'config.json')
        output = os.path.join(path, fname)
        config = {
            'paths': extract_paths(self.egg),
            'conf': extract_config(self.options),
            }
        with open(output, 'w') as fd:
            json.dump(config, fd, indent=4)
        return output

    def install(self):
        output = self.jsonify()
        return [output]

    update = install
