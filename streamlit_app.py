import streamlit as st
import json
import yaml

def extract_json_structure(data, summary_lines, level=2):
    """Recursively extracts sections and pages from the JSON structure."""
    if isinstance(data, list):
        for item in data:
            extract_json_structure(item, summary_lines, level)
    elif isinstance(data, dict):
        if "group" in data:
            summary_lines.append(f"{'#' * level} {data['group']}\n")
        if "dropdown" in data:
            summary_lines.append(f"{'#' * level} {data['dropdown']}\n")
        if "pages" in data:
            for page in data["pages"]:
                if isinstance(page, str):
                    page_link = page + ".md"
                    summary_lines.append(f"* [{page}]({page_link})\n")
                elif isinstance(page, dict):
                    extract_json_structure(page, summary_lines, level + 1)
        if "groups" in data:
            for group in data["groups"]:
                extract_json_structure(group, summary_lines, level + 1)

def parse_mint_json(json_content):
    """Parses the JSON file and extracts navigation elements."""
    try:
        data = json.loads(json_content)
        summary_lines = ["# Table of contents\n"]
        if "navigation" in data and "dropdowns" in data["navigation"]:
            for item in data["navigation"]["dropdowns"]:
                extract_json_structure(item, summary_lines)
        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing JSON: {e}"

def extract_yaml_structure(data, summary_lines, level=2):
    """Recursively extracts sections and pages from the YAML structure."""
    if isinstance(data, list):
        for item in data:
            extract_yaml_structure(item, summary_lines, level)
    elif isinstance(data, dict):
        if "section" in data:
            summary_lines.append(f"{'#' * level} {data['section']}\n")
        if "page" in data and "path" in data:
            page_path = data["path"].replace(".mdx", ".md")
            summary_lines.append(f"* [{data['page']}]({page_path})\n")
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                extract_yaml_structure(value, summary_lines, level + 1)

def parse_docs_yaml(yaml_content):
    """Parses the YAML file and extracts sections, pages, and paths."""
    try:
        data = yaml.safe_load(yaml_content)
        summary_lines = ["# Table of contents\n"]
        extract_yaml_structure(data, summary_lines)
        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing YAML: {e}"

st.title("Docs to SUMMARY.md Converter")
format_option = st.selectbox("Select Input Format", ["docs.yml", "mint.json"])

if format_option == "docs.yml":
    uploaded_file = st.file_uploader("Upload docs.yml", type=["yml", "yaml"])
    yaml_input = st.text_area("Or paste docs.yml content below:")
    yaml_content = uploaded_file.read().decode("utf-8") if uploaded_file else yaml_input if yaml_input else None
    if st.button("Generate SUMMARY.md"):
        if yaml_content:
            summary_md = parse_docs_yaml(yaml_content)
            st.subheader("Generated SUMMARY.md")
            st.code(summary_md, language="markdown")
            st.download_button("Download SUMMARY.md", summary_md.encode("utf-8"), "SUMMARY.md", "text/markdown")
        else:
            st.warning("Please upload or paste the docs.yml content.")

elif format_option == "mint.json":
    uploaded_file = st.file_uploader("Upload mint.json", type=["json"])
    json_input = st.text_area("Or paste mint.json content below:")
    json_content = uploaded_file.read().decode("utf-8") if uploaded_file else json_input if json_input else None
    if st.button("Generate SUMMARY.md"):
        if json_content:
            summary_md = parse_mint_json(json_content)
            st.subheader("Generated SUMMARY.md")
            st.code(summary_md, language="markdown")
            st.download_button("Download SUMMARY.md", summary_md.encode("utf-8"), "SUMMARY.md", "text/markdown")
        else:
            st.warning("Please upload or paste the mint.json content.")
