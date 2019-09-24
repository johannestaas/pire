import re
from collections import namedtuple


def _color_gen():
    colors = ('green', 'blue', 'magenta', 'cyan', 'white', 'red')
    color_i = 0
    while True:
        yield colors[color_i]
        color_i += 1
        color_i %= len(colors)


# Tracks where color text is inserted into lines for matched groups.
_Insert = namedtuple('_Insert', ('text', 'color'))


class Match:

    def __init__(self, line, match, names):
        self.line = line
        self.match = match
        self.names = names

    def draw(self, win, pos):
        # Return yellow if not a match.
        if self.match is None:
            win.write(self.line, color='yellow', pos=pos)
            return

        # Return default color if no groups defined.
        if not self.match.groups():
            win.write(self.line, color=None, pos=pos)
            return

        # Now we have to show the groups.
        self._draw_groups(win, pos)

    def _draw_groups(self, win, pos):
        # Sort by the match span, by start and longest ones.
        def _inverse_span_sort(name):
            span_start, span_end = self.match.span(name)
            # If they're equal starts, then take the longest one as the first.
            return (span_start, span_end * -1)
        names = sorted(self.names, key=_inverse_span_sort)
        inserts = []
        color_gen = _color_gen()
        for i, name in enumerate(names):
            color = next(color_gen)
            start, end = self.match.span(name)
            if isinstance(name, str):
                text = f'(?P<{name}>'
            else:
                text = f'([{name}]'
            inserts.append((start, i, _Insert(text, color)))
            inserts.append((end, -i, _Insert(')', color)))
        # This sorts it so it's naturally sorted by the order they should be
        # written in (i and -i make it so the later matches get written
        # inside).
        inserts = [
            (i_pos, ins)
            for i_pos, _, ins in sorted(inserts)
        ]

        x, y = pos
        last = 0
        for ipos, insert in inserts:
            if ipos > last:
                win.write(self.line[last:ipos], color=None, pos=(x, y))
                x += ipos - last
            win.write(insert.text, color=insert.color, pos=(x, y))
            x += len(insert.text)
            last = ipos
        if self.line[last:]:
            win.write(self.line[last:], color=None, pos=(x, y))


class Regex:

    def __init__(self, regex_str):
        self.regex_str = regex_str
        self.regex = re.compile(regex_str)
        self.num_groups = self.regex.groups
        if self.regex.groupindex.keys():
            self.group_names = list(self.regex.groupindex.keys())
        elif self.num_groups:
            self.group_names = list(range(1, self.num_groups + 1))
        else:
            self.group_names = None
        self.output = []

    def match(self, line):
        match = self.regex.match(line)
        self.output.append(Match(line, match, self.group_names))


def load_regexes(path):
    regex_strs = []
    with open(path) as f:
        for line in f:
            regex_strs.append(line.rstrip('\n'))
    return [
        Regex(regex_str)
        for regex_str in regex_strs
    ]


def run_regex(regex, line_gen):
    for line in line_gen:
        line = line.rstrip('\n')
        regex.match(line)
