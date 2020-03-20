#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Esther Le Rouzic
# @Date:   2019-06-07
"""
@author: esther.lerouzic
checks that  yang formatting if conform to ietf formatting standard

"""

from os import system, unlink
from pathlib import Path
import difflib
from colorama import Fore
import wget
import pytest

TEST_DIR = Path(__file__).parent.parent

YANG_FILE = TEST_DIR /'ietf-optical-impairment-topology.yang'
IETF_DIR = TEST_DIR / 'tests'
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

def color_diff(diff):
    for line in diff:
        if line.startswith('+'):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith('-'):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith('^'):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line

@pytest.mark.parametrize("yangfile", [YANG_FILE])
def test_formating(yangfile):
    my_cmd = f'pyang -f yang -p {IETF_DIR} --keep-comments --ietf --max-line-length 72 {yangfile} -o formated.yang'
    system(my_cmd)

    text1 = open("formated.yang").readlines()
    text2 = open(yangfile).readlines()
    test = list(difflib.unified_diff(text1, text2))

    diff = difflib.ndiff(text1, text2)
    diff = color_diff(diff)
    print('\n'.join(diff))

    assert not test, "YANG not up to ietf standard (trailing edges, ...)"

    unlink('formated.yang')
    for url in urls:
        filename = url.split('/')[-1]
        unlink(f'{IETF_DIR}/{filename}')
