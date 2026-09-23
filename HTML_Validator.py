#!/bin/python3


def validate_html(html):
    '''
    This function performs a limited version of html validation by checking whether every opening tag has a corresponding closing tag.

    >>> validate_html('<strong>example</strong>')
    True
    >>> validate_html('<strong>example')
    False
    >>> validate_html('<strong>python <u>is </strong> awesome </u>')
    False
    >>> validate_html('this is a <a href="https://izbicki.me">link</a>')
    True
    '''
    try:
        tags = _extract_tags(html)
    except ValueError:
        return False

    stack = []
    for tag in tags:
        if not tag.startswith('</'):
            stack.append(tag)
        else:
            # the matching opening tag is the closing tag without the slash
            opening_tag = '<' + tag[2:]
            if len(stack) == 0 or stack[-1] != opening_tag:
                return False
            stack.pop()

    return len(stack) == 0


def _extract_tags(html):
    '''
    This is a helper function for `validate_html`.
    By convention in Python, helper functions that are not meant to be used directly by the user are prefixed with an underscore.

    This function returns a list of all the html tags contained in the input string,
    stripping out all text not contained within angle brackets.

    >>> _extract_tags('Python <strong>rocks</strong>!')
    ['<strong>', '</strong>']

    Any attributes inside a tag are removed, so only the tag name is kept.

    >>> _extract_tags('<a href="https://izbicki.me">link</a>')
    ['<a>', '</a>']
    >>> _extract_tags('<span class=bold id=test></span>')
    ['<span>', '</span>']
    '''
    tags = []
    current = None
    for char in html:
        if char == '<':
            if current is not None:
                raise ValueError('found < without matching >')
            current = ''
        elif char == '>':
            if current is not None:
                name = current.split()[0] if current.strip() else ''
                tags.append('<' + name + '>')
                current = None
        elif current is not None:
            current += char
    if current is not None:
        raise ValueError('found < without matching >')
    return tags
