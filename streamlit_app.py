import streamlit as st
import yaml
import json
from bs4 import BeautifulSoup

# Function to convert mint.json to SUMMARY.md format
def extract_mint_structure(data, summary_lines, level=2):
    """Recursively extracts group and page structure from the mint.json file."""
    if isinstance(data, list):  # If the current data is a list, iterate over it
        for item in data:
            extract_mint_structure(item, summary_lines, level)
    
    elif isinstance(data, dict):  # If it's a dictionary, look for relevant keys
        group = data.get("group", None)
        if group:
            summary_lines.append(f"{'#' * level} {group}\n")  # Sections become ##, ###, etc.
        
        pages = data.get("pages", None)
        if pages:
            for page in pages:
                if isinstance(page, dict):  # Handle nested groups
                    extract_mint_structure(page, summary_lines, level + 1)
                else:  # Handle direct pages
                    # Convert page to .md format
                    page_path = page.replace(".json", ".md")  # Make sure the page ends with .md
                    summary_lines.append(f"* [{page}]({page_path})\n")

def parse_mint_json(json_content):
    """Parses the mint.json file and extracts groups and pages."""
    try:
        data = json.loads(json_content)
        summary_lines = ["# Table of contents\n"]

        extract_mint_structure(data, summary_lines)

        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing mint.json: {e}"

# Function to recursively extract structure from docs.yml (Fern Docs)
def extract_structure(data, summary_lines, level=2):
    """Recursively extracts section, page, and path from the YAML structure."""
    if isinstance(data, list):  # If the current data is a list, iterate over it
        for item in data:
            extract_structure(item, summary_lines, level)
    
    elif isinstance(data, dict):  # If it's a dictionary, look for relevant keys
        if "section" in data:
            summary_lines.append(f"{'#' * level} {data['section']}\n")  # Sections become ##, ###, etc.
        
        if "page" in data and "path" in data:
            # Convert page to .md format
            page_path = data['path'].replace(".yml", ".md")
            summary_lines.append(f"* [{data['page']}]({page_path})\n")
        
        # Recursively check for nested structures
        for key, value in data.items():
            if isinstance(value, (list, dict)):  # If nested, go deeper
                extract_structure(value, summary_lines, level + 1)

def parse_docs_yaml(yaml_content):
    """Parses the YAML file and extracts sections, pages, and paths."""
    try:
        data = yaml.safe_load(yaml_content)
        summary_lines = ["# Table of contents\n"]

        extract_structure(data, summary_lines)

        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing YAML: {e}"

# Function to convert HTML to markdown
def extract_links(tag, summary_lines, level=2):
    """Extracts links from the HTML content and converts to markdown format."""
    links = tag.find_all('a', href=True)
    for link in links:
        link_text = link.get_text()
        link_href = link['href']
        # Convert .html to .md
        if link_href.endswith(".html"):
            link_href = link_href.replace(".html", ".md")
        summary_lines.append(f"{'  ' * (level - 2)}* [{link_text}]({link_href})\n")
    
    # Look for nested dl elements
    nested_dl = tag.find_all('dl')
    for nested in nested_dl:
        extract_links(nested, summary_lines, level + 1)

def html_to_markdown(html_content):
    """Converts HTML content to markdown format."""
    soup = BeautifulSoup(html_content, 'html.parser')
    summary_lines = ["# Table of contents\n"]
    
    # Extract links and convert to markdown format
    extract_links(soup, summary_lines)
    
    return "\n".join(summary_lines)

# Streamlit App UI
st.title("Document Converter to SUMMARY.md")

# Dropdown to select the format
format_selection = st.selectbox(
    "Select the format you want to import:",
    ("Select Format", "mint.json", "docs.yml", "HTML")
)

if format_selection == "mint.json":
    st.subheader("Mint JSON to SUMMARY.md Converter")
    json_content = st.text_area("Paste mint.json content here")

    if json_content:
        summary_md_json = parse_mint_json(json_content)
        
        st.subheader("Generated SUMMARY.md (from mint.json)")
        st.code(summary_md_json, language="markdown")

        # Provide a download button
        summary_bytes_json = summary_md_json.encode("utf-8")
        st.download_button("Download SUMMARY.md (from mint.json)", summary_bytes_json, "SUMMARY.md", "text/markdown")

elif format_selection == "docs.yml":
    st.subheader("Fern Docs YAML to SUMMARY.md Converter")
    yaml_content = st.text_area("Paste docs.yml content here")

    if yaml_content:
        summary_md_yaml = parse_docs_yaml(yaml_content)
        
        st.subheader("Generated SUMMARY.md (from docs.yml)")
        st.code(summary_md_yaml, language="markdown")

        # Provide a download button
        summary_bytes_yaml = summary_md_yaml.encode("utf-8")
        st.download_button("Download SUMMARY.md (from docs.yml)", summary_bytes_yaml, "SUMMARY.md", "text/markdown")

elif format_selection == "HTML":
    st.subheader("HTML to Markdown Converter")
    html_input = st.text_area("Paste HTML content here")

    if html_input:
        markdown_content = html_to_markdown(html_input)

        st.subheader("Generated SUMMARY.md (from HTML)")
        st.code(markdown_content, language="markdown")

        # Provide a download button
        summary_bytes_html = markdown_content.encode("utf-8")
        st.download_button("Download SUMMARY.md (from HTML)", summary_bytes_html, "SUMMARY.md", "text/markdown")
