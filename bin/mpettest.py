#!/usr/bin/env python3

import os
import os.path as osp
import sys
import time

import tests.test_suite as tst

if len(sys.argv) > 1:
    compareDir = osp.join(os.getcwd(), sys.argv[1])
else:
    compareDir = None
timeStart = time.time()
tst.main(compareDir)
timeEnd = time.time()
tTot = timeEnd - timeStart
print("Total test time:", tTot, "s")
