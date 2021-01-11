import unittest


class TestThreadedFilter(unittest.TestCase):
    def test_count(self):
        from lib.pt_scan import filter_ips2
        from lib.pt_ip import generate_ips
        ips = list(generate_ips(100000))
        f_ips = list(filter_ips2(ips, lambda x: x, 120, len(ips)))
        self.assertEqual(len(ips), len(f_ips))
