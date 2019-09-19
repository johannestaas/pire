from ezcurses import Cursed

from .regex_engine import load_regexes, run_regex


def gen_lines(input_path, preprocess):
    with open(input_path) as f:
        yield from preprocess(f)


def display(regexes, sel_regex, scr, regex_win, out_win, match_wins):
    regex_win.clear()
    out_win.clear()
    for win in match_wins:
        win.clear()
    for i, regex in enumerate(regexes):
        color = None if regex is not sel_regex else 'green'
        regex_win.write(regex.regex_str, pos=(0, i), color=color)
    regex_win.refresh()
    out_w, h = out_win.max_size()
    out_win.write('=' * out_w, pos=(0, 0), color='blue')
    for win in match_wins:
        win_w, _ = win.max_size()
        win.write('=' * win_w, pos=(0, 0), color='blue')
    for i, out in enumerate(sel_regex.output):
        pos = (0, i + 1)
        for win in match_wins:
            win.write('|', color='blue', pos=pos)
        if out.match is None:
            out_win.write(out.line, color='yellow', pos=pos)
            continue
        out_win.write(out.line, color=None, pos=pos)
        groups = out.match.groupdict() or out.match.groups()
        if groups:
            if isinstance(groups, dict):
                keys = list(groups.keys())
            else:
                keys = range(len(groups))
            for i, win in enumerate(match_wins):
                key = keys[i]
                win.write(groups[key], pos=(pos[0] + 1, pos[1]))
    for win in match_wins:
        win.refresh()
    out_win.refresh()


def run_pire(
    preprocess=None,
    regex_path=None,
    input_path=None,
    split_horiz=True,
):
    with Cursed() as scr:
        while True:
            regexes = load_regexes(regex_path)
            sel_regex = regexes[2]
            groups = sel_regex.num_groups
            if groups:
                group_cols = [8 // groups] * groups
                match_win_sizes = [4] + group_cols
            else:
                match_win_sizes = [12]
            layout = scr.new_layout()
            layout.add_row(2, [12])
            layout.add_row(10, match_win_sizes)
            layout.draw()
            rows = list(layout)
            regex_win = rows[0][0]
            out_win, *match_wins = rows[1]
            line_gen = gen_lines(input_path, preprocess)
            run_regex(sel_regex, line_gen)
            scr.clear()
            scr.refresh()
            display(regexes, sel_regex, scr, regex_win, out_win, match_wins)
            if scr.getkey() == 'q':
                break
