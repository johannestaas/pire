import re


class Match:

    def __init__(self, line, match, names):
        self.line = line
        self.match = match
        self.names = names

    def draw(self, win, pos):
        if self.match is None:
            # Return if not a match.
            win.write(self.line, color='yellow', pos=pos)
            return
        if not self.match.groups():
            # Return if no groups defined.
            win.write(self.line, color=None, pos=pos)
            return
        names = sorted(self.names, key=lambda x: self.match.span(x))
        start, _ = self.match.span(names[0])
        x, y = pos
        last = 0

        def color():
            colors = ('green', 'blue', 'magenta', 'cyan', 'white', 'red')
            color_i = 0
            while True:
                yield colors[color_i]
                color_i += 1
                color_i %= len(colors)

        color_gen = color()

        for i, name in enumerate(names):
            start, end = self.match.span(name)
            group = self.match.group(name)
            if start > last:
                win.write(self.line[last:start], color=None, pos=(x, y))
                x += start - last
            if isinstance(name, str):
                text = f'(?P<{name}>'
            else:
                text = f'([{name}]'
            match_color = next(color_gen)
            win.write(text, color=match_color, pos=(x, y))
            x += len(text)
            win.write(group, color=None, pos=(x, y))
            x += len(group)
            win.write(')', color=match_color, pos=(x, y))
            x += 1
            last = end


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
