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


def display(
    regexes, sel_regex, scr, regex_win, out_win, start_y=0, start_x=0,
    lines=None,
):
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
        output = sel_regex.output[start_y:start_y + h]
        for i, out in enumerate(output):
            pos = (0, i + 1)
            out.draw(out_win, pos, start_x=start_x)
    else:
        for i, line in enumerate(lines):
            if i < start_y:
                continue
            if i >= start_y + h - 1:
                break
            out_win.write(
                line[start_x:], pos=(0, i - start_y + 1), color='yellow',
            )

    if sel_regex:
        total = f'MATCH:{sel_regex.stats()["matches"]}/{len(sel_regex.output)}'
    else:
        total = f'MATCH:0/{len(lines)}'
    out_win.write(
        (
            f'{total}  ?:help  q:quit  e:edit  w:regex_up  s:regex_down  '
            'r:out_up  f:out_down  [:page_up  ]:page_down'
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
    line_gen = gen_lines(input_paths)
    lines = list(line_gen)
    old_w, old_h = None, None
    with Cursed() as scr:
        sel_index = 0
        start_y = 0
        start_x = 0
        while True:
            w, h = scr.max_size()
            if old_w != w or old_h != h:
                regex_win, out_win = init_layout(scr)
                old_w, old_h = scr.max_size()
            regexes = load_regexes(regex_path)
            if not regexes:
                sel_regex = None
            else:
                sel_regex = regexes[sel_index]
            if sel_regex is not None:
                run_regex(sel_regex, lines)
                output = sel_regex.output
            else:
                output = lines
            scr.clear()
            scr.refresh()
            display(
                regexes, sel_regex, scr, regex_win, out_win,
                start_y=start_y, start_x=start_x, lines=output,
            )
            key = scr.getkey()
            if key == 'q':
                break
            elif key == 'e':
                edit_regex(regex_path)
            elif key == '?':
                draw_help(scr)
            elif key == 's':
                sel_index += 1
                sel_index %= len(regexes)
            elif key == 'w':
                sel_index -= 1
                sel_index %= len(regexes)
            elif key == 'r':
                start_y = max(start_y - 1, 0)
            elif key == 'f':
                start_y = min(start_y + 1, len(output))
            elif key == '[':
                start_y = max(start_y - 10, 0)
            elif key == ']':
                start_y = min(start_y + 10, len(output))
            elif key == 'g':
                start_y = 0
            elif key == 'G':
                start_y = len(output) - 1
            elif key == ',':
                start_x = max(start_x - 1, 0)
            elif key == '<':
                start_x = 0
            elif key == '.':
                # No max, meh.
                start_x += 1
            elif key == '>':
                start_x += 10
            elif sel_regex and key == 'n':
                first = sel_regex.first(after=start_y, match=True)
                if first is not None:
                    start_y = first
            elif sel_regex and key == 'N':
                first = sel_regex.first(before=start_y, match=True)
                if first is not None:
                    start_y = first
            elif sel_regex and key == 'm':
                first = sel_regex.first(after=start_y, match=False)
                if first is not None:
                    start_y = first
            elif sel_regex and key == 'M':
                first = sel_regex.first(before=start_y, match=False)
                if first is not None:
                    start_y = first


def draw_help(scr):
    w, h = scr.max_size()
    scr.clear()
    for i, txt in enumerate([
        '?: display this help',
        'q: quit',
        'e: open editor ($EDITOR environment variable)',
        's: select next regex',
        'w: select previous regex',
        'r: go up one line in output',
        'f: go down one line in output',
        '[: go up 10 lines',
        ']: go down 10 lines',
        'g: go to top of output',
        'G: go to bottom of output',
        ',: scroll output text left',
        '.: scroll output text right',
        '<: scroll output text to far left',
        '>: scroll output text right 10',
        'n: find next regex match after cursor',
        'N: find next regex match before cursor',
        'm: find next regex mismatch after cursor',
        'M: find next regex mismatch before cursor',
    ]):
        txt += ' ' * (w - len(txt))
        scr.write(txt, pos=(0, i), color=('white', 'blue'))
    for y in range(i + 1, h):
        scr.write(' ' * w, pos=(0, y), color=('white', 'blue'))
    scr.refresh()
    scr.getkey()


def init_layout(scr):
    layout = scr.new_layout()
    layout.add_row(2, [12])
    layout.add_row(10, [12])
    layout.draw()
    rows = list(layout)
    regex_win = rows[0][0]
    out_win = rows[1][0]
    return regex_win, out_win
