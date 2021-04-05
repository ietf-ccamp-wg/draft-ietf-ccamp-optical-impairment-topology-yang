#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Esther Le Rouzic
# @Date:   2019-06-07
"""
@author: esther.lerouzic
checks that yang module can be extracted from draft and that the extracted file is
consistent with working .yang (same file) and generates same tree

"""

from os import unlink
from pathlib import Path
import subprocess
import wget
import pytest

MAIN_DIR = Path(__file__).parent.parent

TXT_FILE = MAIN_DIR / 'I-D_in_xml/draft-ietf-ccamp-optical-impairment-topology-yang-06.txt'
YANG_FILE = MAIN_DIR / 'ietf-optical-impairment-topology.yang'
TREE_FILE = MAIN_DIR / 'ietf-optical-impairment-topology.tree'
IETF_DIR = MAIN_DIR / 'tests'
EXTRACTED_FILE = IETF_DIR / 'ietf-optical-impairment-topology.yang'


def test_xym():
    res = subprocess.run(['xym', TXT_FILE], stdout=subprocess.PIPE)
    if res.returncode != 0:
        assert False, f'xym failed: exit code {res.returncode}'


official_yang_repo = 'https://raw.githubusercontent.com/YangModels/yang/master/'
layer0ext_repo = 'https://raw.githubusercontent.com/ietf-ccamp-wg/ietf-ccamp-layer0-types-ext/master/'
urls = [(official_yang_repo, 'standard/ietf/RFC/ietf-network@2018-02-26.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-yang-types@2013-07-15.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-network-topology@2018-02-26.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-inet-types@2013-07-15.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-te-types@2020-06-10.yang'),
        (official_yang_repo, 'experimental/ietf-extracted-YANG-modules/ietf-layer0-types@2020-12-29.yang'),
        (official_yang_repo, 'standard/ietf/RFC/ietf-te-topology@2020-08-06.yang'),
        (layer0ext_repo, 'ietf-layer0-types-ext.yang')]
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


def test_trees():
    """ that both modules generate the same tree
    """
    res1 = subprocess.run(['pyang', '-f', 'tree', '--tree-line-length', '69', '-p', IETF_DIR, YANG_FILE], stdout=subprocess.PIPE)
    res2 = subprocess.run(['pyang', '-f', 'tree', '--tree-line-length', '69', '-p', IETF_DIR, EXTRACTED_FILE], stdout=subprocess.PIPE)
    treefile = Path(YANG_FILE).with_suffix('.tree')
    tree = open(treefile, 'r').read()
    assert res1.stdout.decode('utf-8') == res2.stdout.decode('utf-8'), "YANG tree rendering differs"

    # remove downloaded yang files
    for url in urls:
        base_name, file = url
        filename = file.split('/')[-1]
        unlink(f'{IETF_DIR}/{filename}')
