import os
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10,
         output: tp.Optional[tp.IO[bytes]] = None) -> None:
    """
    :param filename: file to read lines from (the file
    can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    file = open(filename, 'rb')
    fsize = os.path.getsize(filename)
    if not fsize or not lines_amount:
        return
    lines_cnt = 0
    cnt = 1
    v = []
    left_bounce = 0
    while lines_cnt < lines_amount + 1 and 512 * cnt <= fsize:
        file.seek(-512 * cnt, os.SEEK_END)
        bt = file.read(512)
        v = list(memoryview(bt))
        lines_cnt += v.count(ord('\n'))
        cnt += 1
    cnt -= 1
    if 512 * (cnt + 1) > fsize and lines_cnt < lines_amount + 1:
        bt = file.read(fsize - 512 * cnt)
        v = list(memoryview(bt))
        lines_cnt += v.count(ord('\n'))
        if lines_cnt < lines_amount:
            if output:
                output.write(bt)
            else:
                print(bt.decode('utf-8'), end='')
        else:
            while lines_cnt > lines_amount:
                lines_cnt -= 1
                left_bounce += v[left_bounce:].index(ord('\n')) + 1
            file.seek(left_bounce, 0)
            bt = file.read(fsize - 512 * cnt - left_bounce)
            if output:
                output.write(bt)
            else:
                print(bt.decode('utf-8'), end='')
    elif cnt > 0:
        while lines_cnt > lines_amount:
            left_bounce += v[left_bounce:].index(ord('\n')) + 1
            lines_cnt -= 1
        file.seek(-512 * cnt + left_bounce, os.SEEK_END)
        bt = file.read(512 - left_bounce)
        if output:
            output.write(bt)
        else:
            print(bt.decode('utf-8'), end='')
        cnt -= 1
    file.seek(-512 * cnt, os.SEEK_END)
    for i in range(cnt):
        bt = file.read(512)
        if output:
            output.write(bt)
        else:
            print(bt.decode('utf-8'), end='')
    return
