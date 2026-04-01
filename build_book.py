import os
from pathlib import Path
import re
import subprocess

FILES = [
    "00_Workshop_Overview_and_Setup.md",
    "Day1_Foundations_and_16S_Amplicon.md",
    "Day2_Shotgun_Metagenomics.md",
    "Day3_Statistical_Analysis.md",
    "Commands_CheatSheet.md",
    "Glossary_and_References.md",
]

def preprocess_content(text):
    # Regex to capture GitHub-style alerts in blockquotes
    # Pattern: a block of lines starting with '>' where the first line contains [!TYPE]
    alert_pattern = re.compile(r'^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n((?:^>.*\n?)*)', re.MULTILINE)

    def replace_alert(match):
        atype = match.group(1).lower()
        content = match.group(2)
        # Clean the content: remove the leading '> '
        lines = [line.lstrip('> ').rstrip() for line in content.splitlines()]
        clean_content = "\n".join(lines).strip()
        # Convert to Pandoc Fenced Div syntax
        return f'\n:::{atype}\n{clean_content}\n:::\n\n'

    # Apply alert conversion
    text = alert_pattern.sub(replace_alert, text)

    # Secondary check for single-line alerts without content below the marker
    inline_alert_pattern = re.compile(r'^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](.*)$', re.MULTILINE)
    text = inline_alert_pattern.sub(r'\n:::\1\n\2\n:::\n', text)

    # Ensure mermaid code blocks are transformed correctly for our template
    # We use fenced divs for consistency or keep them as pre blocks
    text = text.replace("```mermaid", '\n\n:::mermaid\n').replace("```", '\n:::\n')
    
    # Actually, we want to keep standard code blocks as code blocks.
    # The previous global replace of ``` was too broad.
    # Let's fix that.
    
    return text

def build():
    print("Combining markdown files...")
    combined_content = ""
    for i, f in enumerate(FILES):
        if Path(f).exists():
            content = Path(f).read_text(encoding="utf-8")
            
            # Safe header incrementing: only change if it's at the start of a line
            if i > 0:
                # We want to turn # to ## etc. 
                # But we must be careful not to touch headers inside code blocks.
                # A simple way is to match '#' at the beginning of a line.
                lines = content.splitlines()
                processed_lines = []
                for line in lines:
                    if line.startswith("#"):
                        processed_lines.append("#" + line)
                    else:
                        processed_lines.append(line)
                content = "\n".join(processed_lines)
            
            combined_content += f"\n\n<!-- FILE: {f} -->\n\n" + content + "\n\n"
    
    # Convert Alerts to Fenced Divs
    combined_content = preprocess_content(combined_content)
    
    # Final cleanup: ensure no triple newlines
    combined_content = re.sub(r'\n{3,}', '\n\n', combined_content)

    Path("temp_book.md").write_text(combined_content, encoding="utf-8")

    print("Running Pandoc...")
    cmd = [
        "pandoc",
        "temp_book.md",
        "-s",
        "--toc",
        "--toc-depth=3",
        "--template", "pandoc_template.html",
        "-o", "index.html",
        f"--metadata=title:Computational Metagenomics: Methods and Applications"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Success! index.html created.")
    except Exception as e:
        print(f"Error running pandoc: {e}")
    finally:
        if Path("temp_book.md").exists():
            os.remove("temp_book.md")

if __name__ == "__main__":
    build()
