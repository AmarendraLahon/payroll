#!/usr/bin/env python3
"""Convert the AAU IUMS proposal markdown docs to self-contained HTML.
Faithful markdown render + a clean AAU-branded stylesheet (green/gold),
styled tables and callout-style blockquotes. One .html per .md."""

import re
from pathlib import Path
import markdown

HERE = Path(__file__).parent

DOCS = [
    "00_Roadmap_Options_Overview.md",
    "Roadmap_1_Payroll_Integration.md",
    "Roadmap_2_Payroll_HRMS.md",
    "Roadmap_3_Payroll_HRMS_Finance.md",
    "AI_Assist_Enhancement.md",
]

CSS = """
:root{
  --green:#1b5e20; --green2:#2e7d32; --green3:#43a047;
  --accent:#f9a825; --ink:#1c2b21; --soft:#f3f7f3;
  --muted:#5a6a5a; --line:#dde8dd;
}
*{ box-sizing:border-box; }
body{
  margin:0; background:#fafdfa; color:var(--ink);
  font-family:"Segoe UI",Helvetica,Arial,sans-serif; line-height:1.55;
  padding:32px 18px 80px;
}
.page{ max-width:920px; margin:0 auto; background:#fff; border:1px solid #e6efe6;
  border-radius:12px; padding:38px 46px 52px; box-shadow:0 2px 14px rgba(27,94,32,.06); }
h1{ color:var(--green); font-size:28px; line-height:1.2; letter-spacing:-.5px;
  margin:.1em 0 .5em; border-bottom:3px solid var(--accent); padding-bottom:.35em; }
h2{ color:var(--green); font-size:20px; margin:1.9em 0 .6em;
  border-bottom:2px solid #e0ece0; padding-bottom:.25em; }
h3{ color:var(--green2); font-size:16px; margin:1.5em 0 .5em; }
p,li{ font-size:14.5px; }
a{ color:var(--green2); }
strong{ color:var(--green); }
em{ color:var(--green2); font-style:italic; }
code{ background:#eef4ee; border:1px solid #dce8dc; border-radius:4px;
  padding:.08em .4em; font-family:Consolas,"Courier New",monospace; font-size:.88em; color:#37474f; }
pre{ background:#10240f; color:#d7f0d0; border-radius:8px; padding:16px 18px;
  overflow:auto; font-size:13px; line-height:1.5; }
pre code{ background:none; border:none; color:inherit; padding:0; font-size:13px; }
hr{ border:none; border-top:1px solid var(--line); margin:2em 0; }
ul,ol{ padding-left:24px; }
li{ margin:.28em 0; }
blockquote{
  margin:1.1em 0; padding:11px 16px; background:#fffdf5;
  border-left:5px solid var(--accent); border-radius:6px; color:#5a4a10; }
blockquote p{ margin:.35em 0; color:#4a3d0e; }
blockquote strong{ color:var(--green); }
blockquote code{ background:#fdf3d4; border-color:#f0e2a8; }
table{ border-collapse:collapse; width:100%; margin:1.1em 0; font-size:13px; }
th{ background:var(--green); color:#fff; text-align:left; padding:8px 10px; font-weight:600; font-size:12.5px; }
td{ padding:7px 10px; border-bottom:1px solid var(--line); vertical-align:top; }
tr:nth-child(even) td{ background:#f6faf6; }
table code{ font-size:.85em; }
.docmeta{ color:var(--muted); font-size:12.5px; }
.footer-note{ color:#8a9a8a; font-size:11.5px; text-align:center; margin-top:40px;
  border-top:1px solid #e0ece0; padding-top:14px; }
@media print{
  body{ background:#fff; padding:0; }
  .page{ border:none; box-shadow:none; border-radius:0; padding:0; }
  table,blockquote,pre{ break-inside:avoid; }
  h2{ break-after:avoid; }
}
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="page">
{body}
</div>
</body>
</html>
"""


def title_from(md_text, fallback):
    m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def convert(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"],
        output_format="html5",
    )
    title = title_from(text, md_path.stem)
    out = PAGE.format(title=title, css=CSS, body=html_body)
    out_path = md_path.with_suffix(".html")
    out_path.write_text(out, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    for name in DOCS:
        p = HERE / name
        if not p.exists():
            print(f"SKIP (missing): {name}")
            continue
        outp = convert(p)
        print(f"OK: {name} -> {outp.name}")
