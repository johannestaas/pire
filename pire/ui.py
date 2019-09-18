from ezcurses import Cursed

from .regex_engine import load_regexes, run_regexes


def gen_lines(input_path, preprocess):
    with open(input_path) as f:
        yield from preprocess(f)


def display(regexes, regex_win, out_win):
    regex_win.clear()
    out_win.clear()
    for i, regex in enumerate(regexes):
        color = 'red' if not regex.enabled else None
        regex_win.write(regex.regex_str, pos=(0, i), color=color)
    regex_win.refresh()
    for i, out in enumerate(regexes[2].output):
        msg, color = out.format()
        out_win.write(msg, pos=(0, i), color=color)
    out_win.refresh()


def run_pire(
    preprocess=None,
    regex_path=None,
    input_path=None,
    split_horiz=True,
):
    with Cursed() as scr:
        width, height = scr.max_size()
        if split_horiz:
            size = (width, height // 2)
            second_orig = (0, height // 2)
        else:
            size = (width // 2, height)
            second_orig = (width // 2, 0)
        regex_win = scr.new_win(orig=(0, 0), size=size)
        out_win = scr.new_win(orig=second_orig, size=size)
        while True:
            regexes = load_regexes(regex_path)
            line_gen = gen_lines(input_path, preprocess)
            run_regexes(regexes, line_gen)
            display(regexes, regex_win, out_win)
            scr.getch()
