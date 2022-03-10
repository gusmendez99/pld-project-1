"""
 Open & Save File
"""
def save_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)


def load_file(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

# Str
def camel_to_snake(s):
    return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')