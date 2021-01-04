"""Example2 module"""

from ._module import ToolframeModule

class Example2(ToolframeModule):
    """
    Example2 module class
    """
    def __init__(self) -> None:
        print('ex2 init!!!')
        super().__init__()
    def test(self):
        print('weeeeeee2!')
