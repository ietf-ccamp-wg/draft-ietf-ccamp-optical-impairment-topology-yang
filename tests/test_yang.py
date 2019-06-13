#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Esther Le Rouzic
# @Date:   2019-06-07
"""
@author: esther.lerouzic
checks that tree created with yang modules are consistant with uploaded files

"""

from os import system, unlink, path, mkdir
from pathlib import Path
import pytest
from filecmp import cmp
import git
from shutil import move, rmtree
from tempfile import mkdtemp

TEST_DIR = Path(__file__).parent.parent

# adding tests to check the roadm restrictions

YANG_FILE = TEST_DIR /'ietf-optical-impairment-topology.yang'
TREE_FILE = TEST_DIR /'ietf-optical-impairment-topology.tree'
EXPECTED_FILE = TEST_DIR /'ietf-optical-impairment-topology-expected.tree'


# Create temporary dir
# temp_dir = mkdtemp()
temp_dir = TEST_DIR /'ietf_library'
try:  
    mkdir(temp_dir)
except OSError:  
    print (f'Creation of the {temp_dir} directory failed.')
print (f'Creation of the {temp_dir} directory')
# Clone into temporary dir
git.Repo.clone_from('https://github.com/YangModels/yang.git', temp_dir, branch='master', depth=1)

def test_compile():
    my_cmd = f'pyang -f tree -p {temp_dir} {YANG_FILE} -o {EXPECTED_FILE}'
    print(temp_dir)
    system(my_cmd)
    with open(EXPECTED_FILE) as expected:
        expected_tree = expected.read()
    # Find and print the diff:
    print(f'expected : \n{expected_tree}')
    if not cmp(TREE_FILE, EXPECTED_FILE):
        raise AssertionError()
    unlink(EXPECTED_FILE)
    assert False
#rmtree(temp_dir)