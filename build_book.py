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
    # Convert header levels so everything becomes a single-page structure
    # # -> # (Keep title as is)
    # ## -> ###
    # This assumes only the first file has a level 1 header.
    # For others, we increment header depth.
    
    # Simple GitHub Alert Conversion
    text = re.sub(r'> \[!NOTE\]\s*(.*?)(?=\n\n|\n>|\Z)', r'<div class="alert alert-note">\1</div>', text, flags=re.DOTALL)
    text = re.sub(r'> \[!TIP\]\s*(.*?)(?=\n\n|\n>|\Z)', r'<div class="alert alert-tip">\1</div>', text, flags=re.DOTALL)
    text = re.sub(r'> \[!IMPORTANT\]\s*(.*?)(?=\n\n|\n>|\Z)', r'<div class="alert alert-important">\1</div>', text, flags=re.DOTALL)
    text = re.sub(r'> \[!WARNING\]\s*(.*?)(?=\n\n|\n>|\Z)', r'<div class="alert alert-warning">\1</div>', text, flags=re.DOTALL)

    return text

def build():
    print("Combining markdown files...")
    combined_content = ""
    for i, f in enumerate(FILES):
        if Path(f).exists():
            content = Path(f).read_text(encoding="utf-8")
            if i > 0:
                # Increment all headers by 1 level
                content = re.sub(r'^(#+)', r'#\1', content, flags=re.MULTILINE)
            
            combined_content += f"\n\n<!-- FILE: {f} -->\n\n" + content + "\n\n---\n\n"
    
    combined_content = preprocess_content(combined_content)
    
    # Handle mermaid code blocks
    combined_content = combined_content.replace("```mermaid", '<pre class="mermaid">').replace("```\n", "</pre>\n")

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
