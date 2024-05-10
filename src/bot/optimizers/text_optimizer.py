import re
import markdown
from markdownify import markdownify as md


def make_responsibility(current_str: str) -> list[str]:
    pattern = '[^\w \(\)\[\]\,\.]+'
    sentences = re.sub(pattern, '', current_str)

    special_substrings = ['т.п.', 'т.д.', 'т.к.']
    for subs in special_substrings:
        sentences = sentences.replace(subs, subs.replace('.', '_'))

    without_spaces = ['( ', ' )', '[ ', ' ]']
    for item in without_spaces:
        sentences = sentences.replace(item, item.replace(' ', ''))

    sentences = sentences.replace('...', '.')
    sentences = sentences.replace(' и.', '.')

    my_strings = sentences.split('.')

    for index, sentence in enumerate(my_strings):
        my_strings[index] = sentence.replace('_', '.').strip()

    my_strings = [string.capitalize() for string in my_strings if string]
    return my_strings


def make_key_skills(key_skills: list[dict[str]]):
    skills = []
    pattern = '[^\w \(\)\[\]\,\.]+'

    for item in key_skills:
        skills.append(re.sub(pattern, '', item.get('name')))

    skills = [skill.capitalize() for skill in skills if skill]
    return skills


def make_description(current_str: str) -> str:
    replace_keys = {
        '\n ': '',
        '<p>': '\n',
        '</p>': '\n',
        '<br />': '\n',
        '<strong>': '',
        '</strong>': '',
        '<em>': '',
        '</em>': '',
        '<li> ': '- ',
        '<li>': '- ',
        '</li>': ';\n',
        '<ul>': '',
        '</ul>': '\n',
        '  ': ' ',
    }

    for key, value in replace_keys.items():
        current_str = current_str.replace(key, value)

    array_strings = current_str.split('\n')
    current_str = '\n'.join([string.capitalize() for string in array_strings if string])
    current_str = re.sub('- \n', '- ', current_str)
    current_str = re.sub('[ \n\.\;\:\!\_]+;', ';', current_str)

    return current_str