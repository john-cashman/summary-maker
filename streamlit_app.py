import streamlit as st
import yaml
import json

# Function to extract structure from YAML or JSON
def extract_structure(data, summary_lines, level=2):
    """Recursively extracts section, page, and path from the data structure."""
    if isinstance(data, list):  # If the current data is a list, iterate over it
        for item in data:
            extract_structure(item, summary_lines, level)
    
    elif isinstance(data, dict):  # If it's a dictionary, look for relevant keys
        if "section" in data:
            summary_lines.append(f"{'#' * level} {data['section']}\n")  # Sections become ##, ###, etc.
        
        if "page" in data and "path" in data:
            # Replace .mdx with .md in the page path
            page_path = data['path'].replace(".mdx", ".md")
            summary_lines.append(f"* [{data['page']}]({page_path})\n")
        
        # Recursively check for nested structures
        for key, value in data.items():
            if isinstance(value, (list, dict)):  # If nested, go deeper
                extract_structure(value, summary_lines, level + 1)

# Parse YAML content and convert it into SUMMARY.md format
def parse_docs_yaml(yaml_content):
    """Parses the YAML file and extracts sections, pages, and paths."""
    try:
        data = yaml.safe_load(yaml_content)
        summary_lines = ["# Table of contents\n"]

        extract_structure(data, summary_lines)

        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing YAML: {e}"

# Parse JSON content and convert it into SUMMARY.md format
def parse_mint_json(json_content):
    """Parses the JSON file and extracts sections, pages, and paths."""
    try:
        data = json.loads(json_content)
        summary_lines = ["# Table of contents\n"]

        extract_structure(data, summary_lines)

        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing JSON: {e}"

# Streamlit UI for selecting input format
st.title("Docs to SUMMARY.md Converter")

format_option = st.selectbox("Select Input Format", ["docs.yml", "mint.json"])

if format_option == "docs.yml":
    # File upload option for docs.yml
    uploaded_file = st.file_uploader("Upload docs.yml", type=["yml", "yaml"])
    
    # Text input field option for docs.yml
    yaml_input = st.text_area("Or paste docs.yml content below:")

    if uploaded_file:
        yaml_content = uploaded_file.read().decode("utf-8")
    elif yaml_input:
        yaml_content = yaml_input
    else:
        yaml_content = None
    
    # Button to generate the result for docs.yml
    if st.button("Generate SUMMARY.md"):
        if yaml_content:
            summary_md = parse_docs_yaml(yaml_content)
            if summary_md.startswith("Error"):
                st.error(summary_md)  # Show the error if parsing fails
            else:
                st.subheader("Generated SUMMARY.md")
                st.code(summary_md, language="markdown")

                # Provide a download button
                summary_bytes = summary_md.encode("utf-8")
                st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
        else:
            st.warning("Please upload or paste the docs.yml content to generate SUMMARY.md.")

elif format_option == "mint.json":
    # File upload option for mint.json
    uploaded_file = st.file_uploader("Upload mint.json", type=["json"])
    
    # Text input field option for mint.json
    json_input = st.text_area("Or paste mint.json content below:")

    if uploaded_file:
        json_content = uploaded_file.read().decode("utf-8")
    elif json_input:
        json_content = json_input
    else:
        json_content = None
    
    # Button to generate the result for mint.json
    if st.button("Generate SUMMARY.md"):
        if json_content:
            summary_md = parse_mint_json(json_content)
            if summary_md.startswith("Error"):
                st.error(summary_md)  # Show the error if parsing fails
            else:
                st.subheader("Generated SUMMARY.md")
                st.code(summary_md, language="markdown")

                # Provide a download button
                summary_bytes = summary_md.encode("utf-8")
                st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
        else:
            st.warning("Please upload or paste the mint.json content to generate SUMMARY.md.")
