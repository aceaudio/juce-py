
import os
import unittest

import juce

modules_dir = os.path.join(os.path.dirname(__file__), 'resources', 'modules')


class TsetModuleClass(unittest.TestCase):

    def test_ismodule(self):
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_invalid_id')))
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_invalid_vendor')))
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_missing_description')))
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_missing_header')))
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_missing_id')))
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_missing_module')))
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_missing_vendor')))
        self.assertFalse(juce.ismodule(os.path.join(modules_dir, 'test_missing_version')))
        self.assertTrue(juce.ismodule(os.path.join(modules_dir, 'test_valid_module')))

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            juce.Module(os.path.join(modules_dir, 'test_invalid_id'))

    def test_invalid_vendor(self):
        with self.assertRaises(ValueError):
            juce.Module(os.path.join(modules_dir, 'test_invalid_vendor'))

    def test_missing_description(self):
        with self.assertRaises(ValueError):
            juce.Module(os.path.join(modules_dir, 'test_missing_description'))

    def test_missing_header(self):
        with self.assertRaises(IOError):
            juce.Module(os.path.join(modules_dir, 'test_missing_header'))

    def test_missing_id(self):
        with self.assertRaises(ValueError):
            juce.Module(os.path.join(modules_dir, 'test_missing_id'))

    def test_missing_module(self):
        with self.assertRaises(IOError):
            juce.Module(os.path.join(modules_dir, 'test_missing_module'))

    def test_missing_vendor(self):
        with self.assertRaises(ValueError):
            juce.Module(os.path.join(modules_dir, 'test_missing_vendor'))

    def test_missing_version(self):
        with self.assertRaises(ValueError):
            juce.Module(os.path.join(modules_dir, 'test_missing_version'))

    def test_valid_module(self):
        try:
            module = juce.Module(os.path.join(modules_dir, 'test_valid_module'))
        except IOError:
            self.fail('Unexpected IOError while loading a valid module')
        except ValueError:
            self.fail('Unexpected ValueError while loading a valid module')
        except:
            self.fail('Unexpected error while loading a valid module')
        else:
            self.assertTrue(module.ID == 'test_valid_module')
            self.assertTrue(module.vendor == 'vendor')
            self.assertTrue(module.version == '1.0.0')
            self.assertTrue(module.name == 'name')
            self.assertTrue(module.description == 'description')
            try:
                module.version = '1.2.3'
            except:
                self.fail('Unexpected error setting the version number')
            else:
                self.assertTrue(module.version == '1.2.3')
                module.version = '1.0.0'
