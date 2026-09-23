#!/usr/bin/env python3
"""Generate estate-recovery-overview.ipynb.

The notebook is generated rather than hand-edited, so the prose and the code
live in one reviewable file. Rebuild and run it with

    python3 notebooks/build_overview_notebook.py
    python3 -m nbconvert --execute --inplace notebooks/estate-recovery-overview.ipynb
"""
import pathlib
import nbformat as nbf

HERE = pathlib.Path(__file__).resolve().parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

cells = [
    md("# Medicaid estate recovery and the family home, 50 states and DC\n\n"
       "This notebook loads `data/states.csv` and reproduces the headline counts in the README. "
       "Each row is one jurisdiction. The five method columns record whether Medicaid estate recovery "
       "can reach a house passing at the recipient's death by that method."),
    code("import pandas as pd\n\n"
         "df = pd.read_csv('../data/states.csv', dtype=str, keep_default_na=False)\n"
         "METHODS = ['life_estate', 'lady_bird_deed', 'tod_deed', 'joint_tenancy', 'revocable_trust']\n"
         "len(df)"),
    md("## How far recovery reaches\n\n"
       "`probate_only` states recover only from the probate estate. `expanded` states adopted the optional "
       "federal definition that reaches property passing outside probate."),
    code("df['recovery_scope'].value_counts()"),
    md("## Treatment of the house by transfer method"),
    code("pd.DataFrame({m: df[m].value_counts() for m in METHODS}).fillna(0).astype(int).T"),
    md("## Probate-only is not the same as safe\n\n"
       "Jurisdictions that limit recovery to the probate estate but can still reach a house in a revocable "
       "trust, because the trust code makes the trust liable when the probate estate is short."),
    code("po = df[df['recovery_scope'] == 'probate_only']\n"
         "po.loc[po['revocable_trust'] == 'reachable', ['code', 'name', 'revocable_trust_cite']]"),
    md("## Transfer on death deed statutes by effective date"),
    code("tod = df[df['tod_deed_recognized'] == 'yes'][['code', 'name', 'tod_deed_effective', 'tod_deed_uniform_act', 'tod_deed']]\n"
         "tod.sort_values('tod_deed_effective')"),
    md("## Lady bird deed recognition by authority"),
    code("df[df['lady_bird_deed_recognized'] == 'yes'][['code', 'name', 'lady_bird_authority_type', 'lady_bird_deed']]"),
]

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, HERE / "estate-recovery-overview.ipynb")
print("wrote", HERE / "estate-recovery-overview.ipynb")
