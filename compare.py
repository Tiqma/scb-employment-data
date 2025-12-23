import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

from analys import nice_step 

def compare(sektor, kon, years):
    try:
        df_raw = pd.read_csv('data.csv', 
                             names=['kommun', 'totalt', 'period', 'mått', 'värde'],
                             encoding='utf-8')
    except FileNotFoundError:
        print("Filen data.csv hittades inte.")
        return None

    all_data = []

    for year in years:
        mask = (
            (df_raw['kommun'] == sektor) & 
            (df_raw['totalt'] == kon) & 
            (df_raw['mått'] == "Antal pågående anställningar") & 
            (df_raw['period'].astype(str).str.startswith(str(year)))
        )
        
        df_year = df_raw[mask].copy()
        
        df_year['värde'] = pd.to_numeric(df_year['värde'], errors='coerce')

        try:
            df_year['month_int'] = df_year['period'].astype(str).str[-2:].astype(int)
        except ValueError:
            df_year['month_int'] = range(1, len(df_year) + 1)
            
        df_year['year_label'] = year
        all_data.append(df_year)

    if not all_data:
        print("Ingen data hittades.")
        return None
        
    full_df = pd.concat(all_data)
    
    y_min = int(full_df['värde'].min())
    y_max = int(full_df['värde'].max())

    if y_max == y_min:
        raw_step = 100
    else:
        raw_step = (y_max - y_min) / 6

    step = nice_step(raw_step)

    y_start = (y_min // step) * step
    y_end = ((y_max // step) + 1) * step
    positions = list(range(int(y_start), int(y_end) + int(step), int(step)))

    manader = ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun", 
               "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]
    
    fig, ax = plt.subplots(figsize=(10, 6))

    for df_year in all_data:
        label = df_year['year_label'].iloc[0]

        ax.plot(df_year['month_int'] - 1, df_year['värde'], marker='o', label=label)

    ax.set_title(f'Antal pågående anställningar – {sektor}, {kon}')
    ax.set_ylabel('Antal', rotation=0, labelpad=30)

    ax.set_xticks(range(12))
    ax.set_xticklabels(manader, rotation=45)
    ax.set_xlim(-0.5, 11.5)
    
    ax.set_yticks(positions)
    ax.set_yticklabels([f"{y:,}".replace(',', ' ') for y in positions])
    
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    plt.close(fig)
    return buf
