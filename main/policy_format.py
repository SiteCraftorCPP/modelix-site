"""Преобразование текста политики (.txt) в HTML.

Строки вида «-- 1 of 12 --» (метки страниц при экспорте из PDF) выкидываются.
Пункты, начинающиеся с «- », верстаются абзацами с тем же дефисом, без маркеров <ul>.
"""
from __future__ import annotations

import re

from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe

PAGE_MARKER = re.compile(r"^\s*--\s*\d+\s+of\s+\d+\s*--\s*$", re.I)
SUB_CLAUSE = re.compile(r"^(?P<num>\d+(?:\.\d+)+\.)\s+(?P<body>.*)$")
MAJOR_SECTION = re.compile(r"^[1-9]\.(?!\d)\s+.+$")

_TITLE_JOIN = "\u241e"


def _normalize(raw: str) -> list[str]:
    # Только типичные склейки из PDF, без правки юридической формулировки из файла.
    raw = raw.replace("IP-\nадрес", "IP-адрес")
    raw = raw.replace("IPадрес", "IP-адрес")
    lines: list[str] = []
    for ln in raw.splitlines():
        s = ln.strip()
        if not s or PAGE_MARKER.match(s):
            continue
        lines.append(s)
    return lines


def _starts_new_structural(line: str) -> bool:
    s = line.strip()
    # Шапка документа — каждая строка отдельно (иначе склеивается в один абзац).
    if s.startswith("ИП "):
        return True
    if s.startswith("Настоящую Политику"):
        return True
    if s == "УТВЕРЖДАЮ":
        return True
    if s.startswith("г.") and "Петербург" in s:
        return True
    if re.match(r'^"\d+"\s+апреля', s):
        return True
    if SUB_CLAUSE.match(line):
        return True
    if MAJOR_SECTION.match(line):
        return True
    if line.startswith("- "):
        return True
    if line.startswith("вариант:"):
        return True
    if line.startswith(("Пользователь -", "Сервисы Сайта -")):
        return True
    if line.startswith("Оператор и Пользователи"):
        return True
    if line.startswith("Обработке подлежат"):
        return True
    if line.startswith("Условием прекращения"):
        return True
    if line.startswith("В случае выявления неточных"):
        return True
    if line.startswith("Моральный вред"):
        return True
    if line.startswith("Новая редакция Политики применяется"):
        return True
    return False


def _should_join(prev: str, nxt: str) -> bool:
    if _starts_new_structural(nxt):
        return False
    prev_stripped = prev.rstrip()
    ends_sentence = prev_stripped.endswith((".", ";", ":", "!", "?", "»"))
    if prev.startswith("- ") and not ends_sentence:
        return True
    if nxt and nxt[0].isalpha() and nxt[0].lower() == nxt[0] and not ends_sentence:
        return True
    if not ends_sentence and nxt and nxt[0].isupper():
        if not SUB_CLAUSE.match(nxt) and not MAJOR_SECTION.match(nxt):
            return True
    return False


def _merge_soft(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        cur = lines[i]
        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if _starts_new_structural(nxt):
                break
            if _should_join(cur, nxt):
                cur = f"{cur} {nxt}"
                j += 1
            else:
                break
        out.append(cur)
        i = j
    return out


def _merge_section6_heading(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("6.") and "БЛОКИРОВАНИЕ" in ln and not ln.startswith("6.1"):
            parts = [ln]
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.startswith("6.1"):
                    break
                if SUB_CLAUSE.match(nxt) or MAJOR_SECTION.match(nxt):
                    break
                if nxt.startswith("- "):
                    break
                parts.append(nxt)
                i += 1
            out.append(_TITLE_JOIN.join(parts))
            continue
        out.append(ln)
        i += 1
    return out


def policy_text_to_html(raw: str) -> SafeString:
    lines = _normalize(raw)
    lines = _merge_soft(lines)
    lines = _merge_section6_heading(lines)

    html: list[str] = []
    i = 0

    header_chunks: list[str] = []
    while i < len(lines) and not MAJOR_SECTION.match(lines[i]):
        ln = lines[i]
        if ln.startswith("ИП "):
            header_chunks.append(
                f'<p class="policy-doc-ip"><strong>{escape(ln)}</strong></p>'
            )
        elif "Настоящую Политику" in ln:
            if i + 1 < len(lines) and lines[i + 1] == "УТВЕРЖДАЮ":
                merged = f"{ln} УТВЕРЖДАЮ"
                header_chunks.append(
                    '<p class="policy-doc-lead-approve"><strong>'
                    f"{escape(merged)}</strong></p>"
                )
                i += 2
                continue
            header_chunks.append(f'<p class="policy-doc-lead">{escape(ln)}</p>')
        elif ln == "УТВЕРЖДАЮ":
            header_chunks.append(
                '<p class="policy-doc-approve"><strong>УТВЕРЖДАЮ</strong></p>'
            )
        else:
            header_chunks.append(f'<p class="policy-doc-meta">{escape(ln)}</p>')
        i += 1

    html.append(
        '<header class="policy-doc-head">' + "".join(header_chunks) + "</header>"
    )

    while i < len(lines):
        ln = lines[i]

        if MAJOR_SECTION.match(ln):
            if _TITLE_JOIN in ln:
                inner = "<br>".join(escape(p.strip()) for p in ln.split(_TITLE_JOIN))
                html.append(f'<h2 class="policy-h2">{inner}</h2>')
            else:
                html.append(f'<h2 class="policy-h2">{escape(ln)}</h2>')
            i += 1
            continue

        if ln.startswith("- "):
            paras: list[str] = []
            while i < len(lines) and lines[i].startswith("- "):
                paras.append(
                    f'<p class="policy-dash">{escape(lines[i][2:])}</p>'
                )
                i += 1
            html.append(
                '<div class="policy-dash-block">' + "".join(paras) + "</div>"
            )
            continue

        msub = SUB_CLAUSE.match(ln)
        if msub:
            num = msub.group("num")
            body = msub.group("body")
            html.append(
                '<p class="policy-clause">'
                f'<span class="policy-num">{escape(num)}</span>'
                f'<span class="policy-clause-body">{escape(body)}</span>'
                "</p>"
            )
            i += 1
            continue

        cls = "policy-variant" if ln.startswith("вариант:") else "policy-p"
        html.append(f'<p class="{cls}">{escape(ln)}</p>')
        i += 1

    return mark_safe("\n".join(html))
