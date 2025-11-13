import pandas as pd
from ydata_profiling import ProfileReport

def load_data(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df

def clean_data(df):
    # NaN qiymatlarni to‘ldirish yoki olib tashlash
    df = df.dropna(how='all')
    df = df.fillna('')
    return df

def generate_eda_report(df, output_path):
    """Avtomatik EDA hisobotini yaratadi va HTML faylga saqlaydi"""
    profile = ProfileReport(df, title="Avtomatik EDA Hisobot", explorative=True)
    profile.to_file(output_path)

