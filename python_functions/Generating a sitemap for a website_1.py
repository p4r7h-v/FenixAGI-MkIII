import xml.etree.ElementTree as ET
from typing import List, Tuple

def generate_sitemap(urls: List[Tuple[str, str, float]]) -> str:
    xml_root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url, lastmod, priority in urls:
        url_element = ET.SubElement(xml_root, "url")

        loc_element = ET.SubElement(url_element, "loc")
        loc_element.text = url

        lastmod_element = ET.SubElement(url_element, "lastmod")
        lastmod_element.text = lastmod

        priority_element = ET.SubElement(url_element, "priority")
        priority_element.text = str(priority)

    sitemap = ET.tostring(xml_root, encoding="unicode", pretty_print=True)

    return sitemap

urls = [
    ("https://example.com", "2021-11-02T00:00:00Z", 1.0),
    ("https://example.com/about", "2021-11-02T00:00:00Z", 0.8),
    ("https://example.com/contact", "2021-11-02T00:00:00Z", 0.8),
]

sitemap = generate_sitemap(urls)
print(sitemap)

with open("sitemap.xml", "w") as f:
    f.write(sitemap)