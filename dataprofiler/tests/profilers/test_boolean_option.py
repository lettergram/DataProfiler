import os
import unittest
from unittest import mock

import pandas as pd

from dataprofiler import Data, ProfilerOptions, Profiler
from dataprofiler.profilers.profiler_options import BooleanOption
from dataprofiler.tests.profilers.test_base_option import TestBaseOption

class TestBooleanOption(TestBaseOption):
    
    @classmethod
    def setUpClass(cls):
        cls.option_class = BooleanOption    
        
    def test_init(self, *mocks):
        option = self.get_options()
        self.assertDictEqual({"is_enabled": True}, option.properties)
        option = self.get_options(is_enabled=False)
        self.assertDictEqual({"is_enabled": False}, option.properties)
    
    def test_set_helper(self, *mocks):
        super().test_set_helper(*mocks)
        
        # Enable and Disable Option
        for is_enabled in [True, False]:
            option = self.get_options(is_enabled=not is_enabled)
            option._set_helper({'is_enabled':is_enabled}, '') 
            self.assertEqual(is_enabled, option.properties['is_enabled'])        

        # Treat is_enabled as a BooleanOption
        expected_error = "type object 'is_enabled' has no attribute 'is_enabled'"
        with self.assertRaisesRegex(AttributeError, expected_error):
            option._set_helper({'is_enabled.is_enabled': True}, '')    
        
    def test_set(self, *mocks):
        super().test_set(*mocks)

        # Enable and Disable Options       
        for is_enabled in [True, False]:
            option = self.get_options(is_enabled=not is_enabled)
            option.set({'is_enabled':is_enabled}) 
            self.assertEqual(is_enabled, option.properties['is_enabled'])        
    
        # Treat is_enabled as a BooleanOption
        expected_error = "type object 'is_enabled' has no attribute 'error'"
        with self.assertRaisesRegex(AttributeError, expected_error):
            option.set({'is_enabled.error': True})    

    def test_validate_helper(self, *mocks):
        option = self.get_options(is_enabled=True)
        optpth = self.get_options_path()

        # Default Configuration Is Valid
        self.assertEqual([], option._validate_helper())
        
        # Variable Path Is Not A String
        expected_error = "The variable path must be a string."
        with self.assertRaisesRegex(ValueError, expected_error):
            option._validate_helper(1)
        
        # Option is_enabled is not a boolean
        option = self.get_options(is_enabled="Hello World")
        expected_error = "{}.is_enabled must be a Boolean.".format(optpth)
        self.assertEqual([expected_error], option._validate_helper())
    
    def test_validate(self, *mocks):
        option = self.get_options(is_enabled=True)
        optpth = self.get_options_path()
    
        # Default Configuration Is Valid
        self.assertEqual(None, option.validate())
        
        # Option is_enabled is not a boolean
        option = self.get_options(is_enabled="Hello World")
        expected_error = "{}.is_enabled must be a Boolean.".format(optpth)
        with self.assertRaisesRegex(ValueError, expected_error):
            option.validate(raise_error=True)
        self.assertEqual([expected_error], option.validate(raise_error=False))
