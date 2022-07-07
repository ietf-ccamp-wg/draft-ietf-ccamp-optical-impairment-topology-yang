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

official_yang_repo = 'https://raw.githubusercontent.com/YangModels/yang/master/'
layer0ext_repo = 'https://raw.githubusercontent.com/ietf-ccamp-wg/ietf-ccamp-layer0-types-ext/master/'
urls = [(official_yang_repo, 'standard/ietf/RFC/ietf-network@2018-02-26.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-yang-types@2013-07-15.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-network-topology@2018-02-26.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-inet-types@2013-07-15.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-te-types@2020-06-10.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-te-topology@2020-08-06.yang'),
        (layer0ext_repo, 'ietf-layer0-types.yang')]
# TODO automatically retrieve list of versions based on listing in the github

for url in urls:
    base_name, file = url
    filename = file.split('/')[-1]
    try:
        unlink(f'{IETF_DIR}/{filename}')
    except FileNotFoundError:
        pass
    print(f'loading {url}')
    filename = wget.download(base_name + file, out=f'{IETF_DIR}')


def test_pyang():
    """ first compile the yang with pyang
    """
    res = subprocess.run(['pyang', '-f', 'tree', '--tree-line-length', '69', '-p', IETF_DIR, YANG_FILE],
                         stdout=subprocess.PIPE, check=True)
    if res.returncode != 0:
        assert False, f'pyang failed: exit code {res.returncode}'


def test_yang_tree():
    """ check that the tree is consistent with the yang
    """
    res = subprocess.run(['pyang', '-f', 'tree', '--tree-line-length', '69', '-p', IETF_DIR, YANG_FILE],
                         stdout=subprocess.PIPE, check=True)
    treefile = Path(YANG_FILE).with_suffix('.tree')
    tree = '\n'.join([s for s in open(treefile, 'r').read().splitlines() if s])
    expected = '\n'.join([s for s in res.stdout.decode('utf-8').splitlines() if s])
    assert expected == tree, "YANG tree rendering differs"

    # remove downloaded yang files
    for url in urls:
        base_name, file = url
        filename = file.split('/')[-1]
        unlink(f'{IETF_DIR}/{filename}')
