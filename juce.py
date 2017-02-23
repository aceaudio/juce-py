
import os
import sys
import subprocess

from xml.etree import ElementTree


def ismodule(path):
    """
    Returns:
        bool: ``True`` if *path* is a directory containing a valid JUCE module.
    """
    try:
        Module(path)
    except:
        return False

    return True


class Module(object):
    """
    Encapsulates a JUCE module, making it easy to read values from the module
    header and set the version number.

    Args:
        path (str): The path to a directory containing a JUCE module.
    """
    def __init__(self, path):
        self._path = os.path.abspath(path)
        dirname = os.path.basename(self.path)
        self._header = os.path.join(self.path, dirname + '.h')
        self._begin_declaration_key = 'BEGIN_JUCE_MODULE_DECLARATION'
        self._end_declaration_key = 'END_JUCE_MODULE_DECLARATION'
        self._config_key = 'Config:'
        self._options = {}
        self._declaration = {
            'ID': None,
            'vendor': None,
            'version': None,
            'name': None,
            'description': None,
            'dependencies': '',
            'website': '',
            'license': '',
            'searchpaths': '',
            'OSXFrameworks': '',
            'iOSFrameworks': '',
            'linuxLibs': '',
            'mingwLibs': '',
        }

        didEnterDeclaration = False

        # open the header to read the declaration section
        with open(self._header) as file:
            for line in file:
                line = line.strip()

                # mark the begining of the declaration section
                # and goto the next iteration of the loop
                if line == self._begin_declaration_key:
                    didEnterDeclaration = True
                    continue

                if didEnterDeclaration:
                    # if we find the end of the declaration, stop
                    # reading, and goto the next iteration of the loop
                    if line == self._end_declaration_key:
                        didEnterDeclaration = False
                        continue

                    # inside the declaration section split lines into a key
                    # and value pair splitting at the first occurance of ':'
                    if ':' in line:
                        key, value = line.split(':', 1)

                        # copy the value into the declaration dictionary
                        if key in self._declaration:
                            self._declaration[key] = value.strip()

                # if we find the declaration of an option add
                # a default value to the options dictionary
                elif line.startswith('/**') and self._config_key in line:
                    key = line.split(self._config_key, 1)[1].strip()
                    self._options[key] = None
                    continue

                # if we find a define read its name and value
                elif line.startswith('#define'):
                    define = line.split(None, 2)[1:]

                    # if the define has a value and the name is a key
                    # in the options dictionary, store its value
                    if len(define) == 2 and define[0] in self._options:
                        self._options[define[0]] = define[1]

        self._options = {k: v for k, v in self._options.items() if v in ['0', '1']}

        for key in self._declaration:
            if self._declaration[key] is None:
                raise ValueError('Missing key: \'' + str(key) + '\'')

        if dirname != self.ID:
            raise ValueError('Module ID: \'' + self.ID + '\' does not match module dirname: \'' + dirname + '\'')

        if ' ' in self.vendor:
            raise ValueError('Vendor contains whitespace')

    def __str__(self):
        return self.path

    @property
    def path(self):
        """The full path to the module directory"""
        return self._path

    @property
    def ID(self):
        """A unique ID for the module"""
        return self._declaration['ID']

    @property
    def id(self):
        """A unique ID for the module"""
        return self.ID

    @property
    def vendor(self):
        """A unique ID for the vendor"""
        return self._declaration['vendor']

    @property
    def version(self):
        """The module version number"""
        return self._declaration['version']

    @version.setter
    def version(self, value):
        self._declaration['version'] = value
        self._save()

    @property
    def name(self):
        """A brief description of the module"""
        return self._declaration['name']

    @property
    def description(self):
        """A detailed description of the module"""
        return self._declaration['description']

    @property
    def dependencies(self):
        """An array of module ID's for modules that this module depends on"""
        return self._declaration['dependencies'].replace(',', ' ').split()

    @property
    def website(self):
        """A URL containing useful information about the module"""
        return self._declaration['website']

    @property
    def license(self):
        """A description of the type of software license that applies to this module"""
        return self._declaration['license']

    @property
    def searchpaths(self):
        """
        An array of include paths, relative to the module's parent directory,
        which need to be added to a project's header search path,
        """
        return self._declaration['searchpaths'].split()

    @property
    def OSXFrameworks(self):
        """An array of OSX frameworks that this module depends on"""
        return self._declaration['OSXFrameworks'].replace(',', ' ').split()

    @property
    def osxframeworks(self):
        """An array of OSX frameworks that this module depends on"""
        return self.OSXFrameworks

    @property
    def iOSFrameworks(self):
        """An array of iOS frameworks that this module depends on"""
        return self._declaration['iOSFrameworks'].replace(',', ' ').split()

    @property
    def iosframeworks(self):
        """An array of iOS frameworks that this module depends on"""
        return self.iOSFrameworks

    @property
    def linuxLibs(self):
        """An array of Linux libraries that this module depends on"""
        return self._declaration['linuxLibs'].replace(',', ' ').split()

    @property
    def linuxlibs(self):
        """An array of Linux libraries that this module depends on"""
        return self.linuxLibs

    @property
    def mingwLibs(self):
        """An array of mingw libraries that this module depends on"""
        return self._declaration['mingwLibs'].replace(',', ' ').split()

    @property
    def mingwlibs(self):
        """An array of mingw libraries that this module depends on"""
        return self.mingwLibs

    @property
    def options(self):
        """Returns a dict of config options with default values"""
        return self._options

    def _save(self):
        didEnterDeclaration = False

        # open the header to read the declaration section
        with open(self._header) as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            stripped_line = line.strip()

            # mark the end of the declaration section
            if stripped_line == self._end_declaration_key:
                didEnterDeclaration = False

            # in the declaration section split
            # each line into a key and a value
            if didEnterDeclaration:
                if ':' in stripped_line:
                    key, value = stripped_line.split(':', 1)

                    # replace the value with the corrsponding
                    # one stored in the declaration dict
                    if key in self._declaration:
                        line = line.replace(value.strip(), self._declaration[key])

            # mark the begining of the declaration section
            elif stripped_line == self._begin_declaration_key:
                didEnterDeclaration = True

            new_lines.append(line)

        with open(self._header, 'w') as file:
            file.writelines(new_lines)


