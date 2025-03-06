import streamlit as st
import json
import yaml

def extract_structure_yaml(data, summary_lines, level=2):
    """Recursively extracts section, page, and path from the YAML structure."""
    if isinstance(data, list):
        for item in data:
            extract_structure_yaml(item, summary_lines, level)
    elif isinstance(data, dict):
        if "section" in data:
            summary_lines.append(f"{'#' * level} {data['section']}\n")
        if "page" in data and "path" in data:
            summary_lines.append(f"* [{data['page']}]({data['path']})\n")
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                extract_structure_yaml(value, summary_lines, level + 1)

def extract_structure_json(data, summary_lines, level=2):
    """Recursively extracts section, page, and path from the JSON structure."""
    if isinstance(data, list):
        for item in data:
            extract_structure_json(item, summary_lines, level)
    elif isinstance(data, dict):
        if "group" in data:
            summary_lines.append(f"{'#' * level} {data['group']}\n")
        if "pages" in data:
            for page in data["pages"]:
                if isinstance(page, str):
                    page_link = page.replace("/", "/") + ".md"
                    summary_lines.append(f"* [{page}]({page_link})\n")
                elif isinstance(page, dict):
                    extract_structure_json(page, summary_lines, level + 1)

def parse_data(content, format_type):
    """Parses JSON or YAML content and extracts groups and pages."""
    try:
        if format_type == "json":
            data = json.loads(content)
            summary_lines = ["# Table of contents\n"]
            if "navigation" in data:
                for item in data["navigation"]:
                    extract_structure_json(item, summary_lines)
            return "\n".join(summary_lines)
        else: #yaml
            data = yaml.safe_load(content)
            summary_lines = ["# Table of contents\n"]
            extract_structure_yaml(data, summary_lines)
            return "\n".join(summary_lines)

    except json.JSONDecodeError as e:
        return f"Error parsing JSON: Invalid JSON format. {e}"
    except yaml.YAMLError as e:
        return f"Error parsing YAML: Invalid YAML format. {e}"
    except Exception as e:
        return f"Error: {e}"

st.title("Docs to SUMMARY.md Converter")

format_option = st.selectbox("Select Input Format", ["docs.yml", "mint.json"])

if format_option == "docs.yml":
    file_type = "yaml"
    file_extensions = ["yml", "yaml"]
    default_text = """
- section: Getting Started
  - page: Introduction
    path: introduction.md
  - page: Installation
    path: installation.md
- section: User Guide
  - page: Usage
    path: usage.md
  - page: Advanced Features
    path: advanced.md
    """
elif format_option == "mint.json":
    file_type = "json"
    file_extensions = ["json"]
    default_text = """{
  "navigation": [
    {
      "group": "Getting Started",
      "pages": ["Introduction", "Installation"]
    },
    {
      "group": "User Guide",
      "pages": ["Usage", "Advanced Features"]
    }
  ]
}"""

uploaded_file = st.file_uploader(f"Upload {format_option}", type=file_extensions)
input_text = st.text_area(f"Or paste {format_option} content below:", value=default_text)

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
elif input_text:
    content = input_text
else:
    content = None

if content:
    summary_md = parse_data(content, file_type)
    st.subheader("Generated SUMMARY.md")
    st.code(summary_md, language="markdown")
    summary_bytes = summary_md.encode("utf-8")
    st.download_button("Download SUMMARY.md", summary_bytes, "SUMMARY.md", "text/markdown")
    st.success("Conversion successful!")
