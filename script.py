from pyquery import PyQuery as pq
import re

# Path to the HTML file
file_path = 'samples/split11.html'

namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}
java_patterns = [
    re.compile(r'\) \{'),           # Matches "someMethod() {"
    re.compile(r'int \w+;'),        # Matches "int variable" definition
    re.compile(r'if \('),           # Matches "if (condition)"
    re.compile(r'\);'),             # Matches "method();"
    re.compile(r'class \w+ \{'),    # Matches "class TestClass {"
    re.compile(r'// \w+'),          # Matches "// some comment"
]


def main():
    with open(file_path, 'rb') as file:
        html_content = file.read()

    doc = pq(html_content)
    doc.make_links_absolute(base_url="http://www.w3.org/1999/xhtml")

    for element in doc('xhtml|p', namespaces=namespaces):
        pq_element = pq(element)

        text = pq_element.text()
        if is_java_code(text):
            print(f"Found match in element <{element.tag}>: {text}")
            pq_element.add_class("code-snippet")
            raw_html = pq_element.html()
            if raw_html.startswith('  '):
                pq_element.html(raw_html[2:])

    with open('samples/split11_patched.html', 'w', encoding='utf-8') as f:
        f.write(doc.html())  # Write the modified HTML content


def is_java_code(text: str) -> bool:
    for pattern in java_patterns:
        if text and pattern.search(text):
            return True

    return False


if __name__ == "__main__":
    main()
