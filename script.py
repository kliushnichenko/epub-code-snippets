from pyquery import PyQuery as pq
import re

# Path to the HTML file
file_path = 'samples/split11.html'
namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}


def main():
    with open(file_path, 'rb') as file:
        html_content = file.read()

    doc = pq(html_content)
    doc.make_links_absolute(base_url="http://www.w3.org/1999/xhtml")
    print(doc('body'))

    pattern = re.compile(r'getThem')

    for element in doc('xhtml|p', namespaces=namespaces):
        pq_element = pq(element)

        text = pq_element.text()
        if text and pattern.search(text):
            print(f"Found match in element <{element.tag}>: {text}")


if __name__ == "__main__":
    main()