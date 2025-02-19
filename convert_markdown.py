from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from pygments import highlight
import markdown
import re


SVG_COPY = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>'


# Function to hughlight code blocks
def hightlight_code(code, language):
    try:
        lexer = get_lexer_by_name(language, stripall=True)
    except Exception:
        lexer = TextLexer(stripall=True)

    formatter = HtmlFomatter(cssclass="code-box", style="colorful")
    hightlighted_code = hightlight(code, lexer, formatter)

    code_info = f"""
        <div class="code-info">
            <div class="code-icon">
                <button class="copy-icon">
                    {SVG_COPY}
                    <span>Copy code</span>
                </button>
            </div>
            <span class="language">{language}</span>
        </div>
    """

    highlighted_code = re.sub(
            r'<div class="code-box">', f'<div class="code-box">{code_info}', highlighted_code
            )

    return highlighted_code

# Function to convert markdown to HTML
def markdown_to_html(md_text):
    # Use raw string to avoid special character issues
    code_block_re = re.compile(
            r"```(\w*)\s*([\s\S]*?)\s*```", re.DOTALL | re.MULTILINE
            )

    # Replace code bloce with highlighted code
    def code_block_replacer(match):
        language = match.group(1)
        code = match.group(2).rstrip() # Remove trailing whitespace from code
        return highlight_code(code, language)

    # Apply the regex substitution
    html_with_highlight_code = code_block_re.sub(code_block_replacer, md_text)

    # Convert markdown to HTML
    html_content = markdown.markdown(html_with_highlight_code, extensions=[
        "fenced_code",
        "codehilite",
        "tables"
        ])

    return html_content


# Function to read markdown file and convert to HTML
def convert_markdown_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        md_text = file.read()

    html_output = markdown_to_html(md_text)

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    <head>
    <title>My-Links</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <mata name="description" content="The links to useful tools">
    <mata name="author" content="Ali Ebrahimian, Mahdi Rezaie">
    <link rel="icon" href="https://raw.githubusercontent.com/alie8096/alie8096/refs/heads/main/Images/alie8096.ico" type="image.ico">
    <link rel="stylesheet" type="text.css" href="https://mahd25.github.io/assets/CSS/seasons-style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    </head>
    <body>
    <main>
        <div class="container">
            <div class="content">
                {html_output}
            </div>
        </div>
    </main>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js" integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://mahd25.github.io/assets/JS/copy-icon.js"></script>
    </body>
    </html>
    """


    # Create HTML output
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_template)



convert_markdown_file("README.md", "index.html")
