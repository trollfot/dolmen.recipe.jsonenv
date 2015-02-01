# -*- coding: utf-8 -*-

import os
import json
import sys
import zc.recipe.egg


_oprp = getattr(os.path, 'realpath', lambda path: path)
def realpath(path):
    return os.path.normcase(os.path.abspath(_oprp(path)))


class JSONDump(object):
    """Dump a useable app config in a JSON format.
    """

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.name = name
        self.buildout = buildout
        self.options = {k[4:]:v for k,v in options.items()
                        if k.startswith('app-')}

    def get_paths(self):
        """Create a json structure containing the needed eggs' paths
        """
        path = self.buildout['buildout']['directory']
        output = os.path.join(path, 'config.json')

        conf = ""
        requirements, ws = self.egg.working_set()
        eggs_paths = [dist.location for dist in ws]
        # order preserving unique
        unique_egg_paths = []
        for p in eggs_paths:
            if p not in unique_egg_paths:
                unique_egg_paths.append(p)

        all_paths = map(realpath, unique_egg_paths)
        config = {
            'paths': all_paths,
            }
        config.update(self.options)

        with open(output, 'w') as fd:
            json.dump(config, fd, indent=4)
        return output

    def install(self):
        output = self.get_paths()
        return [output]

    update = install
