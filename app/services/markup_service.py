import re

from markupsafe import escape

_HEADING_RE = re.compile(r"^\s*<(\d+)>\s*(.*)$")
_EXTERNAL_LINK_RE = re.compile(r"\[([^\s\]]+)(?:\s+([^\]]+))?\]")
_INTERNAL_LINK_RE = re.compile(r"/([^/\n]+?)/")


def _linkify(raw_text):
    placeholders = []

    def _stash(html):
        token = f"\x00{len(placeholders)}\x00"
        placeholders.append(html)
        return token

    def _external_sub(match):
        url = match.group(1)
        label = (match.group(2) or url).strip()
        href = url if re.match(r"^https?://", url) else f"https://{url}"
        safe_href = str(escape(href))
        safe_label = str(escape(label))
        return _stash(f'<a href="{safe_href}" target="_blank" rel="noopener noreferrer">{safe_label}</a>')

    without_external = _EXTERNAL_LINK_RE.sub(_external_sub, raw_text)

    def _internal_sub(match):
        slug = match.group(1).strip()
        safe_slug = str(escape(slug))
        return _stash(f'<a href="/wiki/{safe_slug}">{safe_slug}</a>')

    without_links = _INTERNAL_LINK_RE.sub(_internal_sub, without_external)

    escaped = str(escape(without_links))
    for i, html in enumerate(placeholders):
        escaped = escaped.replace(f"\x00{i}\x00", html)

    return escaped


def to_html(content):
    lines = (content or "").split("\n")
    rendered_lines = []

    for line in lines:
        heading_match = _HEADING_RE.match(line)
        if heading_match:
            level = max(1, min(6, int(heading_match.group(1))))
            text = heading_match.group(2)
            rendered_lines.append(f"<h{level}>{_linkify(text)}</h{level}>")
        else:
            rendered_lines.append(_linkify(line))

    return "<br>\n".join(rendered_lines)


def to_plain_text(content):
    lines = (content or "").split("\n")
    stripped_lines = []

    for line in lines:
        heading_match = _HEADING_RE.match(line)
        stripped_lines.append(heading_match.group(2) if heading_match else line)

    text = "\n".join(stripped_lines)
    text = _EXTERNAL_LINK_RE.sub(lambda m: (m.group(2) or m.group(1)).strip(), text)
    text = _INTERNAL_LINK_RE.sub(lambda m: m.group(1).strip(), text)
    return re.sub(r"\s+", " ", text).strip()
