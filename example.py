#!/usr/bin/env python

# Author: Epihaius
# Date: 2021-01-09
# Last revision: 2021-01-11
#
# This layout system is applicable to any kind of object that has a position
# and a size, e.g. colored rectangles in an image or widgets of a GUI system.
# This example uses the layout system to create rectangular blocks of text
# whose sizes and positions depend on how they are set up to occupy the space
# available to them.
# There are three types of text blocks, each made up of multiple instances of
# a particular text character:
#
#         BlockA:                 BlockB:                BlockC:
#
#  XXXXXXXXXXXXXXXXXXXX    ....................    ++++++++++++++++++++
#  XXXXXXXXXXXXXXXXXXXX    ....................    ++++++++++++++++++++
#  XXXXXXXXXXXXXXXXXXXX    ....................    ++++++++++++++++++++
#  XXXXXXXXXXXXXXXXXXXX    ....................    ++++++++++++++++++++
#  XXXXXXXXXXXXXXXXXXXX    ....................    ++++++++++++++++++++
#
# Any block can be attached to a "parent" block. This way, a hierarchy can be
# created, leading to complex, nested layouts.
#

from sizer import Sizer
from primitive import Primitive


class TextBlock(Primitive):

    def __init__(self, w, h, char, parent=None, sizer_borders=(0, 0, 0, 0)):

        Primitive.__init__(self, (w, h), sizer_borders)

        self.char = char
        self.parent = parent

    def get_net_pos(self, child_pos=(0, 0)):

        x_c, y_c = child_pos
        x, y = self.pos
        pos = (x + x_c, y + y_c)

        if self.parent:
            return self.parent.get_net_pos(pos)

        return pos

    def get_pos(self, net=False):

        if net:
            return self.get_net_pos()
        else:
            return self.pos


class BlockA(TextBlock):

    def __init__(self, w, h, parent=None, sizer_borders=(0, 0, 0, 0)):

        TextBlock.__init__(self, w, h, "X", parent, sizer_borders)


class BlockB(TextBlock):

    def __init__(self, w, h, parent=None, sizer_borders=(0, 0, 0, 0)):

        TextBlock.__init__(self, w, h, ".", parent, sizer_borders)


class BlockC(TextBlock):

    def __init__(self, w, h, parent=None, sizer_borders=(0, 0, 0, 0)):

        TextBlock.__init__(self, w, h, "+", parent, sizer_borders)


class App:

    def __init__(self):

        # create the main sizer
        main_sizer = Sizer("horizontal")
        # its first two columns are set to take up an equal amount of the width
        # assigned to it
        main_sizer.set_column_proportion(0, 1.)
        main_sizer.set_column_proportion(1, 1.)
        # its first row is set to take up all of the height assigned to it
        main_sizer.set_row_proportion(0, 1.)
        # create the first vertical subsizer...
        v_sizer1 = Sizer("vertical")
        # ...and add it to the main sizer, with 1-unit borders around it
        main_sizer.add(v_sizer1, borders=(1, 1, 1, 1))
        # create a BlockA instance, ensuring that if it gets its own sizer, the
        # latter will have borders around it, relative to the edges of that block
        block1 = BlockA(10, 10, sizer_borders=(2, 2, 1, 1))
        # add the block to `v_sizer1`, associating a vertical proportion of 1.
        # with its cell, which will be applied to its row in absence of an
        # explicitly set proportion;
        # a negative value is passed for the horizontal proportion, such that the
        # default proportion will be applied to the cell's column if none is set
        # explicitly
        v_sizer1.add(block1, proportions=(-1., 1.))
        # create a new grid-like sizer with space between its rows and columns...
        block1_sizer = Sizer("vertical", 3, gaps=(1, 2))
        # ...and assign it to `block1`; this allows the creation of a nested
        # layout, linked to `block1`
        block1.sizer = block1_sizer
        # create a nested layout
        block1_sizer.add(BlockC(5, 2, block1), proportions=(-1., .5))
        block1_sizer.add(BlockB(10, 2, block1), proportions=(-1., 1.))
        block1_sizer.add(BlockC(5, 2, block1), proportions=(-1., .5))
        block1_sizer.add(BlockB(10, 2, block1))
        block1_sizer.add(BlockC(5, 2, block1), proportions=(1., -1.))
        # add another block to `v_sizer1`, associating a horizontal proportion
        # of 1. with its cell, which will be applied to its column in absence of
        # an explicitly set proportion
        v_sizer1.add(BlockB(10, 2), proportions=(1., -1.), borders=(1, 2, 4, 3))
        # add a third block to `v_sizer1`, associating a vertical proportion of
        # .5 with its cell, which will be applied to its row in absence of an
        # explicitly set proportion
        v_sizer1.add(BlockC(5, 2), proportions=(-1., .5))
        # create the second vertical subsizer with space between its rows...
        v_sizer2 = Sizer("vertical", gaps=(0, 2))
        # ...and add it to the main sizer, with 1-unit borders around it and
        # centered horizontally within its column
        main_sizer.add(v_sizer2, alignments=("center", "expand"), borders=(1, 1, 1, 1))
        v_sizer2.add(BlockA(5, 2))
        v_sizer2.add(BlockB(20, 2), proportions=(-1., .25))
        # add a third block to `v_sizer2` and request it to be aligned to the
        # right of its cell
        v_sizer2.add(BlockC(1, 2), proportions=(-1., .75), alignments=("max", "expand"))
        # create the layout by updating the main sizer with the size of the
        # available space
        total_space = (80, 60)
        main_sizer.update(total_space)
        w_min, h_min = main_sizer.min_size
        # the minimum layout size could be bigger than the requested total space
        total_space = (max(80, w_min), max(60, h_min))

        # Generate the layout as blocks of text characters

        lines = [" " * total_space[0] + "\n" for _ in range(total_space[1])]

        for text_block in main_sizer.get_primitives():

            x, y = text_block.get_pos(net=True)
            w, h = text_block.get_size()
            c = text_block.char

            for i in range(h):
                line = lines[i+y]
                lines[i+y] = line[:x] + c * w + line[x+w:]

        with open("layout.txt", "w") as output_file:
            output_file.writelines(lines)


App()
