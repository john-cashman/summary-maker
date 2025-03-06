import streamlit as st
from bs4 import BeautifulSoup
import os

def html_to_markdown(html_content):
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_output = ""

    # Process groups
    groups = soup.find_all(class_='group')  # Assuming groups have class "group", adjust based on your HTML structure
    for group in groups:
        group_name = group.get_text(strip=True)
        markdown_output += f"## {group_name}\n"

    # Process pages and subpages
    pages = soup.find_all(class_='page')  # Assuming pages have class "page", adjust based on your HTML structure
    for page in pages:
        page_name = page.get_text(strip=True)
        page_link = page.get('href', '').replace('.html', '.md')  # Convert .html to .md
        markdown_output += f"* [{page_name}]({page_link})\n"
        
        # Check for subpages
        subpages = page.find_all(class_='subpage')  # Assuming subpages have class "subpage", adjust as needed
        for subpage in subpages:
            subpage_name = subpage.get_text(strip=True)
            subpage_link = subpage.get('href', '').replace('.html', '.md')  # Convert .html to .md
            markdown_output += f"  * [{subpage_name}]({subpage_link})\n"

    return markdown_output

# Streamlit UI
st.title("HTML to Markdown Converter")

# Upload HTML file
html_file = st.file_uploader("Upload an HTML file", type=["html"])

if html_file is not None:
    html_content = html_file.read().decode('utf-8')
    
    # Convert HTML to Markdown
    markdown_content = html_to_markdown(html_content)
    
    # Display the markdown content
    st.subheader("Converted Markdown")
    st.code(markdown_content, language='markdown')
    
    # Provide an option to download the converted markdown file
    st.download_button(
        label="Download Markdown file",
        data=markdown_content,
        file_name="converted_file.md",
        mime="text/markdown"
    )
