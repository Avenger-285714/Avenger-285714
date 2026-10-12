#!/usr/bin/env python3
"""Fetch WakaTime languages JSON and render a pie chart SVG."""

import json
import sys
import urllib.request

import pygal
from pygal.style import Style

JSON_URL = (
    "https://wakatime.com/share/@9f5ee620-d071-4a5e-b45d-a89f7722ae0f/"
    "8cdeb3e2-5de2-494a-9b87-6bdfc0bf9509.json"
)
OUTPUT = "assets/wakatime-languages.svg"
MAX_LANGUAGES = 15


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def render_svg(data: dict, output: str) -> None:
    items = [x for x in data["data"] if x["percent"] > 0][:MAX_LANGUAGES]

    style = Style(
        background="transparent",
        plot_background="transparent",
        foreground="#333",
        foreground_strong="#333",
        foreground_subtle="#666",
        colors=tuple(x["color"] for x in items),
        title_font_size=16,
        label_font_size=12,
        legend_font_size=12,
        value_font_size=12,
    )

    pie = pygal.Pie(
        style=style,
        inner_radius=0.5,
        show_legend=True,
        legend_box_size=12,
        print_values=True,
        print_values_position="top",
        value_formatter=lambda x: f"{x}%",
        truncate_legend=-1,
        width=800,
        height=500,
        explicit_size=True,
    )

    pie.title = "Languages over All Time (Powered by wakatime.com)"
    for x in items:
        pie.add(f"{x['name']} ({x['percent']}%)", x["percent"])

    pie.render_to_file(output)
    print(f"Wrote {output}")


def main() -> int:
    try:
        data = fetch_json(JSON_URL)
    except Exception as e:
        print(f"Failed to fetch WakaTime JSON: {e}", file=sys.stderr)
        return 1

    render_svg(data, OUTPUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
