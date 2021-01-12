import unittest


class TestThreadedFilter(unittest.TestCase):
    def test_count(self):
        from lib.pt_scan import filter_ips2
        from lib.pt_ip import generate_ips

        COUNT = 102400

        ips = generate_ips(COUNT)
        f_ips = list(filter_ips2(ips, lambda x: x, 128, COUNT))
        self.assertEqual(COUNT, len(f_ips))
