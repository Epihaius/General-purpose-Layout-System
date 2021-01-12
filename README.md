# General-purpose Layout System

A system that automatically takes care of placement and sizing of any kind of objects that can be manipulated in such a way. The resulting composition depends on desired alignments, use of available space and minimal offsets between those objects; no specific positions need to be assigned.

The spatial relationships between the objects will be retained whenever the available space changes.

Since this system is not tied to any particular existing software libraries, it can easily be integrated into any Python-based projects without additional dependencies.

Although the creation and maintaining of widget layouts is arguably its most practical application, this system is not specifically geared towards GUI's (graphical user interfaces).
In fact, the included example applies it to blocks of text, which should illustrate its versatile, general-purpose nature. Its output looks like this:

```
                                                                                
 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXXXXXXXXXXXXX          
 XX++++++++++X.......................XX           XXXXXXXXXXXXXXXXXXXX          
 XX++++++++++X.......................XX                                         
 XX++++++++++X.......................XX                                         
 XX++++++++++X.......................XX           ....................          
 XX++++++++++X.......................XX           ....................          
 XX++++++++++X.......................XX           ....................          
 XX++++++++++X.......................XX           ....................          
 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           ....................          
 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           ....................          
 XX..........X+++++++++++++++++++++++XX           ....................          
 XX..........X+++++++++++++++++++++++XX           ....................          
 XX..........X+++++++++++++++++++++++XX           ....................          
 XX..........X+++++++++++++++++++++++XX           ....................          
 XX..........X+++++++++++++++++++++++XX           ....................          
 XX..........X+++++++++++++++++++++++XX           ....................          
 XX..........X+++++++++++++++++++++++XX           ....................          
 XX..........X+++++++++++++++++++++++XX                                         
 XX..........X+++++++++++++++++++++++XX                                         
 XX..........X+++++++++++++++++++++++XX                              +          
 XX..........X+++++++++++++++++++++++XX                              +          
 XX..........X+++++++++++++++++++++++XX                              +          
 XX..........X+++++++++++++++++++++++XX                              +          
 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XX++++++++++XXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XX++++++++++XXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XX++++++++++XXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XX++++++++++XXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XX++++++++++XXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XX++++++++++XXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XX++++++++++XXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                              +          
                                                                     +          
                                                                     +          
                                                                     +          
  ...................................                                +          
  ...................................                                +          
                                                                     +          
                                                                     +          
                                                                     +          
                                                                     +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
 ++++++++++++++++++++++++++++++++++++++                              +          
                                                                                
```

The same layout can be visualized as colored rectangles in an image:

![layout](https://github.com/Epihaius/General-purpose-Layout-System/blob/main/layout.png "Layout of colored rectangles")


## Requirements

Python 3.5+

## Usage

There are no special installation requirements. Simply copy the `sizer.py` and `primitive.py` files to a convenient location, so they can easily be imported by the target project.

Here is a very basic code sample:

```python
from sizer import Sizer
from primitive import Primitive


class App:

    def __init__(self):

        # create a sizer to which primitives will be added horizontally (from
        # left to right)
        sizer = Sizer("horizontal")
        # allow the second primitive added to the sizer to take up all of the
        # space available to it
        sizer.set_column_proportion(1, 1.)
        # create the first primitive, 8 units wide and 6 units high...
        prim1 = Primitive((8, 6))
        # ...and center-align it vertically within the available height, while
        # making it take up all of the width of its column
        sizer.add(prim1, alignments=("expand", "center"))
        # add the second primitive, 4 units wide and 8 units high
        prim2 = Primitive((4, 8))
        sizer.add(prim2)
        # set the total available space to 20 by 10 units
        total_space = (20, 10)
        # create the layout by updating the sizer with the available space
        sizer.update(total_space)
        # the y-coordinate of the first primitive equals 1 instead of 0, since
        # it is centered within its row, which has a height of 8 due to the
        # height of the second primitive
        print("prim1 position:", prim1.get_pos(net=True))
        # the size of the first primitive remains unchanged
        print("prim1 size:", prim1.get_size())
        # the width of the second primitive equals 12, as it was resized to take
        # up all of the width assigned to its column (which is set up to take up
        # the entire remaining 12 units after assigning 8 units to the first
        # column)
        print("prim2 size:", prim2.get_size())


App()
```

An in-depth explanation with more code examples as well as a complete API reference can be found in the [Wiki](https://github.com/Epihaius/General-purpose-Layout-System/wiki).
