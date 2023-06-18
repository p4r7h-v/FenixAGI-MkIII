import os
import datetime

def generate_sitemap(base_url, directory):
    """
    This function generates a sitemap for a website.
    
    :param base_url: The base URL of the website (e.g. "https://example.com")
    :param directory: The path to the root directory where the website files are located
    :return: A string containing the sitemap in XML format
    """
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.htm', '.php')):
                file_path = os.path.join(root, file)
                last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')

                relative_url = os.path.relpath(file_path, directory).replace('\\', '/')
                url = f"{base_url}/{relative_url}"
                
                sitemap += '<url>\n'
                sitemap += f'  <loc>{url}</loc>\n'
                sitemap += f'  <lastmod>{last_modified}</lastmod>\n'
                sitemap += '</url>\n'

    sitemap += '</urlset>\n'
    return sitemap


# Example of how to use the generate_sitemap function
website_base_url = "https://example.com"
website_directory = "/path/to/your/website/files"

sitemap = generate_sitemap(website_base_url, website_directory)

with open('sitemap.xml', 'w') as sitemap_file:
    sitemap_file.write(sitemap)