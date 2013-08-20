#!/usr/bin/env python

import math
import subprocess
import unittest

def runSystemCmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()

class SystemTest(unittest.TestCase):
    def test_bios_vendor(self):
        expected = "American Megatrends Inc."
        actual = runSystemCmd("dmidecode -s bios-vendor")
        self.assertEqual(expected, actual)

    def test_bios_version(self):
        expected = "2.0"
        actual = runSystemCmd("dmidecode -s bios-version")
        self.assertEqual(expected, actual)

    def test_server_manufacturer(self):
        expected = "Supermicro"
        actual = runSystemCmd("dmidecode -s system-manufacturer")
        self.assertEqual(expected, actual)

    def test_server_model(self):
        expected = "SYS-6017R-72RFTP"
        actual = runSystemCmd("dmidecode -s system-product-name")
        self.assertEqual(expected, actual)

    def test_motherboard_manufacturer(self):
        expected = "Supermicro"
        actual = runSystemCmd("dmidecode -s baseboard-manufacturer")
        self.assertEqual(expected, actual)

    def test_motherboard_model(self):
        expected = "X9DRW-7/iTPF"
        actual = runSystemCmd("dmidecode -s baseboard-product-name")
        self.assertEqual(expected, actual)

    def test_cpu_socket_count(self):
        expected = "2"
        actual = runSystemCmd("cat /proc/cpuinfo | egrep 'physical id' | sort -u | wc -l")
        self.assertEqual(expected, actual)

    def test_cpu_core_count(self):
        expected = "24"
        actual = runSystemCmd("cat /proc/cpuinfo | egrep -c '^processor'")
        self.assertEqual(expected, actual)

    def test_cpu_models_match(self):
        expected = "1"
        actual = runSystemCmd("dmidecode -s processor-version | sort -u | wc -l")
        self.assertEqual(expected, actual)

    def test_cpu_model(self):
        expected = "Intel(R) Xeon(R) CPU E5-2620 0 @ 2.00GHz"
        actual = runSystemCmd("dmidecode -s processor-version | head -1")
        self.assertEqual(expected, actual)

    def test_cpu_frequency(self):
        expected = "2000 MHz"
        actual = runSystemCmd("dmidecode -s processor-frequency | head -1")
        self.assertEqual(expected, actual)

    def test_num_memory_modules(self):
        expected = "8"
        actual = runSystemCmd("dmidecode -t memory | egrep 'Configured Clock Speed' | egrep -cv 'Unknown'")
        self.assertEqual(expected, actual)

    def test_memory_speed_match(self):
        expected = "1"
        actual = runSystemCmd("dmidecode -t memory | egrep 'Configured Clock Speed' | egrep -v 'Unknown' | sort -u | wc -l")
        self.assertEqual(expected, actual)

    def test_memory_speed(self):
        expected = "1333 MHz"
        actual = runSystemCmd("dmidecode -t memory | egrep 'Configured Clock Speed' | egrep -v 'Unknown' | sort -u | cut -f2 -d ':'")
        self.assertEqual(expected, actual)

    def test_memory_type_match(self):
        expected = "1"
        actual = runSystemCmd("dmidecode -t memory | egrep -A4 'Form Factor: DIMM'  | egrep Type | egrep -v Unknown | sort -u | wc -l")
        self.assertEqual(expected, actual)

    def test_memory_type(self):
        expected = "DDR3"
        actual = runSystemCmd("dmidecode -t memory | egrep -A4 'Form Factor: DIMM'  | egrep Type | egrep -v Unknown | sort -u | cut -f2 -d ':'")
        self.assertEqual(expected, actual)

    def test_memory_ecc_match(self):
        expected = "1"
        actual = runSystemCmd("dmidecode -t memory | egrep -A5 'Form Factor: DIMM' | egrep 'Type Detail:' | egrep -v Synchronous | sort -u | wc -l")
        self.assertEqual(expected, actual)

    def test_memory_ecc(self):
        expected = "Registered (Buffered)"
        actual = runSystemCmd("dmidecode -t memory | egrep -A5 'Form Factor: DIMM' | egrep 'Type Detail:' | egrep -v Synchronous | sort -u | cut -f2 -d ':'")
        self.assertEqual(expected, actual)

    def test_memory_size_match(self):
        expected = "1"
        actual = runSystemCmd("dmidecode -t memory | egrep -B1 'Form Factor: DIMM' | egrep Size: | egrep -v 'No Module Installed' | sort -u | wc -l")
        self.assertEqual(expected, actual)

    def test_memory_size(self):
        expected = "16384 MB"
        actual = runSystemCmd("dmidecode -t memory | egrep -B1 'Form Factor: DIMM' | egrep Size: | egrep -v 'No Module Installed' | sort -u | cut -f2 -d ':'")
        self.assertEqual(expected, actual)

    def test_total_memory(self):
        expected = 132125660
        actual = runSystemCmd("cat /proc/meminfo | egrep MemTotal: | awk '{print $2}'")
        self.assertTrue(math.fabs(expected - int(actual)) < 1024)

    def test_eth0_present(self):
        expected = "1"
        actual = runSystemCmd("ip link show | egrep -c eth0")
        self.assertEqual(expected, actual) 

    def test_eth1_present(self):
        expected = "1"
        actual = runSystemCmd("ip link show | egrep -c eth1")
        self.assertEqual(expected, actual) 

    def test_eth2_present(self):
        expected = "1"
        actual = runSystemCmd("ip link show | egrep -c eth2")
        self.assertEqual(expected, actual) 

    def test_eth0_speed(self):
        expected = "10000Mb/s"
        actual = runSystemCmd("ethtool eth0 | egrep Speed: | awk '{print $2}'")
        self.assertEqual(expected, actual)

    def test_eth1_speed(self):
        expected = "10000Mb/s"
        actual = runSystemCmd("ethtool eth1 | egrep Speed: | awk '{print $2}'")
        self.assertEqual(expected, actual)

    def test_eth2_speed(self):
        expected = "1000Mb/s"
        actual = runSystemCmd("ethtool eth2 | egrep Speed: | awk '{print $2}'")
        self.assertEqual(expected, actual)

    def test_kernel_version(self):
        expected = "2.6.32-358.el6.x86_64"
        actual = runSystemCmd("uname -r")
        self.assertEqual(expected, actual) 

    def test_distro_version(self):
        expected = "Scientific Linux release 6.4 (Carbon)" 
        actual = runSystemCmd("cat /etc/redhat-release")
        self.assertEqual(expected, actual)


suite = unittest.TestLoader().loadTestsFromTestCase(SystemTest)
unittest.TextTestRunner().run(suite)
