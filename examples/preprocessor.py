def preprocess(f):
    for line in f:
        if line.startswith('#'):
            continue
        yield line
