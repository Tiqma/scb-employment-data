import subprocess
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO, BytesIO
import json
def graf(sektor_i, kon_i, year_i):
    sektor = sektor_i
    kon = kon_i
    year = year_i

    awk_cmd = f"""
    awk -F',' '$1=="\\"{sektor}\\"" && $2=="\\"{kon}\\"" && $3 ~ /^"{year}/ && $4=="\\"Antal pågående anställningar\\"" {{print $0}}' data.csv
    """

    result = subprocess.run(awk_cmd, shell=True, capture_output=True, text=True)
    
    df = pd.read_csv(StringIO(result.stdout), header=None, names=['kommun','totalt','period','mått','värde'], encoding='windows-1252')
    print(df)
    manader = ["Januari","Februari","Mars","April","Maj","Juni","Juli","Augusti","September"]

    y_min = int(df['värde'].min())
    y_max = int(df['värde'].max())
    positions = list(range(y_min, y_max + 5001, 5000))

    plt.figure(figsize=(10,6))
    plt.plot(df['period'], df['värde'], marker='o', linestyle='-')
    plt.title('Antal pågående anställningar 2025 – Kommun, Män')
    plt.xlabel('Månad')
    plt.ylabel('Antal pågående anställningar, 1000-tal')
    plt.xticks(df['period'], manader, rotation=45)
    plt.yticks(positions, [int(y/1000) for y in positions])
    plt.grid(True)
    plt.tight_layout()

    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df['period'], df['värde'], marker='o')
    ax.set_title('Antal pågående anställningar 2025 – Kommun, Män')
    ax.set_xlabel('Månad')
    ax.set_ylabel('Antal pågående anställningar, 1000-tal')
    ax.set_xticks(df['period'])
    ax.set_xticklabels(manader, rotation=45)
    ax.set_yticks(positions)
    ax.set_yticklabels([int(y/1000) for y in positions])
    ax.grid(True)

    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return fig

def get_options():
    with open("csv_summary.json", "r", encoding="utf-8") as f:
        innehall = json.load(f)
        return innehall
