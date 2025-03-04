import streamlit as st
import yaml
import io

def extract_structure(data, summary_lines, level=2):
    """Recursively extracts section, page, and path from the YAML structure."""
    if isinstance(data, list):  # If the current data is a list, iterate over it
        for item in data:
            extract_structure(item, summary_lines, level)
    
    elif isinstance(data, dict):  # If it's a dictionary, look for relevant keys
        if "section" in data:
            summary_lines.append(f"{'#' * level} {data['section']}\n")  # Sections become ##, ###, etc.
        
        if "page" in data and "path" in data:
            summary_lines.append(f"* [{data['page']}]({data['path']})\n")
        
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

st.title("Fern Docs to SUMMARY.md Converter")

uploaded_file = st.file_uploader("Upload docs.yml", type=["yml", "yaml"])

if uploaded_file:
    yaml_content = uploaded_file.read().decode("utf-8")
    summary_md = parse_docs_yaml(yaml_content)
    
    st.subheader("Generated SUMMARY.md")
    st.code(summary_md, language="markdown")

    # Provide a download button
    summary_bytes = summary_md.encode("utf-8")
    st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
