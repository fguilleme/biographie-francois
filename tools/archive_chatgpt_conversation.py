#!/usr/bin/env python3
"""Extract one ChatGPT export conversation as raw JSON and readable Markdown."""

import argparse
import datetime as dt
import json
from pathlib import Path


def format_time(value):
    if not value:
        return "date inconnue"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def render_content(message):
    content = message.get("content") or {}
    parts = content.get("parts") or []
    rendered = []
    for part in parts:
        if isinstance(part, str):
            rendered.append(part)
        else:
            rendered.append("```json\n" + json.dumps(part, ensure_ascii=False, indent=2) + "\n```")
    if not rendered and content:
        rendered.append("```json\n" + json.dumps(content, ensure_ascii=False, indent=2) + "\n```")
    return "\n\n".join(rendered).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("conversation_id")
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    conversations = json.loads(args.source.read_text(encoding="utf-8"))
    conversation = next((c for c in conversations if c.get("id") == args.conversation_id), None)
    if conversation is None:
        raise SystemExit(f"Conversation introuvable : {args.conversation_id}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = args.output_dir / "biographie-conversation-complete-raw.json"
    md_path = args.output_dir / "biographie-conversation-complete.md"
    raw_path.write_text(json.dumps(conversation, ensure_ascii=False, indent=2), encoding="utf-8")

    mapping = conversation.get("mapping") or {}
    node_id = conversation.get("current_node")
    active_path = []
    seen = set()
    while node_id and node_id not in seen:
        seen.add(node_id)
        node = mapping.get(node_id)
        if not node:
            break
        active_path.append(node)
        node_id = node.get("parent")
    active_path.reverse()

    messages = [n.get("message") for n in active_path if n.get("message")]
    lines = [
        "# Conversation ChatGPT complète — Biographie",
        "",
        f"- Identifiant : `{conversation.get('id')}`",
        f"- Titre : **{conversation.get('title', '')}**",
        f"- Création : {format_time(conversation.get('create_time'))}",
        f"- Dernière mise à jour : {format_time(conversation.get('update_time'))}",
        f"- Messages du fil actif : {len(messages)}",
        f"- Nœuds conservés dans l’archive JSON (branches comprises) : {len(mapping)}",
        "- Source : export officiel ChatGPT reçu le 13 juillet 2026",
        "",
        "Le fichier JSON voisin conserve la structure originale complète, y compris les branches et métadonnées.",
        "",
        "---",
        "",
    ]
    role_names = {"user": "Utilisateur", "assistant": "Assistant", "system": "Système", "tool": "Outil"}
    for index, message in enumerate(messages, 1):
        author = (message.get("author") or {}).get("role", "inconnu")
        name = (message.get("author") or {}).get("name")
        heading = role_names.get(author, author.capitalize())
        if name:
            heading += f" — {name}"
        lines.extend([
            f"## {index}. {heading}",
            "",
            f"*{format_time(message.get('create_time'))}*",
            "",
            render_content(message) or "*[Message sans contenu textuel]*",
            "",
        ])
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "markdown": str(md_path),
        "raw_json": str(raw_path),
        "messages": len(messages),
        "nodes": len(mapping),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
