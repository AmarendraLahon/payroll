# Convert the Visit Closure Document (markdown) to a signing-ready PDF.
import sys, markdown
from xhtml2pdf import pisa

SRC = r"D:\Projects\pr\docs\Visit_Closure_Document.md"
OUT = r"D:\Projects\pr\docs\Visit_Closure_Document.pdf"

with open(SRC, encoding="utf-8") as f:
    md = f.read()

body_html = markdown.markdown(
    md,
    extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
)
# xhtml2pdf cannot size zero-content cells; give empty cells a filler so
# signature/blank columns still render with width + height.
body_html = body_html.replace("<td></td>", "<td>&nbsp;</td>").replace("<th></th>", "<th>&nbsp;</th>")

CSS = """
@page {
    size: A4;
    margin: 2.0cm 1.8cm 2.2cm 1.8cm;
    @frame footer { -pdf-frame-content: footerContent; bottom: 1.0cm; margin-left: 1.8cm; margin-right: 1.8cm; height: 1cm; }
}
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; color: #202124; line-height: 1.45; }
h1 { font-size: 19pt; color: #1a4f9c; margin: 0 0 2pt 0; }
h2 { font-size: 13pt; color: #1a4f9c; border-bottom: 1.2pt solid #1a73e8; padding-bottom: 3pt; margin-top: 16pt; margin-bottom: 6pt; }
h3 { font-size: 11pt; color: #137333; margin-top: 11pt; margin-bottom: 3pt; }
p { margin: 4pt 0; }
strong { color: #202124; }
ul, ol { margin: 4pt 0 6pt 0; }
li { margin: 2pt 0; }
hr { border: none; border-top: 0.6pt solid #cccccc; margin: 10pt 0; }
blockquote { background: #f1f3f4; border-left: 3pt solid #1a73e8; margin: 6pt 0; padding: 4pt 8pt; color: #3c4043; font-size: 10pt; }
code { font-family: Courier, monospace; font-size: 9.5pt; background: #f1f3f4; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0; }
th { background: #1a73e8; color: #ffffff; font-size: 9.5pt; padding: 4pt 5pt; text-align: left; border: 0.5pt solid #1a73e8; }
td { font-size: 9.5pt; padding: 4pt 5pt; border: 0.5pt solid #c0c4c8; vertical-align: top; }
tr:nth-child(even) td { background: #f6f8fc; }
.cover { border-bottom: 2pt solid #137333; padding-bottom: 8pt; margin-bottom: 6pt; }
.cover .co { font-size: 12pt; color: #137333; font-weight: bold; }
"""

# brand cover line above content
cover = (
    '<div class="cover"><span class="co">Bohniman Systems Private Limited (BSPL)</span></div>'
)

footer = (
    '<div id="footerContent" style="font-size:8pt; color:#5f6368; text-align:center;">'
    'Bohniman Systems Private Limited (BSPL) &nbsp;·&nbsp; AAU ERP/Payroll — Visit Closure Document '
    '&nbsp;·&nbsp; Page <pdf:pagenumber> of <pdf:pagecount></div>'
)

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{cover}{body_html}{footer}</body></html>"""

with open(OUT, "wb") as out:
    result = pisa.CreatePDF(html, dest=out, encoding="utf-8")

if result.err:
    print("FAILED", result.err); sys.exit(1)
print("SAVED", OUT)
