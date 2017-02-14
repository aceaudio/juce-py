
import os
import sys
import argparse

# required to pull in the juce module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import juce

parser = argparse.ArgumentParser()
parser.add_argument('--path',
                    required=True,
                    help='path to a directory containing a valid JUCE module.')

args = parser.parse_args()
module = juce.Module(args.path)

print('')
print('=' * 80)
print('path:            ' + module.path)
print('id:              ' + module.id)
print('vendor:          ' + module.vendor)
print('version:         ' + module.version)
print('name:            ' + module.name)
print('description:     ' + module.description)
print('dependencies:    ' + ', '.join(module.dependencies))
print('website:         ' + module.website)
print('license:         ' + module.license)
print('searchpaths:     ' + ', '.join(module.searchpaths))
print('OSXFrameworks:   ' + ', '.join(module.OSXFrameworks))
print('iOSFrameworks:   ' + ', '.join(module.iOSFrameworks))
print('linuxLibs:       ' + ', '.join(module.linuxLibs))
print('mingwLibs:       ' + ', '.join(module.mingwLibs))
print('')
