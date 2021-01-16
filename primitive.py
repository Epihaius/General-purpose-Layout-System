# Author: Epihaius
# Date: 2021-01-09
# Last revision: 2021-01-16
#
# This module defines a `Primitive` class, the purpose of which is to link
# any kind of object with a position and size into the layout system.


class Primitive:

    def __init__(self, size, sizer_borders=(0, 0, 0, 0)):

        self.type = "primitive"
        self.pos = (0, 0)
        self._size = self._min_size = self._native_size = size
        self._sizer = None
        # the borders around the sizer
        self._sizer_borders = sizer_borders
        # the SizerCell this primitive is inside of
        self.sizer_cell = None
        self._on_destroy = lambda: None
        self._on_resize = lambda s: None
        self._on_reposition = lambda p: None

    def destroy(self):

        if self._sizer:
            self._sizer.destroy()
            self._sizer = None

        self.sizer_cell = None
        self._on_destroy()
        self._on_destroy = lambda: None
        self._on_resize = lambda s: None
        self._on_reposition = lambda p: None

    @property
    def on_destroy(self):

        return self._on_destroy

    @on_destroy.setter
    def on_destroy(self, on_destroy):

        self._on_destroy = on_destroy if on_destroy else lambda: None

    @property
    def on_resize(self):

        return self._on_resize

    @on_resize.setter
    def on_resize(self, on_resize):

        self._on_resize = on_resize if on_resize else lambda s: None

    @property
    def on_reposition(self):

        return self._on_reposition

    @on_reposition.setter
    def on_reposition(self, on_reposition):

        self._on_reposition = on_reposition if on_reposition else lambda p: None

    @property
    def sizer(self):

        return self._sizer

    @sizer.setter
    def sizer(self, sizer):

        if sizer:
            sizer.owner = self

        self._sizer = sizer

    @property
    def sizer_borders(self):

        return self._sizer_borders

    @sizer_borders.setter
    def sizer_borders(self, sizer_borders):

        self._sizer_borders = sizer_borders

        if self._sizer:
            self._sizer.owner = self

    @property
    def min_size(self):

        return self.get_min_size()

    def get_min_size(self, ignore_sizer=False):

        if ignore_sizer or not self._sizer:
            return self._min_size

        l, r, b, t = self._sizer_borders
        w_min, h_min = self._sizer.min_size

        return (w_min + l + r, h_min + b + t)

    @property
    def native_size(self):

        l, r, b, t = self._sizer_borders
        w, h = self._native_size
        w = max(w, l + r)
        h = max(h, b + t)

        return (w, h)

    def get_size(self):

        return self._size

    def set_size(self, size, is_min=False):

        w_old, h_old = self.get_size()
        width, height = size
        w_nat, h_nat = self.native_size
        width = max(w_nat, width)
        height = max(h_nat, height)

        if is_min:
            w_new, h_new = width, height
        else:
            w_min, h_min = self.min_size
            w_new, h_new = (max(w_min, width), max(h_min, height))

        new_size = (w_new, h_new)

        if self._sizer:
            l, r, b, t = self.sizer_borders
            self._sizer.set_size((w_new - l - r, h_new - b - t))

        self._size = new_size

        if is_min:
            self._min_size = new_size

        self._on_resize(new_size)

        return new_size

    def get_pos(self, net=False):

        return self.pos

    def set_pos(self, pos):

        self.pos = pos

        self._on_reposition(pos)
