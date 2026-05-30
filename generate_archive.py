import os
import re
import sys

try:
    import markdown
except ImportError:
    print("Error: The 'markdown' package is required. Install it using: pip install markdown")
    sys.exit(1)

# Using simple double-curly-brace placeholders for text replacement
# This allows all CSS and JS blocks to write standard single-curly-brace blocks.
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <style>
        :root {
            --bg-base: #131314;
            --bg-sidebar: #1e1f20;
            --bg-card: #1e1f20;
            --bg-code: #0f0f10;
            --bg-inline-code: #2d2f31;
            --border-color: #444746;
            --border-muted: #2f3032;
            --text-primary: #e3e3e3;
            --text-secondary: #c4c7c5;
            --text-muted: #8e918f;
            --accent: #8ab4f8;
            --accent-hover: #a8c7fa;
            --accent-bg: rgba(138, 180, 248, 0.08);
            --math-color: #fbc02d;
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            --font-mono: ui-monospace, SFMono-Regular, SF Pro Mono, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background-color: var(--bg-base);
            background-image: radial-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 0);
            background-size: 24px 24px;
            color: var(--text-primary);
            font-family: var(--font-sans);
            font-size: 15px;
            line-height: 1.6;
            letter-spacing: 0.2px;
            display: flex;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .app-container { display: flex; width: 100%; }
        
        .sidebar {
            width: 300px;
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            position: fixed;
            top: 0; bottom: 0; left: 0;
            z-index: 100;
            display: flex;
            flex-direction: column;
            user-select: none;
        }

        .sidebar-header { padding: 24px; border-bottom: 1px solid var(--border-muted); }
        .logo-area { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
        .logo-icon { color: var(--accent); flex-shrink: 0; }
        .logo-title { font-size: 16px; font-weight: 600; letter-spacing: 0.5px; color: var(--text-primary); }
        
        .search-wrapper { position: relative; }
        .search-input {
            width: 100%;
            background-color: var(--bg-base);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 12px 10px 36px;
            color: var(--text-primary);
            font-size: 13px;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .search-input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-bg); }
        .search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-muted); pointer-events: none; }

        .toc-wrapper { flex-grow: 1; overflow-y: auto; padding: 16px 12px; }
        .toc-list { list-style: none; }
        .toc-item { margin-bottom: 4px; }
        .toc-item a {
            display: block; padding: 8px 12px; color: var(--text-secondary); text-decoration: none;
            font-size: 13px; border-radius: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            transition: background-color 0.2s, color 0.2s;
        }
        .toc-item a:hover { background-color: rgba(255, 255, 255, 0.04); color: var(--text-primary); }
        .toc-item.active a { background-color: var(--accent-bg); color: var(--accent); font-weight: 500; }
        .toc-h3 { padding-left: 16px; }

        .sidebar-footer { padding: 16px 24px; border-top: 1px solid var(--border-muted); font-size: 11px; color: var(--text-muted); display: flex; justify-content: space-between; }

        .main-content { margin-left: 300px; flex-grow: 1; min-width: 0; padding: 40px 60px; display: flex; flex-direction: column; align-items: flex-start; }
        
        .document-header { width: 100%; max-width: 1000px; border-bottom: 1px solid var(--border-color); padding-bottom: 24px; margin-bottom: 32px; }
        .badge-row { display: flex; gap: 8px; margin-bottom: 12px; }
        .badge { background-color: var(--border-color); color: var(--text-secondary); padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .badge.interactive { background-color: var(--accent-bg); color: var(--accent); }
        .doc-title { font-size: 28px; font-weight: 700; color: var(--text-primary); line-height: 1.3; }

        .chat-document { width: 100%; max-width: 1000px; }
        .archive-section {
            margin-bottom: 40px; background-color: rgba(255, 255, 255, 0.01);
            border: 1px solid var(--border-muted); border-radius: 12px; padding: 24px 32px;
            transition: border-color 0.3s;
        }
        .archive-section:hover { border-color: rgba(138, 180, 248, 0.25); }

        p { margin-bottom: 16px; color: var(--text-secondary); }
        h2 { font-size: 20px; font-weight: 600; color: var(--text-primary); margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border-muted); margin-top: 12px; }
        h3 { font-size: 16px; font-weight: 600; color: var(--accent); margin-top: 24px; margin-bottom: 12px; }
        ul, ol { margin-bottom: 16px; padding-left: 24px; }
        li { margin-bottom: 8px; color: var(--text-secondary); }
        li::marker { color: var(--accent); }
        li ul, li ol { margin-top: 8px; margin-bottom: 4px; }
        
        code { font-family: var(--font-mono); background-color: var(--bg-inline-code); padding: 2px 6px; border-radius: 4px; font-size: 13px; color: #e5c07b; word-break: break-all; }
        .math-expr { font-family: var(--font-mono); background-color: var(--bg-inline-code); padding: 2px 6px; border-radius: 4px; color: var(--math-color); font-size: 13px; white-space: nowrap; }
        
        hr { border: none; border-top: 1px dashed var(--border-color); margin: 32px 0; width: 100%; }
        strong { color: var(--text-primary); font-weight: 600; }

        .code-block-wrapper { background-color: var(--bg-code); border: 1px solid var(--border-color); border-radius: 8px; margin: 16px 0; overflow: hidden; }
        .code-block-header { display: flex; justify-content: space-between; align-items: center; background-color: rgba(255, 255, 255, 0.03); padding: 8px 16px; border-bottom: 1px solid var(--border-color); font-family: var(--font-mono); font-size: 11px; color: var(--text-muted); }
        .copy-btn { background: none; border: none; color: var(--text-muted); cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 11px; padding: 4px 8px; border-radius: 4px; }
        .copy-btn:hover { background-color: rgba(255, 255, 255, 0.06); color: var(--text-primary); }
        pre { padding: 16px; overflow-x: auto; font-family: var(--font-mono); font-size: 13px; line-height: 1.5; }

        @media (max-width: 900px) {
            .sidebar { display: none; }
            .main-content { margin-left: 0; padding: 24px; }
        }

        @media print {
            @page { size: A4 portrait; margin: 20mm 15mm 20mm 15mm; }
            body { background: #ffffff !important; color: #1a1a1a !important; font-size: 11pt; }
            .sidebar { display: none !important; }
            .main-content { margin-left: 0 !important; padding: 0 !important; width: 100% !important; max-width: 100% !important; }
            .document-header { border-bottom: 2px solid #1a1a1a !important; }
            .doc-title { color: #000000 !important; }
            .archive-section { border: none !important; background: none !important; padding: 0 !important; margin-bottom: 40px !important; page-break-inside: avoid; }
            h2, h3 { color: #000000 !important; border-bottom-color: #cccccc !important; page-break-after: avoid; }
            p, li { color: #222222 !important; }
            code, .math-expr { background-color: #f1f1f1 !important; color: #000000 !important; border: 1px solid #cccccc !important; font-size: 9.5pt; }
            .code-block-wrapper { border: 1px solid #cccccc !important; background-color: #fcfcfc !important; page-break-inside: avoid; }
            .code-block-header { border-bottom: 1px solid #cccccc !important; background-color: #f1f1f1 !important; }
            .copy-btn { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="logo-area">
                    <svg class="logo-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                        <polyline points="2 17 12 22 22 17"></polyline>
                        <polyline points="2 12 12 17 22 12"></polyline>
                    </svg>
                    <span class="logo-title">AI Studio Archive</span>
                </div>
                <div class="search-wrapper">
                    <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input type="text" class="search-input" id="search-input" placeholder="Search sections...">
                </div>
            </div>
            <nav class="toc-wrapper">
                <ul class="toc-list" id="toc-list"></ul>
            </nav>
            <div class="sidebar-footer">
                <span>Status: Local</span>
                <span>Generated Build</span>
            </div>
        </aside>

        <main class="main-content">
            <header class="document-header">
                <div class="badge-row">
                    <div class="badge interactive">Generated Archive</div>
                    <div class="badge">Offline</div>
                </div>
                <h1 class="doc-title">{{TITLE}}</h1>
            </header>
            
            <article class="chat-document" id="document-root">
                {{BODY}}
            </article>
        </main>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const documentRoot = document.getElementById("document-root");
            const tocList = document.getElementById("toc-list");
            const searchInput = document.getElementById("search-input");
            const sections = document.querySelectorAll(".archive-section");

            sections.forEach((section) => {
                const heading = section.querySelector("h2, h3");
                if (!heading) return;

                const headingText = heading.textContent;
                const sectionId = section.id;

                const li = document.createElement("li");
                li.className = "toc-item toc-" + heading.tagName.toLowerCase();
                li.setAttribute("data-target", sectionId);

                const a = document.createElement("a");
                a.href = "#" + sectionId;
                a.textContent = headingText;
                
                a.addEventListener("click", (e) => {
                    e.preventDefault();
                    section.scrollIntoView({ behavior: "smooth", block: "start" });
                });

                li.appendChild(a);
                tocList.appendChild(li);
            });

            const observerOptions = { root: null, rootMargin: "-10% 0px -70% 0px", threshold: 0 };
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const targetId = entry.target.id;
                        document.querySelectorAll(".toc-item").forEach((item) => {
                            if (item.getAttribute("data-target") === targetId) {
                                item.classList.add("active");
                            } else {
                                item.classList.remove("active");
                            }
                        });
                    }
                });
            }, observerOptions);

            sections.forEach((section) => observer.observe(section));

            searchInput.addEventListener("input", (e) => {
                const query = e.target.value.toLowerCase().trim();
                sections.forEach((section) => {
                    const sectionText = section.textContent.toLowerCase();
                    const targetTOCItem = document.querySelector(".toc-item[data-target='" + section.id + "']");
                    
                    if (query === "" || sectionText.includes(query)) {
                        section.style.display = "block";
                        if (targetTOCItem) targetTOCItem.style.display = "block";
                    } else {
                        section.style.display = "none";
                        if (targetTOCItem) targetTOCItem.style.display = "none";
                    }
                });
            });

            const preBlocks = document.querySelectorAll("pre");
            preBlocks.forEach((pre) => {
                const code = pre.querySelector("code");
                if (!code) return;

                const wrapper = document.createElement("div");
                wrapper.className = "code-block-wrapper";
                pre.parentNode.insertBefore(wrapper, pre);

                const header = document.createElement("div");
                header.className = "code-block-header";

                let lang = "TEXT";
                code.classList.forEach((cls) => {
                    if (cls.startsWith("language-")) {
                        lang = cls.replace("language-", "").toUpperCase();
                    }
                });

                const langTag = document.createElement("span");
                langTag.textContent = lang;

                const copyBtn = document.createElement("button");
                copyBtn.className = "copy-btn";
                copyBtn.innerHTML = `
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    <span>Copy</span>
                `;

                copyBtn.addEventListener("click", () => {
                    navigator.clipboard.writeText(code.textContent).then(() => {
                        copyBtn.querySelector("span").textContent = "Copied!";
                        setTimeout(() => { copyBtn.querySelector("span").textContent = "Copy"; }, 2000);
                    });
                });

                header.appendChild(langTag);
                header.appendChild(copyBtn);
                wrapper.appendChild(header);
                wrapper.appendChild(pre);
            });
        });
    </script>
</body>
</html>
"""

def generate_archive(md_file_path, output_html_path):
    if not os.path.exists(md_file_path):
        print(f"Error: Source markdown file '{md_file_path}' not found.")
        return

    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Fallback to file name if no explicit markdown header title is present
    title = "AI Studio Local Archive"
    first_line = md_content.split('\n')[0].strip()
    if first_line.startswith('# '):
        title = first_line.lstrip('# ')
        md_content = '\n'.join(md_content.split('\n')[1:])

    # Use markdown module to render html markup
    html_raw = markdown.markdown(
        md_content, 
        extensions=['fenced_code', 'tables', 'sane_lists']
    )

    # Wrap parent semantic elements into logical sections for layout cards
    html_processed = ""
    sections_list = re.split(r'(<h2>|<h3>|<hr\s*/?>)', html_raw)
    
    section_counter = 1
    current_section = ""
    
    for segment in sections_list:
        if segment in ['<h2>', '<h3>', '<hr>', '<hr />']:
            if current_section.strip():
                html_processed += f'<div class="archive-section" id="section-{section_counter}">{current_section}</div>'
                section_counter += 1
                current_section = ""
            if segment == '<h2>':
                current_section += "<h2>"
            elif segment == '<h3>':
                current_section += "<h3>"
            elif segment.startswith('<hr'):
                html_processed += '<hr class="section-divider">'
        else:
            current_section += segment

    if current_section.strip():
        html_processed += f'<div class="archive-section" id="section-{section_counter}">{current_section}</div>'

    # Format inline mathematical elements
    html_processed = re.sub(r'\$([^$]+)\$', r'<span class="math-expr">\1</span>', html_processed)

    # Replace with template tags
    final_html = HTML_TEMPLATE.replace("{{TITLE}}", title).replace("{{BODY}}", html_processed)

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Successfully processed archive: '{output_html_path}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_archive.py <input.md> [output.html]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.rsplit('.', 1)[0] + '.html'
    generate_archive(input_file, output_file)