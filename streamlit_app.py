import streamlit as st
import json
import yaml

def extract_structure(data, summary_lines, level=2):
    """Recursively extracts section, page, and path from the JSON structure."""
    if isinstance(data, list):  # If the current data is a list, iterate over it
        for item in data:
            extract_structure(item, summary_lines, level)
    
    elif isinstance(data, dict):  # If it's a dictionary, look for relevant keys
        if "group" in data:
            summary_lines.append(f"{'#' * level} {data['group']}\n")  # Groups become ##, ###, etc.
        
        if "pages" in data:
            for page in data["pages"]:
                if isinstance(page, str):  # If the page is just a string, create a markdown link
                    page_link = page.replace("/", "/") + ".md"
                    summary_lines.append(f"* [{page}]({page_link})\n")
                elif isinstance(page, dict):  # Handle nested groups
                    extract_structure(page, summary_lines, level + 1)

def parse_docs_yaml(yaml_content):
    """Parses the YAML file and extracts groups and pages."""
    try:
        data = yaml.safe_load(yaml_content)
        summary_lines = ["# Table of contents\n"]
        
        if "navigation" in data:
            for item in data["navigation"]:
                extract_structure(item, summary_lines)

        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing YAML: {e}"

def parse_mint_json(json_content):
    """Parses the JSON file and extracts groups and pages."""
    try:
        data = json.loads(json_content)
        summary_lines = ["# Table of contents\n"]

        if "navigation" in data:
            for item in data["navigation"]:
                extract_structure(item, summary_lines)

        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing JSON: {e}"

# Streamlit UI for selecting input format
st.title("Docs to SUMMARY.md Converter")

format_option = st.selectbox("Select Input Format", ["docs.yml", "mint.json"])

if format_option == "docs.yml":
    uploaded_file = st.file_uploader("Upload docs.yml", type=["yml", "yaml"])
    
    if uploaded_file:
        yaml_content = uploaded_file.read().decode("utf-8")
        summary_md = parse_docs_yaml(yaml_content)
        
        st.subheader("Generated SUMMARY.md")
        st.code(summary_md, language="markdown")

        # Provide a download button
        summary_bytes = summary_md.encode("utf-8")
        st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")

elif format_option == "mint.json":
    uploaded_file = st.file_uploader("Upload mint.json", type=["json"])
    
    if uploaded_file:
        json_content = uploaded_file.read().decode("utf-8")
        summary_md = parse_mint_json(json_content)
        
        st.subheader("Generated SUMMARY.md")
        st.code(summary_md, language="markdown")

        # Provide a download button
        summary_bytes = summary_md.encode("utf-8")
        st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
