"""
 Open & Save File
"""
def save_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)


def load_file(filename):
    contents = None
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

def load_txt_file(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines
