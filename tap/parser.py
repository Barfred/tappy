# Copyright (c) 2014, Matt Layman

import re

from tap.directive import Directive
from tap.line import Result


class Parser(object):
    """A parser for TAP files and lines."""

    # ok and not ok share most of the same characteristics.
    result_base = r"""\s*                    # Optional whitespace.
                      (?P<number>\d*)        # Optional test number.
                      \s*                    # Optional whitespace.
                      (?P<description>[^#]*) # Optional description before #.
                      \#?                    # Optional directive marker.
                      \s*                    # Optional whitespace.
                      (?P<directive>.*)      # Optional directive text
                   """
    ok = re.compile(r'^ok' + result_base, re.VERBOSE)

    def parse_line(self, text):
        """Parse a line into whatever TAP category it belongs."""
        match = self.ok.match(text)
        if match:
            return self.parse_result(match)

        # TODO: Integrate with all the other line types.

    def parse_result(self, match):
        """Parse a matching result line into a result instance."""
        return Result(
            True, match.group('number'), match.group('description').strip(),
            Directive(match.group('directive')))