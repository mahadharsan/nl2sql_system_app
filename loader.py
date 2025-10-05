import pandas as pd
import yaml
from sqlalchemy import create_engine

def load_file(file, sheet_name=None):
    """Load CSV, Excel, JSON, Parquet, Feather, HDF5, Stata, SAS, XML, YAML,
    or compressed files into a pandas DataFrame."""
    name = file.name.lower()
    
    if name.endswith(".csv"):
        df = pd.read_csv(file)
    elif name.endswith(".tsv"):
        df = pd.read_csv(file, sep="\t")
    elif name.endswith((".xls", ".xlsx", ".ods")):
        df = pd.read_excel(file, sheet_name=sheet_name)
    elif name.endswith(".json"):
        df = pd.read_json(file)
    elif name.endswith(".parquet"):
        df = pd.read_parquet(file)
    elif name.endswith(".feather"):
        df = pd.read_feather(file)
    elif name.endswith(".h5"):
        df = pd.read_hdf(file)
    elif name.endswith(".dta"):
        df = pd.read_stata(file)
    elif name.endswith(".sas7bdat"):
        df = pd.read_sas(file)
    elif name.endswith(".xml"):
        df = pd.read_xml(file)
    elif name.endswith((".yaml", ".yml")):
        df = pd.DataFrame(yaml.safe_load(file))
    elif name.endswith(".zip"):
        df = pd.read_csv(file, compression="zip")
    elif name.endswith(".gz"):
        df = pd.read_csv(file, compression="gzip")
    elif name.endswith(".bz2"):
        df = pd.read_csv(file, compression="bz2")
    elif name.endswith(".xz"):
        df = pd.read_csv(file, compression="xz")
    else:
        raise ValueError(f"Unsupported file type: {file.name}")
    
    return df

def df_to_sqlite(df):
    """Convert a DataFrame to an in-memory SQLite database"""
    engine = create_engine("sqlite:///:memory:")
    df.to_sql("data", engine, index=False, if_exists="replace")
    return engine
