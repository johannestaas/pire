import re


class Match:

    def __init__(self, line, match):
        self.line = line
        self.match = match

    def format(self):
        if self.match is None:
            return (self.line, 'red')
        if self.match.groupdict():
            msg = f'{self.line}\t{self.match.groupdict()!r}'
        elif self.match.groups():
            msg = f'{self.line}\t{self.match.groups()!r}'
        else:
            msg = self.line
        return msg, None


class Regex:

    def __init__(self, regex_str):
        self.regex_str = regex_str
        self.enabled = (not regex_str.startswith('#'))
        if self.enabled:
            self.regex = re.compile(regex_str)
        else:
            self.regex = re.compile(regex_str[1:])
        self.output = []

    def match(self, line):
        if self.enabled:
            match = self.regex.match(line)
            self.output.append(Match(line, match))


def load_regexes(path):
    regex_strs = []
    with open(path) as f:
        for line in f:
            regex_strs.append(line.rstrip('\n'))
    return [
        Regex(regex_str)
        for regex_str in regex_strs
    ]


def run_regexes(regexes, line_gen):
    for line in line_gen:
        line = line.rstrip('\n')
        for regex in regexes:
            regex.match(line)
