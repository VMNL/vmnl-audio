# Markdown style

This style applies to maintained Markdown in both `vmnl-audio` and `vmnl-graphics`, including README
files, guides, API reference pages, contribution rules and agent documentation. Each repository
keeps a copy of this guide so that it can be read independently.

## Content preservation

A formatting change preserves wording, language, punctuation, section order, heading levels, list
order and nesting, link labels and destinations, images, and table cell contents. Do not translate,
rewrite, rename files or headings, or update technical claims while formatting.

Keep code examples, commands, fence language annotations, HTML blocks and YAML front matter
unchanged. Preserve explicit line breaks: two trailing spaces or a backslash can be meaningful.

## Headings and spacing

- Use ATX headings (`#`, `##`, `###`) with a space before the title.
- Keep existing heading text and levels so that section links remain valid.
- Separate top-level headings, paragraphs, lists, fenced code blocks and tables with one blank line.
- Use one blank line between ordinary text blocks; avoid consecutive empty lines outside literal
  content such as code, HTML and front matter.
- Use UTF-8 text, LF line endings and exactly one final newline.
- Remove trailing whitespace except the two spaces used for an explicit Markdown line break.

## Paragraphs and lists

Wrap ordinary prose at 100 columns, including list indentation. A source newline within a paragraph
is a soft break; it does not start a new paragraph. Keep inline code spans intact.

Long URLs and other indivisible tokens may exceed 100 columns. Tables, headings, code blocks, HTML,
front matter, image paragraphs, blockquotes and paragraphs with explicit hard breaks are exempt from
prose wrapping.

Use `- ` for unordered list items and `1.`, `2.`, etc. for ordered steps. Align continuation lines
with the first character of the item's text. Preserve existing nesting and item numbers.

```markdown
- First item with a continuation that remains part of the same item.
  Continuation text starts under the first character of the item.
- Second item.

1. First step.
2. Second step.
```

## Tables

Use a leading and trailing pipe, one space around each cell, and three hyphens in separator cells.
Preserve alignment colons and escaped pipes. Keep each row on one source line; padding columns to
the width of their longest cell is unnecessary.

```markdown
| Name | Meaning |
| --- | --- |
| `value` | Existing description |
```

## Links and code

Use relative links for local documentation. Keep existing destinations and fragments unchanged
during formatting. Keep inline code between backticks, and retain fenced and indented code exactly
as written. Formatting prose must not change a command or Rust example.

## Generated files

Files beginning with a generated-file notice are exempt from manual formatting. Their generator owns
their layout; run an update only when the underlying inventory intentionally changes. This includes
API snapshots, symbol and method indexes, and the graphics GLFW inventory and window compatibility
matrix. Build outputs and third-party documentation are outside this scope.

## Reviewing a formatting change

Compare the Markdown structure and inline content before and after formatting. Text may differ only
in soft whitespace; headings, lists, links, images, table contents and literal blocks must retain
their meaning and order. Check that formatting a second time produces no further changes.

Check local links and anchors, and verify that generated files and code examples remain unchanged.
Follow [the contribution guide](../CONTRIBUTING.md#before-submission) for applicable documentation
checks. A formatting-only change does not require runtime or hardware validation.
