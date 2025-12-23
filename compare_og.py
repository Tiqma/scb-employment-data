import subprocess
from unittest import result
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO, BytesIO
import json
from analys import nice_step

def compare(sektor, kon, years):

    data = []
    
    for year in years:
        awk_cmd = f"""
    awk -F',' '$1=="\\"{sektor}\\"" && $2=="\\"{kon}\\"" && $3 ~ /^"{year}/ && $4=="\\"Antal pågående anställningar\\"" {{print $0}}' data.csv
    """
        result = subprocess.run(awk_cmd, shell=True, capture_output=True, text=True)

        df = pd.read_csv(StringIO(result.stdout), header=None,
                     names=['kommun','totalt','period','mått','värde'],
                     encoding='utf-8')
        
        data.append(df)

    manader = ["Januari","Februari","Mars","April","Maj","Juni","Juli",
               "Augusti","September", "Oktober", "November", "December"]
    
    y_min = int(data['värde'].min())
    y_max = int(data['värde'].max())

    raw_step = (y_max - y_min) / 6

    step = nice_step(raw_step)

    y_start = (y_min // step) * step
    y_end = ((y_max // step) + 1) * step

    positions = list(range(y_start, y_end + step, step))

    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(data['period'], data['värde'], marker='o')
    ax.set_title(f'Antal pågående anställningar {year} – {sektor}, {kon}')
    ax.set_xlabel('Månad')
    ax.set_ylabel('Antal', rotation=0, labelpad=30)
    ax.set_xticks(df['period'])
    ax.set_xticklabels(manader, rotation=45)
    ax.set_yticks(positions)
    ax.set_yticklabels([f"{y:,}" for y in positions])
    ax.grid(True)

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return fig

x = compare("kommun", "män", ["2024", "2023"])

print(x)