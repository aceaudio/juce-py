
import os
import unittest

from juce.module import ismodule, Module

modules_dir = os.path.join(os.path.dirname(__file__), 'resources', 'modules')


class TsetModuleClass(unittest.TestCase):

    def test_ismodule(self):
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_invalid_id')))
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_invalid_vendor')))
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_missing_description')))
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_missing_header')))
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_missing_id')))
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_missing_module')))
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_missing_vendor')))
        self.assertFalse(ismodule(os.path.join(modules_dir, 'test_missing_version')))
        self.assertTrue(ismodule(os.path.join(modules_dir, 'test_valid_module')))

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            Module(os.path.join(modules_dir, 'test_invalid_id'))

    def test_invalid_vendor(self):
        with self.assertRaises(ValueError):
            Module(os.path.join(modules_dir, 'test_invalid_vendor'))

    def test_missing_description(self):
        with self.assertRaises(ValueError):
            Module(os.path.join(modules_dir, 'test_missing_description'))

    def test_missing_header(self):
        with self.assertRaises(IOError):
            Module(os.path.join(modules_dir, 'test_missing_header'))

    def test_missing_id(self):
        with self.assertRaises(ValueError):
            Module(os.path.join(modules_dir, 'test_missing_id'))

    def test_missing_module(self):
        with self.assertRaises(IOError):
            Module(os.path.join(modules_dir, 'test_missing_module'))

    def test_missing_vendor(self):
        with self.assertRaises(ValueError):
            Module(os.path.join(modules_dir, 'test_missing_vendor'))

    def test_missing_version(self):
        with self.assertRaises(ValueError):
            Module(os.path.join(modules_dir, 'test_missing_version'))

    def test_valid_module(self):
        try:
            module = Module(os.path.join(modules_dir, 'test_valid_module'))
        except IOError:
            self.fail('Unexpected IOError')
        except ValueError:
            self.fail('Unexpected ValueError')
        else:
            self.assertTrue(module.ID == 'test_valid_module')
            self.assertTrue(module.vendor == 'vendor')
            self.assertTrue(module.version == '1.0.0')
            self.assertTrue(module.name == 'name')
            self.assertTrue(module.description == 'description')
