import unittest
import os
from ptrlib.filestruct.elf import ELF
from logging import getLogger, FATAL

_is_windows = os.name == 'nt'


PATH_ELF = "./tests/test.bin/libc-2.27.so"
BASE = 0x7fffdeadb000

class TestELF1(unittest.TestCase):
    def setUp(self):
        getLogger("ptrlib").setLevel(FATAL)
        if _is_windows:
            self.skipTest("This test is intended for the Linux platform")
        self.elf = ELF(PATH_ELF)

    def test_symbol(self):
        self.elf.base = 0
        self.assertEqual(self.elf.symbol('system'), 0x4f440)
        self.assertEqual(self.elf.symbol('system'), 0x4f440) # test cache
        self.assertEqual(self.elf.symbol('__libc_system'), 0x4f440)
        self.assertEqual(self.elf.symbol('_IO_2_1_stdout_'), 0x3ec760)

        self.elf.base = BASE
        self.assertEqual(self.elf.symbol('system'), BASE + 0x4f440)
        self.assertEqual(self.elf.symbol('system'), BASE + 0x4f440)
        self.assertEqual(self.elf.symbol('getpwnam'), BASE + 0xe3260)
        self.assertEqual(self.elf.symbol('_IO_2_1_stdout_'), BASE + 0x3ec760)

    def test_search(self):
        self.elf.base = 0
        it = self.elf.search('A')
        self.assertEqual(next(it), 742)
        self.assertEqual(next(it), 925)
        self.assertEqual(next(it), 983)
        self.assertEqual(next(self.elf.search('A', writable=True)), 4099264)
        self.assertEqual(next(self.elf.find(b'/bin/sh\0')), 1785498)

        self.elf.base = BASE
        it = self.elf.search('A')
        self.assertEqual(next(it), BASE + 742)
        self.assertEqual(next(it), BASE + 925)
        self.assertEqual(next(it), BASE + 983)
        self.assertEqual(next(self.elf.search('A', writable=True)), BASE + 4099264)
        self.assertEqual(next(self.elf.find(b'/bin/sh\0')), BASE + 1785498)

    def test_main_arena(self):
        self.elf.base = 0
        self.assertEqual(self.elf.main_arena(), 0x3ebc40)
        self.elf.base = BASE
        self.assertEqual(self.elf.main_arena(), BASE + 0x3ebc40)

    def test_security(self):
        self.assertEqual(self.elf.relro(), 1)
        self.assertEqual(self.elf.ssp(), True)
        self.assertEqual(self.elf.nx(), True)
        self.assertEqual(self.elf.pie(), True)
