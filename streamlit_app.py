import streamlit as st
import yaml
import json

# Function to extract links from HTML and convert to markdown
def html_to_markdown(html_content):
    from bs4 import BeautifulSoup
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_output = "# Table of contents\n\n"  # Starting header for Table of Contents

    # Set to keep track of already processed elements (to avoid infinite recursion)
    visited_tags = set()

    def extract_links(tag, level=1):
        """
        Extract links from the HTML, handle nested links recursively.
        """
        nonlocal markdown_output

        # Check if the tag is already processed to prevent infinite recursion
        tag_id = id(tag)
        if tag_id in visited_tags:
            return
        visited_tags.add(tag_id)

        # Check if the tag is a group and treat it as a header
        if tag.name == 'span' and tag.get('class') == ['section']:
            # Convert group name to Markdown header
            group_name = tag.get_text(strip=True)
            markdown_output += f"## {group_name}\n"  # Ensure only two hashtags (##)

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

# Function to extract structure from the YAML document
def extract_structure(data, summary_lines, level=2):
    """Recursively extracts section, page, and path from the YAML structure."""
    if isinstance(data, list):  # If the current data is a list, iterate over it
        for item in data:
            extract_structure(item, summary_lines, level)
    
    elif isinstance(data, dict):  # If it's a dictionary, look for relevant keys
        if "section" in data:
            # Use only two hashtags (##) for sections
            summary_lines.append(f"## {data['section']}\n")  # Sections become ##, not ###.
        
        if "page" in data and "path" in data:
            # Convert .mdx extension to .md in the page path
            path = data['path']
            if path.endswith('.mdx'):
                path = path.replace('.mdx', '.md')

            summary_lines.append(f"* [{data['page']}]({path})\n")
        
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

# Function to process mint.json data and convert to markdown
def mint_json_to_markdown(json_content):
    data = json.loads(json_content)
    markdown_output = "# Table of contents\n\n"
    
    def process_group(group, level=2):
        nonlocal markdown_output
        group_name = group['group']
        markdown_output += f"## {group_name}\n"  # Group names are converted to ## in markdown
        
        if 'pages' in group:
            for page in group['pages']:
                if isinstance(page, str):
                    # Single page link
                    markdown_output += f"* [{page.split('/')[-1]}]({page}.md)\n"
                elif isinstance(page, dict) and 'group' in page:
                    # Nested group
                    process_group(page, level + 1)
                    # For nested pages, list each page under its group
                    if 'pages' in page:
                        for nested_page in page['pages']:
                            markdown_output += f"  * [{nested_page.split('/')[-1]}]({nested_page}.md)\n"
    
    # Start the process with the root group
    process_group(data)
    
    return markdown_output

# Streamlit UI
st.title("Multi-format Markdown Converter")

# Option to choose between HTML, docs.yml, or mint.json input
option = st.selectbox("Choose the input format", ("HTML", "docs.yml", "mint.json"))

if option == "HTML":
    html_input = st.text_area("Paste your HTML content here", height=300)
    if st.button("Convert HTML to Markdown"):
        if html_input:
            try:
                # Convert the HTML input to Markdown
                markdown_content = html_to_markdown(html_input)

                # Display the converted Markdown content
                st.subheader("Generated Markdown")
                st.text_area("Markdown Output", value=markdown_content, height=300)

                # Provide a download button
                summary_bytes = markdown_content.encode("utf-8")
                st.download_button("Download Markdown", summary_bytes, "summary.md", "text/markdown")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please paste HTML content into the text area.")

elif option == "docs.yml":
    yaml_input = st.text_area("Paste your docs.yml content here", height=300)
    
    if st.button("Convert docs.yml to SUMMARY.md"):
        if yaml_input:
            try:
                # Parse the YAML input and convert to Markdown
                summary_md = parse_docs_yaml(yaml_input)
                
                st.subheader("Generated SUMMARY.md")
                st.code(summary_md, language="markdown")

                # Provide a download button
                summary_bytes = summary_md.encode("utf-8")
                st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please paste docs.yml content into the text area.")

elif option == "mint.json":
    json_input = st.text_area("Paste your mint.json content here", height=300)
    
    if st.button("Convert mint.json to SUMMARY.md"):
        if json_input:
            try:
                # Process the mint.json input and convert to Markdown
                summary_md = mint_json_to_markdown(json_input)
                
                st.subheader("Generated SUMMARY.md")
                st.code(summary_md, language="markdown")

                # Provide a download button
                summary_bytes = summary_md.encode("utf-8")
                st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please paste mint.json content into the text area.")
