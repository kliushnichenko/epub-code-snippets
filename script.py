from pyquery import PyQuery as pq
import re

# Path to the HTML file
split_num = "014"
file_path = f'samples/The_Robert_C._Martin_Clean_Code_split_{split_num}.html'

namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}
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
            print(f"Found match in element <{element.tag}>: {text}")
            tt_elems = pq_element.find('tt')
            if len(tt_elems) > 0:
                for tt_elem in tt_elems:
                    tt_pq = pq(tt_elem)
                    tt_pq.add_class("inline-code-snippet")
            else:
                pq_element.add_class("code-snippet")
                raw_html = pq_element.html()
                if raw_html.startswith('  '):
                    pq_element.html(raw_html[2:])

                prev_elem = pq_element.prev()
                if prev_elem[0].tag == 'blockquote':
                    prev_elem.add_class("listing-header")

    # restore xmlns namespace
    doc('html').attr("xmlns", "http://www.w3.org/1999/xhtml")
    with open(f'samples/split_{split_num}_patched.html', 'w', encoding='utf-8') as f:
        f.write(doc.html())  # Write the modified HTML content


def is_java_code(text: str) -> bool:
    for pattern in java_patterns:
        if text and pattern.search(text):
            return True

    return False

if __name__ == "__main__":
    main()
