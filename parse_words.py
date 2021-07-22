"""Solutions to an interview question.

You're given a set of "words" and a string that might be a concatenation
of elements of that set.  Return either `None`, indicating that the string is
not such a concatenation, or return a string that is the concatenation with
spaces between each constituent "word."
"""


import functools
import re
from typing import Any, Generator, Iterable, Optional, Set, Union


"""
Solution Using Regular Expressions
----------------------------------
This is problematic because there's no way to say "capture all of the values
this repeated subpattern matched."  That is, /foo_(<pattern>)+_bar/ only
captures the _last_ /<pattern>/.  You could instead have
/foo_(<pattern>+)_bar, but that would match the _concatenation_ of all
matches.  You lose information about the individual matches.

Since in general there's more than one way to break the input string into
words from the dictionary, we have to match the entire string over and over
again, each time extracting one match (the last one).

This is inefficient, but short.
"""
def solution_regex_inefficient(text: str, words: Set[str]) -> Optional[str]:
    if text == '':
        return ''

    pattern = f'({"|".join(words)})+'
    subject = text
    parts = []

    while subject != '':
        match = re.fullmatch(pattern, subject)
        if match is None:
            return None
        part, = match.groups()
        parts.append(part)
        subject = subject[:-len(part)]

    return ' '.join(reversed(parts))


"""
Solution Using Recursion
------------------------
The recursive solution lends itself well to lisp-style singly linked lists, and
prefix tries.  This solution first defines and then uses those data structures.
"""
class ChainNull:
    """A ChainNull is an empty singly linked list."""
    pass


Chain = Union['ChainLink', ChainNull]


class ChainLink:
    """A ChainLink is a node in a singly linked list."""
    EMPTY = ChainNull()

    value: Any
    suffix: Chain

    def __init__(self, value, suffix: Chain):
        self.value = value
        self.suffix = suffix

    def __iter__(self):
        chain = self
        while chain is not ChainLink.EMPTY:
            yield chain.value
            chain = chain.suffix
    

def prepend(value, chain: Chain) -> ChainLink:
    return ChainLink(value, chain)


def add_to_prefix_trie(trie: dict, word: str) -> dict:
    for letter in word:
        value = trie.get(letter)
        if value is not None:
            trie = value
        else:
            next_trie = {}
            trie[letter] = next_trie
            trie = next_trie
    trie[''] = word


def make_prefix_trie(words: Iterable[str]) -> dict:
    """A prefix trie is a `dict` that maps letters to tries, and has a special
    key, "" (the empty string), that is a `str` containing the matched prefix,
    if there is one.
    """
    trie = {}
    for word in words:
        add_to_prefix_trie(trie, word)
    return trie


def prefixes_of(text: str, trie: dict) -> Generator[str, None, None]:
    prefix = trie.get('')
    if prefix is not None:
        yield prefix

    for letter in text:
        trie = trie.get(letter)
        if trie is None:
            return

        prefix = trie.get('')
        if prefix is not None:
            yield prefix


def solution_recursive(text: str, words: Set[str]) -> Optional[str]:
    trie = make_prefix_trie(words)

    @functools.cache
    def recur(index: int) -> Optional[Chain]:
        current_text = text[index:]
        if current_text == '':
            return ChainLink.EMPTY

        for prefix in prefixes_of(current_text, trie):
            suffix_solution = recur(index + len(prefix))
            if suffix_solution is not None:
                return prepend(prefix, suffix_solution)

    chain = recur(0)
    if chain is None:
        return Non
    return ' '.join(chain)


if __name__ == '__main__':
    text = 'ininisbarfish'
    words = {'foo', 'bar', 'fish', 'h', 'is', 'ini', 'in'}

    print('using regex:', solution_regex_inefficient(text, words))
    print('using recursion:', solution_recursive(text, words))
