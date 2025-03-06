import streamlit as st
from bs4 import BeautifulSoup

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

# Input HTML via a text area
html_input = st.text_area("Paste your HTML content here", height=300)

# Convert the HTML content to Markdown when user presses the button
if st.button("Convert to Markdown"):
    if html_input:
        # Convert the HTML input to Markdown
        markdown_content = html_to_markdown(html_input)

        # Display the converted Markdown content in a text area
        st.subheader("Converted Markdown")
        st.text_area("Markdown Output", value=markdown_content, height=300)
    else:
        st.error("Please paste HTML content into the text area.")
