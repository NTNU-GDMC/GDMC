import pandas as pd
import re
from re import compile
from pathlib import Path
import plotly.express as px

LOG_PATH = Path("log")

def readFile():
    mesg: dict[str, list] = {}
    pattern = compile(r'buildArea: (\d+) (\d+)\nround: (\d+)\nlevel: (\d+)\nGenerate Blueprint Time: ([\d.]+)', flags=re.M)
    for file in LOG_PATH.iterdir():
        with file.open("r") as f:
            content = f.read()
            match = pattern.search(content)
            if match:
                mesg.setdefault("size", []).append(int(match.group(1)))
                mesg.setdefault("round", []).append(int(match.group(3)))
                mesg.setdefault("time", []).append(float(match.group(5)))
                mesg.setdefault("level", []).append(int(match.group(4)))
    df = pd.DataFrame(mesg)

    return df


if __name__ == "__main__":
    """
        size
        time
        level
        round
    """
    df = readFile()
    relations = [
        ("size", "time"),
        ("size", "level"),
    ]
    color_discrete_sequences = [
        px.colors.qualitative.Prism,
        px.colors.qualitative.Vivid,
    ]

    for relation, color_discrete_sequence in zip(relations, color_discrete_sequences):
        xlabel, ylabel = relation
        fig = px.box(data_frame=df, x=xlabel, y=ylabel, color="size", color_discrete_sequence=color_discrete_sequence)
        fig.show()
