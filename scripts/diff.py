"""Side-by-side HTML diff of an Edit or Rewrite run. Stdlib only.

    python3 scripts/diff.py post.md post_v2.md [out.html]
    open diff.html          # xdg-open on Linux, start on Windows

Writes ./diff.html unless a third argument says otherwise, and prints the path
it wrote. Nothing opens it for you.

For most reviewing, `git diff --no-index --word-diff` is better: every change
lands on one line as [-old-]{+new+} and a hundred of them scan in seconds. This
is for when you want the whole document side by side, or a page to hand to
somebody.
"""

import difflib
import html
import re
import sys
from pathlib import Path

# difflib emits an unstyled table. The classes it sets are diff_add, diff_chg
# and diff_sub on changed spans, and diff_header on the line-number gutters.
CSS = """
:root { color-scheme: light dark;
  --bg:#fff; --fg:#1a1a1a; --rule:#dcdcdc; --gutter:#9a9a9a;
  --add:#d7f0d7; --sub:#fadcdc; --chg:#fdf0c4; --head:#f4f4f5; }
@media (prefers-color-scheme: dark) { :root {
  --bg:#16181c; --fg:#e6e6e6; --rule:#2f333a; --gutter:#6b7280;
  --add:#1f3a24; --sub:#432024; --chg:#443a15; --head:#20232a; } }
body { background:var(--bg); color:var(--fg); margin:0;
  padding:1.5rem 1.25rem 4rem;
  font:13px/1.6 ui-monospace, SFMono-Regular, Menlo, monospace; }
h1 { font:600 15px/1.4 ui-sans-serif, system-ui, sans-serif; margin:0 0 1rem; }
h1 span { font-weight:400; color:var(--gutter); }

table.diff { border-collapse:collapse; width:100%; table-layout:fixed; }
table.diff td { padding:1px .6rem; vertical-align:top;
  white-space:pre-wrap; overflow-wrap:break-word; }
table.diff td.diff_header + td { border-right:1px solid var(--rule); }

.diff_header { width:3.2em; color:var(--gutter); text-align:right;
  user-select:none; background:var(--head); border-right:1px solid var(--rule);
  padding:0 .5rem; }

.diff_add { background:var(--add); }
.diff_sub { background:var(--sub); }
.diff_chg { background:var(--chg); }

thead th { position:sticky; top:0; z-index:1; text-align:left;
  padding:.45rem .6rem; background:var(--head); color:var(--fg);
  border-bottom:1px solid var(--rule); font-weight:600; }
"""


def build_table(src_lines, out_lines, src_name, out_name):
    """difflib's table, reshaped into four columns that actually lay out."""
    # No wrapcolumn: difflib hard-wraps mid-word and litters the result with
    # continuation markers. CSS wraps at word boundaries instead.
    # context=False so the whole document is there to scroll, not just the
    # changed spans with everything between them collapsed away.
    table = difflib.HtmlDiff().make_table(
        src_lines, out_lines, src_name, out_name, context=False
    )

    # Six columns come out: [nav][lineno][text] per side, where nav holds the
    # jump-to-next-change links. Those are pointless once the whole file is
    # shown, and they will not collapse to zero width, so drop the cells. The
    # header's colspan="2" still covers lineno+text, leaving four columns.
    #
    # [^>]* is load-bearing: difflib puts an id on the nav cell at each change
    # boundary, so a pattern assuming the tag ends right after the class leaves
    # exactly those rows with a fifth cell, shifting every column after it. The
    # damage then appears only at changed lines, which is the confusing part.
    table = re.sub(r'<t[dh] class="diff_next"[^>]*>.*?</t[dh]>', "", table)

    # Widths must be percentages. calc() inside a <colgroup> is not resolved by
    # every engine, and a column that cannot resolve its width collapses to
    # nothing — one character per line, which is what it looks like when wrong.
    for width in ("4%", "46%", "4%", "46%"):
        table = table.replace(
            "<colgroup></colgroup>", f'<colgroup style="width:{width}"></colgroup>', 1
        )
    table = table.replace("<colgroup></colgroup>", "")  # the two now unused

    # nowrap on every text cell defeats wrapping in a fixed-layout table.
    return table.replace(' nowrap="nowrap"', "")


def check_columns(table):
    """Every row must be four cells, or the two colspan cells of the header.

    This is the invariant the reshaping above can silently break, and the one
    that took a screenshot to notice: rows keep an extra cell, text lands one
    column right, and it only shows at changed lines.
    """
    for row in re.findall(r"<tr>(.*?)</tr>", table, re.S):
        cells = len(re.findall(r"<t[dh][ >]", row))
        if cells not in (2, 4):
            raise AssertionError(
                f"row has {cells} cells, expected 4 (or 2 in the header): {row[:120]}"
            )


def render(src, out, dest):
    table = build_table(
        src.read_text().splitlines(), out.read_text().splitlines(), src.name, out.name
    )
    check_columns(table)

    changed = sum(table.count(c) for c in ("diff_chg", "diff_add", "diff_sub"))
    src_name, out_name = html.escape(src.name), html.escape(out.name)
    dest.write_text(
        f"<!doctype html><meta charset=utf-8><title>{src_name} diff</title>"
        f"<style>{CSS}</style>"
        f"<h1>{src_name} <span>&rarr;</span> {out_name} "
        f"<span>&mdash; {changed} changed spans</span></h1>{table}"
    )
    return changed


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    src, out = Path(argv[1]), Path(argv[2])
    dest = Path(argv[3]) if len(argv) > 3 else Path("diff.html")
    changed = render(src, out, dest)
    print(f"{dest} ({dest.stat().st_size:,} bytes, {changed} changed spans)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