class Projucer(object):
    """
    Encapsulates the access of the Projucer application using the command line.

    Args:
        path (str): The path to the Projucer executable binary, or app bundle
            on mac.
    """

    def __init__(self, path):
        if path.endswith('.app'):
            executable = os.path.join(path, 'Contents', 'MacOS', 'Projucer')
        else:
            executable = path

        self._executable = os.path.abspath(executable)

    def __str__(self):
        return self.executable

    @property
    def executable(self):
        """
        The full path to the Projucer executable binary.
        """
        return self._executable

    def resave(self, project_file):
        """
        Resaves all files and resources in a project.

        Args:
            project_file (str): The path to a jucer project file.
        """
        self._call('--resave', project_file)

    def resave_resources(self, project_file):
        """
        Resaves just the binary resources for a project.

        Args:
            project_file (str): The path to a jucer project file.
        """
        self._call('--resave-resources', project_file)

    def set_version(self, version_number, project_file):
        """
        Updates the version number in a project.

        Args:
            project_file (str): The path to a jucer project file.
            version_number (str): The version number to set the project to.
        """
        self._call('--set-version', version_number, project_file)

    def bump_version(self, project_file):
        """
        Updates the minor version number in a project by 1.

        Args:
            project_file (str): The path to a jucer project file.
        """
        self._call('--bump-version', project_file)

    def git_tag_version(self, project_file):
        """
        Invokes 'git tag' to attach the project's version number to the current
        git repository.

        Args:
            project_file (str): The path to a jucer project file.
        """
        self._call('--git-tag-version', project_file)

    def build_module(self, target_dir, module_dir):
        """
        Zips a module into a downloadable file format.

        Args:
            target_dir (str): The path to a directory to store the output file.
            module_dir (str): The path to a directory containing a juce module.
        """
        self._call('--buildmodule', target_dir, module_dir)

    def build_all_modules(self, target_dir, module_dir):
        """
        Zips all modules in a given folder and creates an index for them.

        Args:
            target_dir (str): The path to a directory to store the output file.
            module_dir (str): The path to a directory containing a multiple juce
                modules.
        """
        self._call('--buildallmodules', target_dir, module_dir)

    def trim_whitespace(self, target_dir):
        """
        Scans the given folder for C/C++ source files, and trims any trailing
        whitespace from their lines, as well as normalising their line-endings
        to CR-LF.

        Args:
            target_dir (str): The path to a directory containing C/C++ source
                files.
        """
        self._call('--trim-whitespace', target_dir)

    def remove_tabs(self, target_dir):
        """
        Scans the given folder for C/C++ source files, and replaces any tab
        characters with 4 spaces.

        Args:
            target_dir (str): The path to a directory containing C/C++ source
                files.
        """
        self._call('--remove-tabs', target_dir)

    def tidy_divider_comments(self, target_dir):
        """
        Scans the given folder for C/C++ source files, and normalises any
        juce-style comment division lines.

        (i.e. any lines that look like ``//=====`` or ``//-----`` or ``///////``
        will be replaced)

        Args:
            target_dir (str): The path to a directory containing C/C++ source
                files.
        """
        self._call('--tidy-divider-comments', target_dir)

    def fix_broken_include_paths(self, target_dir):
        """
        Scans the given folder for C/C++ source files (recursively). Where a
        file contains an #include of one of the other filenames, it changes it
        to use the optimum relative path. Helpful for auto-fixing includes when
        re-arranging files and folders in a project.

        Args:
            target_dir (str): The path to a directory containing C/C++ source
                files.
        """
        self._call('--fix-broken-include-paths', target_dir)

    def encode_binary(self, source_file, target_cpp):
        """
        Converts a binary file to a C++ file containing its contents as a block
        of data. Provide a .h file as the target if you want a single output
        file, or a .cpp file if you want a pair of .h/.cpp files.

        Args:
            source_file (str): The path to a binary file.
            target_cpp (str): The path to a .cpp or .h file to store the binary
                data in.
        """
        self._call('--encode-binary', source_file, target_cpp)

    def _call(self, *args):
        sys.stdout.flush()
        sys.stderr.flush()
        subprocess.check_call([self.executable] + list(args))
        sys.stdout.flush()
        sys.stderr.flush()


