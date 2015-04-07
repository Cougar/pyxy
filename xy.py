class Area(object):
	def __init__(self, x1, y1, x2, y2, name):
		if x1 == x2:
			raise Exception
		if y1 == y2:
			raise Exception
		if x1 < x2:
			self.xmin = x1
			self.xmax = x2
		else:
			self.xmin = x2
			self.xmax = x1
		if y1 < y2:
			self.ymin = y1
			self.ymax = y2
		else:
			self.ymin = y2
			self.ymax = y1
		self.name = name

	def is_exact(self, other):
		return self.xmin == other.xmin and self.xmax == other.xmax and self.ymin == other.ymin and self.ymax == other.ymax

	def is_inside(self, other):
		return self.xmin >= other.xmin and self.xmax <= other.xmax and self.ymin >= other.ymin and self.ymax <= other.ymax

	def is_around(self ,other):
		return other.is_inside(self)

	def is_overlap(self, other):
		if self.xmin >= other.xmax or self.xmax <= other.xmin or self.ymin >= other.ymax or self.ymax <= other.ymin:
			return False
		x = False
		y = False
		if self.xmin >= other.xmin and self.xmin <= other.xmax:
			x = True
		if self.xmax >= other.xmin and self.xmax <= other.xmax:
			x = True
		if self.ymin >= other.ymin and self.ymin <= other.ymax:
			y = True
		if self.ymax >= other.ymin and self.ymax <= other.ymax:
			y = True
		return x and y

	def __str__(self):
		return "(%d, %d) - (%d, %d) - %s" % (self.xmin, self.ymin, self.xmax, self.ymax, str(self.name))

class XY(object):
	def __init__(self, xmin, ymin, xmax, ymax):
		self.areas = []
		self.xmin = xmin
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax
		self.areas.append(Area(xmin, ymin, xmax, ymax, None))

	def add_area(self, x1, y1, x2, y2, name):
		area = Area(x1, y1, x2, y2, name)
		overlaps = []
		for a in self.areas:
			if area.is_exact(a):
				if a.name:
					raise Exception('eexactly the same area exists')
				else:
					self._add_area_replace(area, a)
					return
			if area.is_inside(a):
				if a.name:
					raise Exception('inside existing area')
				else:
					self._add_area_inside(area ,a)
					return

			if area.is_around(a): 
				if a.name:
					raise Exception('around existing area')
				else:
					overlaps.append(a)
			if a.is_overlap(area):
				if a.name:
					raise Exception('overlapping with existing area')
				else:
					overlaps.append(a)
		raise NotImplementedError

	def _add_area(self, area):
		self.areas.append(area)

	def _add_area_replace(self, new, old):
		self.areas.remove(old)
		self._add_area(new)

	def _add_area_inside(self, new, old):
		self.areas.remove(old)
		self._add_area(new)
		# add empty areas around
		# TODO check which side is bigger
		self._add_area(Area(old.xmin, old.ymin, new.xmin, old.ymax, None))
		self._add_area(Area(new.xmax, old.ymin, old.xmax, old.ymax, None))
		self._add_area(Area(new.xmin, old.ymin, new.xmax, new.ymin, None))
		self._add_area(Area(new.xmin, new.ymax, new.xmax, old.ymax, None))

	def find_area(self, x, y):
		for a in self.areas:
			if x >= a.xmin and x <= a.xmax and y >= a.ymin and y <= a.ymax:
				return a
		return None

	def get_area_count(self):
		used = 0
		free = 0
		for a in self.areas:
			if a.name:
				used += 1
			else:
				free += 1
		return (used, free)

	def __str__(self):
		areas = ""
		for a in self.areas:
			areas += "\n" + str(a)
		return areas
