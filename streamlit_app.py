import streamlit as st
import json
import yaml

def extract_structure_yaml(data, summary_lines, level=2):
    if isinstance(data, list):
        for item in data:
            extract_structure_yaml(item, summary_lines, level)
    elif isinstance(data, dict):
        if "section" in data:
            summary_lines.append(f"{'#' * level} {data['section']}\n")
        if "page" in data and "path" in data:
            page_title = data['path'].split("/")[-1]  # Extract last part of the path
            summary_lines.append(f"* [{page_title}]({data['path']}.md)\n")
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                extract_structure_yaml(value, summary_lines, level + 1)

def parse_docs_yaml(yaml_content):
    try:
        data = yaml.safe_load(yaml_content)
        summary_lines = ["# Table of contents\n"]
        extract_structure_yaml(data, summary_lines)
        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing YAML: {e}"

def extract_structure_json(data, summary_lines, level=2):
    if isinstance(data, list):
        for item in data:
            extract_structure_json(item, summary_lines, level)
    elif isinstance(data, dict):
        if "group" in data:
            summary_lines.append(f"{'#' * level} {data['group']}\n")
        if "pages" in data:
            for page in data["pages"]:
                if isinstance(page, str):
                    page_title = page.split("/")[-1]  # Extract last part of the path
                    summary_lines.append(f"* [{page_title}]({page}.md)\n")
                elif isinstance(page, dict):
                    extract_structure_json(page, summary_lines, level + 1)

def parse_mint_json(json_content):
    try:
        data = json.loads(json_content)
        summary_lines = ["# Table of contents\n"]
        if "navigation" in data:
            for item in data["navigation"].get("dropdowns", []):
                extract_structure_json(item, summary_lines)
        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error parsing JSON: {e}"

st.title("Docs to SUMMARY.md Converter")
format_option = st.selectbox("Select Input Format", ["docs.yml", "mint.json"])
uploaded_file = st.file_uploader("Upload file", type=["yml", "yaml", "json"])
text_input = st.text_area("Or paste content below:")

if st.button("Generate SUMMARY.md"):
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
    elif text_input:
        content = text_input
    else:
        content = None
    
    if content:
        if format_option == "docs.yml":
            summary_md = parse_docs_yaml(content)
        else:
            summary_md = parse_mint_json(content)
        
        st.subheader("Generated SUMMARY.md")
        st.code(summary_md, language="markdown")
        summary_bytes = summary_md.encode("utf-8")
        st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
