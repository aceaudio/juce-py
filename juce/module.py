
import os


def ismodule(path):
    try:
        Module(path)
    except:
        return False

    return True


class Module(object):
    def __init__(self, path):
        self._path = path
        self._header = os.path.join(path, os.path.basename(path) + '.h')
        self._begin_declaration_key = 'BEGIN_JUCE_MODULE_DECLARATION'
        self._end_declaration_key = 'END_JUCE_MODULE_DECLARATION'

        self._declaration = {
            'ID:': None,
            'vendor:': None,
            'version:': None,
            'name:': None,
            'description:': None,
            'dependencies:': '',
            'website:': '',
            'license:': '',
            'searchpaths:': '',
            'OSXFrameworks:': '',
            'iOSFrameworks:': '',
            'linuxLibs:': '',
            'mingwLibs:': '',
        }

        didEnterDeclaration = False

        with open(self._header) as file:
            for line in file:
                line = line.strip()

                if line == self._begin_declaration_key:
                    didEnterDeclaration = True
                    continue

                if not didEnterDeclaration:
                    continue

                if line == self._end_declaration_key:
                    break

                for key in self._declaration:
                    if line.startswith(key):
                        self._declaration[key] = line[len(key):].lstrip()
                        break

        for key in self._declaration:
            if self._declaration[key] is None:
                raise ValueError('Compulsory ' + str(key[:-1]) + ' value missing')

        if os.path.basename(path) != self.name:
            raise ValueError('Module ID \'' + self.ID + '\' does not match dirname \'' + os.path.basename(path) + '\'')

        if ' ' in self.vendor:
            raise ValueError('Vendor contains whitespace')

    @property
    def path(self):
        """The full path to the module directory"""
        return self._path

    @property
    def ID(self):
        """A unique ID for the module"""
        return self._declaration['ID:']

    @property
    def id(self):
        """A unique ID for the module"""
        return self.ID

    @property
    def vendor(self):
        """A unique ID for the vendor"""
        return self._declaration['vendor:']

    @property
    def version(self):
        """The module version number"""
        return self._declaration['version:']

    @version.setter
    def version(self, value):
        self._declaration['version:'] = value
        self._save()

    @property
    def name(self):
        """A brief description of the module"""
        return self._declaration['name:']

    @property
    def description(self):
        """A description of the module"""
        return self._declaration['description:']

    @property
    def dependencies(self):
        """An array of module ID's for modules that this module depends on"""
        return self._declaration['dependencies:'].replace(',', ' ').split()

    @property
    def website(self):
        """A URL containing useful information about the module"""
        return self._declaration['website:']

    @property
    def license(self):
        """A description of the type of software license that applies to this module"""
        return self._declaration['license:']

    @property
    def searchpaths(self):
        """
        An array of include paths, relative to the module's parent folder,
        which need to be added to a project's header search path,
        """
        return self._declaration['searchpaths:'].split()

    @property
    def OSXFrameworks(self):
        """An array of OSX frameworks that this module depends on"""
        return self._declaration['OSXFrameworks:'].replace(',', ' ').split()

    @property
    def osxframeworks(self):
        """An array of OSX frameworks that this module depends on"""
        return self.OSXFrameworks

    @property
    def iOSFrameworks(self):
        """An array of iOS frameworks that this module depends on"""
        return self._declaration['iOSFrameworks:'].replace(',', ' ').split()

    @property
    def iosframeworks(self):
        """An array of iOS frameworks that this module depends on"""
        return self.iOSFrameworks

    @property
    def linuxLibs(self):
        """An array of Linux libraries that this module depends on"""
        return self._declaration['linuxLibs:'].replace(',', ' ').split()

    @property
    def linuxlibs(self):
        """An array of Linux libraries that this module depends on"""
        return self.linuxLibs

    @property
    def mingwLibs(self):
        """An array of mingw libraries that this module depends on"""
        return self._declaration['mingwLibs:'].replace(',', ' ').split()

    @property
    def mingwlibs(self):
        """An array of mingw libraries that this module depends on"""
        return self.mingwLibs

    def _save(self):
        didEnterDeclaration = False

        with open(self._header) as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            stripped_line = line.strip()

            if stripped_line == self._end_declaration_key:
                didEnterDeclaration = False

            if didEnterDeclaration:
                for key in self._declaration:
                    if stripped_line.startswith(key):
                        string_to_replace = stripped_line[len(key):].lstrip()
                        if string_to_replace:
                            line = line.replace(string_to_replace, self._declaration[key])
            elif stripped_line == self._begin_declaration_key:
                didEnterDeclaration = True

            new_lines.append(line)

            with open(self._header, 'w') as file:
                file.writelines(new_lines)
