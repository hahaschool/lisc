"""Tests for the lisc.core.modutils."""

from inspect import ismodule

from py.test import raises

from lisc.core.modutils import *

###################################################################################################
###################################################################################################

def test_dependency():

    dep = Dependency('test_module')

    with raises(ImportError):
        dep.method_call

def test_safe_import():

	# Check an import that should work
	imp = safe_import('numpy')
	assert ismodule(imp)

	# Check an import that should fail
	imp = safe_import('bad')
	assert not ismodule(imp)
	assert isinstance(imp, Dependency)