class Project(object):
    def __init__(self, path, projucer):
        self._path = os.path.abspath(path)

        if isinstance(projucer, Projucer):
            self._projucer = projucer
        else:
            self._projucer = Projucer(projucer)

        self._xml = ElementTree.parse(path).getroot()
        self._xml_restore_point = ElementTree.parse(path)

    @property
    def path(self):
        return self._path

    def __getattr__(self, name):
        try:
            return self._xml.attrib[name]
        except KeyError:
            raise AttributeError('\'Project\' object has no attribute \'' + name + '\'')

    def exporters_of_type(self, exporter_type):
        exporters = list()
        for exporter in self.exporters():
            if exporter.type == exporter_type:
                exporters.append(exporter)
        return exporters

    @property
    def exporters(self):
        return [Exporter(self, exporter) for exporter in self._xml.find('EXPORTFORMATS')]

    @property
    def options(self):
        return self._xml.find('JUCEOPTIONS').attrib


class Exporter(object):
    def __init__(self, project, exporter):
        self._project_dir = os.path.dirname(project.path)
        self._xml = exporter

    @property
    def type(self):
        return self._xml.tag

    def __getattr__(self, name):
        return self._xml.attrib[name]

    def configuration(self, name):
        for config in self.get_configurations():
            if config.name == name:
                return config
        raise ValueError('No configuration with name: \'' + name + '\'')

    @property
    def configurations(self):
        return [Configuration(config) for config in self._xml.find('CONFIGURATIONS')]

    @property
    def modules(self):
        modules = list()
        for module in self._xml.find('MODULEPATHS'):
            module_path = os.path.join(self._project_dir,
                                       module.attrib['path'],
                                       module.attrib['id'])
            modules.append(Module(module_path))
        return modules


class Configuration(object):
    def __init__(self, configuration):
        self._xml = configuration

    def __getattr__(self, name):
        return self._xml.attrib[name]
