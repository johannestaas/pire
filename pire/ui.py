from ezcurses import Cursed

from .regex_engine import load_regexes, run_regexes


def gen_lines(input_path, preprocess):
    with open(input_path) as f:
        yield from preprocess(f)


def display(regexes, scr, regex_win, out_win, match_win):
    regex_win.clear()
    out_win.clear()
    match_win.clear()
    for i, regex in enumerate(regexes):
        color = 'red' if not regex.enabled else None
        regex_win.write(regex.regex_str, pos=(0, i), color=color)
    regex_win.refresh()
    w, _ = scr.max_size()
    out_win.write('=' * (w // 2), pos=(0, 0), color='blue')
    match_win.write('=' * (w // 2), pos=(0, 0), color='blue')
    for i, out in enumerate(regexes[2].output):
        pos = (0, i + 1)
        match_win.write('|', color='blue', pos=pos)
        if out.match is None:
            out_win.write(out.line, color='yellow', pos=pos)
            continue
        out_win.write(out.line, color=None, pos=pos)
        groups = out.match.groupdict() or out.match.groups()
        if groups:
            match_win.write(repr(groups), pos=(pos[0] + 1, pos[1]))
    match_win.refresh()
    out_win.refresh()


def run_pire(
    preprocess=None,
    regex_path=None,
    input_path=None,
    split_horiz=True,
):
    with Cursed() as scr:
        layout = scr.new_layout()
        layout.add_row(3, [12])
        layout.add_row(9, [6, 6])
        layout.draw()
        rows = list(layout)
        regex_win = rows[0][0]
        out_win, match_win = rows[1]

        while True:
            regexes = load_regexes(regex_path)
            line_gen = gen_lines(input_path, preprocess)
            run_regexes(regexes, line_gen)
            scr.clear()
            scr.refresh()
            display(regexes, scr, regex_win, out_win, match_win)
            if scr.getkey() == 'q':
                break
