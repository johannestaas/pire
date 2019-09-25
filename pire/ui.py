from subprocess import call

from ezcurses import Cursed

from .regex_engine import load_regexes, run_regex
from .local_os import get_editor


def edit_regex(path):
    editor = get_editor()
    call([editor, path])


def gen_lines(input_paths):
    for path in input_paths:
        with open(path) as f:
            yield from f


def display(regexes, sel_regex, scr, regex_win, out_win, start=0):
    """
    Displays the input matched against the regexes in two windows.
    """
    regex_win.clear()
    out_win.clear()
    for i, regex in enumerate(regexes):
        color = None if regex is not sel_regex else 'green'
        regex_win.write(regex.regex_str, pos=(0, i), color=color)
    regex_win.refresh()
    out_w, h = out_win.max_size()
    out_win.write('=' * out_w, pos=(0, 0), color='blue')
    if sel_regex is not None:
        output = sel_regex.output[start:start + h]
        for i, out in enumerate(output):
            pos = (0, i + 1)
            out.draw(out_win, pos)
    out_win.write(
        (
            '?:help q:quit  e:edit  w:regex_up  s:regex_down  r:out_up  '
            'f:out_down  [:page_up  ]:page_down'
        ),
        pos=(0, h - 1),
        color=('white', 'blue'),
    )
    out_win.refresh()


def run_pire(
    regex_path=None,
    input_paths=None,
    split_horiz=True,
):
    with Cursed() as scr:
        sel_index = 0
        output_start = 0
        while True:
            regexes = load_regexes(regex_path)
            if not regexes:
                sel_regex = None
            else:
                sel_regex = regexes[sel_index]
            layout = scr.new_layout()
            layout.add_row(2, [12])
            layout.add_row(10, [12])
            layout.draw()
            rows = list(layout)
            regex_win = rows[0][0]
            out_win = rows[1][0]
            line_gen = gen_lines(input_paths)
            if sel_regex is not None:
                run_regex(sel_regex, line_gen)
            scr.clear()
            scr.refresh()
            display(
                regexes, sel_regex, scr, regex_win, out_win,
                start=output_start,
            )
            key = scr.getkey()
            if key == 'q':
                break
            elif key == 'e':
                edit_regex(regex_path)
            elif key == 's':
                sel_index += 1
                sel_index %= len(regexes)
            elif key == 'w':
                sel_index -= 1
                sel_index %= len(regexes)
            elif key == 'r':
                output_start = max(output_start - 1, 0)
            elif key == 'f':
                output_start = min(output_start + 1, len(sel_regex.output))
            elif key == '[':
                output_start = max(output_start - 10, 0)
            elif key == ']':
                output_start = min(output_start + 10, len(sel_regex.output))
            elif key == 'g':
                output_start = 0
            elif key == 'G':
                output_start = len(sel_regex.output) - 1
            elif key == 'n':
                first = sel_regex.first(after=output_start, match=True)
                if first is not None:
                    output_start = first
            elif key == 'N':
                first = sel_regex.first(before=output_start, match=True)
                if first is not None:
                    output_start = first
            elif key == 'm':
                first = sel_regex.first(after=output_start, match=False)
                if first is not None:
                    output_start = first
            elif key == 'M':
                first = sel_regex.first(before=output_start, match=False)
                if first is not None:
                    output_start = first
