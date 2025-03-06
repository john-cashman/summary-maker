import streamlit as st
from bs4 import BeautifulSoup

def html_to_markdown(html_content):
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_output = "# Table of contents\n\n"  # Starting header for Table of Contents

    def extract_links(tag, level=1):
        """
        Extract links from the HTML, handle nested links recursively.
        """
        nonlocal markdown_output

        # Check if the tag is a group and treat it as a header
        if tag.name == 'span' and tag.get('class') == ['section']:
            # Convert group name to Markdown header
            group_name = tag.get_text(strip=True)
            markdown_output += f"## {group_name}\n"

        # Find all anchor tags in the current tag
        links = tag.find_all('a', href=True)

        for link in links:
            text = link.get_text(strip=True)
            href = link['href']

            # Convert .html to .md
            if href.endswith('.html'):
                href = href.replace('.html', '.md')

            # Add the link as a markdown list item
            markdown_output += "  " * (level - 1) + f"* [{text}]({href})\n"

            # Look for nested <dl> (definition list) elements and process them as sub-pages
            nested_dl = link.find_parent('dd')  # Check if it's in a <dd> (nested list item)
            if nested_dl:
                # Recursive call for nested <dl> inside the <dd>
                extract_links(nested_dl, level + 1)

    # Start processing from the entire document (or specific part if needed)
    extract_links(soup)

    return markdown_output

# Streamlit UI
st.title("HTML to Markdown Converter")

# Input HTML via a text area
html_input = st.text_area("Paste your HTML content here", height=300)

# Convert the HTML content to Markdown when user presses the button
if st.button("Convert to Markdown"):
    if html_input:
        # Convert the HTML input to Markdown
        markdown_content = html_to_markdown(html_input)

        # Display the converted Markdown content in a text area
        st.subheader("Converted Markdown")
        st.text_area("Markdown Output", value=markdown_content, height=300)
    else:
        st.error("Please paste HTML content into the text area.")
