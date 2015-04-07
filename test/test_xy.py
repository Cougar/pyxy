import unittest

from xy import Area, XY

class AreaTests(unittest.TestCase):
	def test_area(self):
		a1 = Area(-1, -2, 1, 2, 'name1')
		self.assertEqual(a1.xmin, -1)
		self.assertEqual(a1.ymin, -2)
		self.assertEqual(a1.xmax, 1)
		self.assertEqual(a1.ymax, 2)
		self.assertEqual(a1.name, 'name1')

		a2 = Area(10, 20, -10, -20, 'name2')
		self.assertEqual(a2.xmin, -10)
		self.assertEqual(a2.ymin, -20)
		self.assertEqual(a2.xmax, 10)
		self.assertEqual(a2.ymax, 20)
		self.assertEqual(a2.name, 'name2')

	def test_area_thin(self):
		self.assertRaises(Exception, Area, 0, 1, 0, 2, None)
		self.assertRaises(Exception, Area, 1, 0, 2, 0, None)
	
	def test_area_exact(self):
		a1 = Area(-10, -10, 10, 10, 'name1')
		a2 = Area(-10, -10, 10, 10, 'name2')
		a3 = Area(-15, -15, 15, 15, 'name2')
		self.assertTrue(a1.is_exact(a2))
		self.assertTrue(a2.is_exact(a1))
		self.assertFalse(a1.is_exact(a3))
		self.assertFalse(a3.is_exact(a1))

	def test_area_iside_outside(self):
		a1 = Area(-10, -10, 10, 10, 'name1')
		a2 = Area(-5, -5, 5, 5, 'name2')
		a3 = Area(-15, -15, 15, 15, 'name2')
		self.assertTrue(a2.is_inside(a1))
		self.assertFalse(a3.is_inside(a1))
		self.assertFalse(a2.is_around(a1))
		self.assertTrue(a3.is_around(a1))

	def test_area_no_overlap(self):
		a1 = Area(-10, -10, 10, 10, 'name1')
		a2 = Area(-15, -15, -10, -10, 'name2')
		self.assertFalse(a1.is_overlap(a2))
		self.assertFalse(a2.is_overlap(a1))
		a1 = Area(-10, -10, 10, 10, 'name1')
		a2 = Area(-15, -10, -10, 0, 'name2')
		self.assertFalse(a1.is_overlap(a2))
		self.assertFalse(a2.is_overlap(a1))

	def test_area_overlap(self):
		a1 = Area(-10, -10, 10, 10, 'name1')
		a2 = Area(-15, -15, -9, -9, 'name2')
		self.assertTrue(a1.is_overlap(a2))
		self.assertTrue(a2.is_overlap(a1))

class XYTests(unittest.TestCase):
	def setUp(self):
		self.m = XY(-100, -100, 100, 100)

	def test_empty_map(self):
		self.assertEqual(len(self.m.areas), 1)
		self.assertEqual(self.m.get_area_count(), (0, 1))
		self.assertEqual(self.m.find_area(0, 0).name, None)

	def test_one_area_replace(self):
		self.m.add_area(-100, -100, 100, 100, 'test')
		self.assertEqual(len(self.m.areas), 1)
		self.assertEqual(self.m.get_area_count(), (1, 0))
		self.assertEqual(self.m.find_area(0, 0).name, 'test')

	def test_one_area(self):
		m = XY(-100, -100, 100, 100)
		m.add_area(10, 20, -30, -40, 'test')
		self.assertEqual(len(m.areas), 5)
		self.assertEqual(m.get_area_count(), (1, 4))
		self.assertEqual(m.find_area(0, 0).name, 'test')
		self.assertEqual(m.find_area(20, 10).name, None)

	def test_area_overlaps(self):
		self.m.add_area(-20, -20, 20, 20, 'test')
		self.assertRaises(Exception, self.m.add_area, -10, -10, 10, 10, 'test2')
		self.assertRaises(Exception, self.m.add_area, -30, -30, 30, 30, 'test3')
		self.assertRaises(Exception, self.m.add_area, -30, -30, 10, 10, 'test4')
