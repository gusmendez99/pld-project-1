"""
 Tree models
"""

class ParseNode:
    def __init__(self, left = None, right = None, value = None, index = None):
        self.initials = set()
        self.finals = set()
        self.left = left
        self.right = right
        self.value = value
        self.idx = idx
        self.avoidable = False