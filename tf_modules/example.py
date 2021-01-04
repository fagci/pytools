"""Example module"""

from .module import ToolframeModule

class Example(ToolframeModule):
    """
    Example module class
    """
    def __init__(self) -> None:
        print('ex init!!!')
        super().__init__()
    def test(self):
        print('weeeeeee!')
