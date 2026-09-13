import json
from pathlib import Path


DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

COLORS = [
    "#161B22",
    "#0E4429",
    "#006D32",
    "#26A641",
    "#39D353"
]

CELL_SIZE = 12
GAP = 3

LEFT = 35
TOP = 45

WIDTH = 850
HEIGHT = 175


def load_data():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def create_heatmap(data):

    days = data.get("days", [])

    # Keep the latest 364 days
    days = days[-364:]

    svg = []

    svg.append(
        f'''<svg
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}"
        xmlns="http://www.w3.org/2000/svg">'''
    )

    # Background
    svg.append(
        f'''
        <rect
            width="{WIDTH}"
            height="{HEIGHT}"
            rx="18"
            fill="#0B1120"
            stroke="#00BFFF"
            stroke-width="1"/>
        '''
    )

    # Terminal title
    svg.append(
        '''
        <text
            x="30"
            y="27"
            fill="#00BFFF"
            font-family="monospace"
            font-size="14">
            harshi@github ~ $ contributions
        </text>
        '''
    )

    # Contribution boxes
    for index, day in enumerate(days):

        week = index // 7
        weekday = index % 7

        x = LEFT + week * (
            CELL_SIZE + GAP
        )

        y = TOP + weekday * (
            CELL_SIZE + GAP
        )

        level = int(
            day.get("level", 0)
        )

        level = max(
            0,
            min(level, 4)
        )

        color = COLORS[level]

        delay = index * 0.003

        svg.append(
            f'''
            <rect
                x="{x}"
                y="{y}"
                width="{CELL_SIZE}"
                height="{CELL_SIZE}"
                rx="3"
                fill="{color}"
                opacity="0">

                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    begin="{delay:.3f}s"
                    dur="0.25s"
                    fill="freeze"/>

            </rect>
            '''
        )

    # Legend
    svg.append(
        '''
        <text
            x="35"
            y="165"
            fill="#64748B"
            font-family="monospace"
            font-size="11">
            Less
        </text>
        '''
    )

    for index, color in enumerate(COLORS):

        x = 70 + index * 18

        svg.append(
            f'''
            <rect
                x="{x}"
                y="155"
                width="12"
                height="12"
                rx="3"
                fill="{color}"/>
            '''
        )

    svg.append(
        '''
        <text
            x="165"
            y="165"
            fill="#64748B"
            font-family="monospace"
            font-size="11">
            More
        </text>
        '''
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    print("Creating contribution heatmap...")

    data = load_data()

    svg = create_heatmap(data)

    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print(
        "contrib-heatmap.svg created successfully!"
    )


if __name__ == "__main__":
    main()
