import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    text = inp.read().split('\n')
    logs = [log.split('\t') for log in text if log]
    shas = [el[0][:7] for el in logs]
    message = [el[len(el) - 1] for el in logs]
    points_len = [73 - len(mes) for mes in message]
    for i in range(len(logs)):
        out.write(shas[i] + '.'*points_len[i] + message[i] + '\n')
