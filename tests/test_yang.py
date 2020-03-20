#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Esther Le Rouzic
# @Date:   2019-06-07
"""
@author: esther.lerouzic
checks that tree created with yang modules are consistant with uploaded files

"""

from os import unlink
from pathlib import Path
import subprocess
import wget
import pytest

TEST_DIR = Path(__file__).parent.parent

YANG_FILE = TEST_DIR /'ietf-optical-impairment-topology.yang'
TREE_FILE = TEST_DIR /'ietf-optical-impairment-topology.tree'
EXPECTED_FILE = TEST_DIR /'ietf-optical-impairment-topology-expected.tree'
IETF_DIR = TEST_DIR / 'tests'
# use case 1 or case 2
# case 1: download ietf library from github
# Create temporary dir
# temp_dir = TEST_DIR /'ietf_library'
# try:
#     mkdir(temp_dir)
# except OSError:
#     print (f'Creation of the {temp_dir} directory failed.')
# print (f'Creation of the {temp_dir} directory')
# Clone into temporary dir
# git.Repo.clone_from('https://github.com/YangModels/yang.git', temp_dir, branch='master', depth=1)
# case 2 download only usefull files:

base_name = 'https://raw.githubusercontent.com/YangModels/yang/master/'
urls = ['standard/ietf/RFC/ietf-network@2018-02-26.yang',
        'standard/ietf/RFC/ietf-yang-types@2010-09-24.yang',
        'standard/ietf/RFC/ietf-network-topology@2018-02-26.yang',
        'standard/ietf/RFC/ietf-inet-types@2010-09-24.yang',
        'experimental/ietf-extracted-YANG-modules/ietf-te-types@2019-11-18.yang',
        'experimental/ietf-extracted-YANG-modules/ietf-layer0-types@2019-11-28.yang',
        'experimental/ietf-extracted-YANG-modules/ietf-te-topology@2019-02-07.yang']
# TODO automatically retrieve list of versions based on listing in the github

for url in urls:
    filename = url.split('/')[-1]
    try:
        unlink(f'{IETF_DIR}/{filename}')
    except FileNotFoundError:
        pass
    print(f'loading {url}')
    filename = wget.download(base_name + url, out=f'{IETF_DIR}')

@pytest.mark.parametrize("yangfile", [YANG_FILE])
def test_yang_tree(yangfile):
    res = subprocess.run(['pyang', '-f', 'tree', '-p', IETF_DIR, yangfile], stdout=subprocess.PIPE)
    if res.returncode != 0:
        assert False, f'pyang failed: exit code {res.returncode}'
    treefile = Path(yangfile).with_suffix('.tree')
    tree = open(treefile, 'r').read()
    assert res.stdout.decode('utf-8') == tree, "YANG tree rendering differs"

    for url in urls:
        filename = url.split('/')[-1]
        unlink(f'{IETF_DIR}/{filename}')
