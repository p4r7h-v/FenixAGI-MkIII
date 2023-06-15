import xml.etree.ElementTree as ET

def parse_xml_data(xml_data):
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"Error parsing XML data: {e}")
        return None

    def parse_element(element):
        data = {'tag': element.tag, 'attributes': element.attrib, 'text': element.text.strip() if element.text else ""}
        children = [parse_element(child) for child in element]
        if children:
            data['children'] = children
        return data

    return parse_element(root)

# Example usage
if __name__ == '__main__':
    xml_data = '''
        <root>
            <element1 attribute1="value1">Text1</element1>
            <element2 attribute2="value2">
                <child1>Text2</child1>
                <child2 attribute3="value3">Text3</child2>
            </element2>
        </root>
    '''

    parsed_data = parse_xml_data(xml_data)
    print(parsed_data)