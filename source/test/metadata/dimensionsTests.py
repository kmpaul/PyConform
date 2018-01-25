"""
Unit Tests for Dimension Metadata Objects

Copyright 2017-2018, University Corporation for Atmospheric Research
LICENSE: See the LICENSE.rst file for details
"""

import unittest

from pyconform.metadata import Dimension
from pyconform.metadata.datasets import Dataset


class MockNetCDF4Dimension(object):

    def __init__(self, name, size, isunlimited=False):
        self.name = name
        self.size = size
        self._isunlimited = isunlimited

    def __len__(self):
        return self.size

    def isunlimited(self):
        return self._isunlimited


class DimensionTests(unittest.TestCase):

    def setUp(self):
        self.ds = Dataset()

    def test_create(self):
        d = self.ds.new_dimension('x')
        self.assertIsInstance(d, Dimension)

    def test_default_size_is_none(self):
        d = self.ds.new_dimension('x')
        self.assertEqual(d.size, None)

    def test_setting_size_property_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.d.size = 5

    def test_set_size_to_int_in_constructor(self):
        d = self.ds.new_dimension('x', size=4)
        self.assertEqual(d.size, 4)

    def test_set_size_to_non_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.ds.new_dimension('x', size='4')

    def test_set_size_to_non_positive_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.ds.new_dimension('x', size=-2)

    def test_default_is_unlimited_is_false(self):
        d = self.ds.new_dimension('x')
        self.assertEqual(d.is_unlimited, False)

    def test_setting_is_unlimited_property_raises_attribute_error(self):
        d = self.ds.new_dimension('x')
        with self.assertRaises(AttributeError):
            d.is_unlimited = True

    def test_set_is_unlimited_to_bool_in_constructor(self):
        d = self.ds.new_dimension('x', is_unlimited=True)
        self.assertEqual(d.is_unlimited, True)

    def test_set_is_unlimited_to_non_bool_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.ds.new_dimension('x', is_unlimited='false')

    def test_from_netcdf4(self):
        ncdim = MockNetCDF4Dimension('x', 4, isunlimited=True)
        dim = Dimension.from_netcdf4(ncdim, dataset=self.ds)
        self.assertEqual(dim.name, 'x')
        self.assertEqual(dim.size, 4)
        self.assertTrue(dim.is_unlimited)

    def test_equal(self):
        d1 = self.ds.new_dimension('x', size=5, is_unlimited=True)
        d2 = self.ds.new_dimension('y', size=5, is_unlimited=True)
        self.assertEqual(d1, d2)

    def test_not_equal(self):
        d1 = self.ds.new_dimension('x', size=5, is_unlimited=True)
        d2 = self.ds.new_dimension('y', size=2, is_unlimited=True)
        self.assertIsNot(d1, d2)
        self.assertNotEqual(d1, d2)


if __name__ == '__main__':
    unittest.main()
