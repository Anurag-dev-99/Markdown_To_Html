# Markup to HTML Converter

A Python tool that converts Markdown (and other markup) files to clean, styled HTML documents.

## Features

- 🎨 **Customizable styling** - Light or dark theme options
- 📑 **Table of contents** - Auto-generated navigation sidebar
- 🔢 **Math support** - LaTeX-style math expressions via MathJax
- 🎨 **Syntax highlighting** - Code blocks with Prism.js styling
- 📦 **Self-contained output** - Single HTML file with embedded resources

## Requirements

- Python 3.6+
- `markdown` Python package

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd markdowntopdf
   ```

2. Install dependencies:
   ```bash
   pip install markdown
   ```

## Usage

```bash
python convert_to_html.py <input.md> [output.html]
```

### Examples

Convert a markdown file with default output name:
```bash
python convert_to_html.py document.md
# Creates: document.html
```

Convert with custom output name:
```bash
python convert_to_html.py document.md my-page.html
# Creates: my-page.html
```

## How It Works

1. Reads the Markdown file and parses its content
2. Converts Markdown to HTML using the `markdown` library
3. Wraps the content in an HTML template with:
   - Dark mode styling (CSS)
   - Auto-generated table of contents (JavaScript)
   - MathJax for math rendering
   - Prism.js for syntax highlighting
4. Outputs a single, self-contained HTML file

## Example Output

The generated HTML includes:
- Responsive design for all screen sizes
- Sidebar navigation with table of contents
- Clickable headings for easy navigation
- Print-friendly CSS

## Dependencies

- `markdown` - For Markdown to HTML conversion

## License

MIT License - Feel free to use and modify.