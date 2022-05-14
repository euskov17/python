def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    # if path.index('.') and len(path) != 1:
    #    path.replace('.', '')
    # path.replace('//', '/')
    if not path:
        return '.'
    if len(path) > 100000:
        return '.'
    dir = ""
    start_from_root = False
    if path[0] == '/':
        start_from_root = True
    path_l = list(filter(None, path.split('/')))
    path_l = list(filter(lambda x: x != '.', path_l))
    while path_l and start_from_root and path_l[0] == "..":
        path_l.pop(0)
    it = 1
    while it < len(path_l):
        if it != 0 and path_l[it] == '..' and path_l[it - 1] != '..':
            path_l.pop(it)
            path_l.pop(it - 1)
            it -= 2
        it += 1
    if not path_l and not start_from_root:
        dir = '.'
    if start_from_root:
        dir = '/'
    return dir + '/'.join(path_l)
