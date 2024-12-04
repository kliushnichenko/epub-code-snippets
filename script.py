import os

from pyquery import PyQuery as pq
import re

source_dir = "source"
target_dir = "target"

java_patterns = [
    re.compile(r'\) \{'),           # Matches "someMethod() {"
    re.compile(r'int \w+;'),        # Matches "int variable" definition
    re.compile(r'int \w+ = .+;'),   # Matches "int dailyPay = hourlyRate * 8;" definition
    re.compile(r'if \('),           # Matches "if (condition)"
    re.compile(r'\);'),             # Matches "method();"
    re.compile(r'class \w+ \{'),    # Matches "class TestClass {"
    re.compile(r'enum \w+ \{'),     # Matches "enum TestEnum {"
    re.compile(r'// \w+'),          # Matches "// some comment"
    re.compile(r'/\*\*.+\*/'),      # Matches "/** some comment */"
    re.compile(r'\* <p/>'),
    re.compile(r'\* <pre/>'),
    re.compile(r'\* @param'),
    re.compile(r'public void'),
    re.compile(r'new byte\['),
    re.compile(r'RFC 2045'),
    re.compile(r'getAbsolutePath\(\)'),
    re.compile(r'package com\.example'),
    re.compile(r'public interface .+ \{'),
    re.compile(r'public abstract .+ \{'),
    re.compile(r'<bean id='),
    re.compile(r'svn get '),
    re.compile(r'\(\) < \d+'),         # Matches "stack.percentFull() < 50.0"
    re.compile(r'import package\.'),
]


def main():
    for filename in os.listdir(source_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(source_dir, filename)
            process_file(file_path, filename)


def process_file(file_path, filename):
    with open(file_path, 'rb') as file:
        original_html_content = file.read()

    doc = pq(original_html_content)

    # temporary remove xmlns namespace
    doc('html').remove_attr("xmlns")
    doc = pq(doc.html())

    for element in doc('p'):
        pq_element = pq(element)

        text = pq_element.text()
        if is_java_code(text):
            process_element(element, pq_element, text)

    # restore xmlns namespace
    result = f'<html xmlns="http://www.w3.org/1999/xhtml">{doc.html()}</html>'
    with open(f'{target_dir}/{filename}', 'w', encoding='utf-8') as f:
        f.write(result)


def process_element(element, pq_element, text):
    print(f"Found match in element <{element.tag}>: \n {text} \n\n")
    tt_elems = pq_element.find('tt')
    if len(tt_elems) > 0:
        # handle inline matches
        for tt_elem in tt_elems:
            tt_pq = pq(tt_elem)
            tt_pq.add_class("inline-code-snippet")
    else:
        pq_element.add_class("code-snippet")
        raw_html = pq_element.html()
        # remove odd whitespaces
        if raw_html.startswith('  '):
            pq_element.html(raw_html[2:])

        prev_elem = pq_element.prev()
        if prev_elem[0].tag == 'blockquote':
            prev_elem.add_class("listing-header")


def is_java_code(text: str) -> bool:
    for pattern in java_patterns:
        if text and pattern.search(text):
            return True

    return False


if __name__ == "__main__":
    main()
