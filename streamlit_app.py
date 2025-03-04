import streamlit as st
import yaml
import io

def parse_docs_yaml(yaml_content):
    """Parses the YAML file and extracts sections, pages, and paths."""
    try:
        data = yaml.safe_load(yaml_content)
        summary_lines = ["# Table of contents\n"]
        
        if "navigation" in data and "layout" in data["navigation"]:
            for section in data["navigation"]["layout"]:
                if "section" in section and "contents" in section:
                    summary_lines.append(f"## {section['section']}\n")
                    for content in section["contents"]:
                        if "page" in content and "path" in content:
                            summary_lines.append(f"* [{content['page']}]({content['path']})\n")
        
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
