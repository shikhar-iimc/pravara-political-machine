# Pravara: the sugar-bank-party network

An interactive companion to the Politics of Development essay. It maps how ownership,
control and credit overlap in the Pravara cooperative sugar factory, lets you switch
the political period to watch the machine stay fixed while the party label moves, and
highlights the capture loop on demand.

## Files

- `app.py` — the Streamlit application
- `data.py` — schematic network nodes, edges, the 2021 board roster, and sources
- `data/frp_statement_a_2025_26.csv` — the full 206-mill Statement A dataset (season 2025-26,
  as on 28 Feb 2026), cleaned from the Sugar Commissionerate's scanned PDF
- `data/frp_statement_a_2025_26.xlsx` — the same data as a formatted workbook, with a notes
  sheet describing the cleanup
- `graph_html.py` — builds the vis-network graph as self-contained HTML
- `.streamlit/config.toml` — pins a light theme so the look holds under dark mode
- `requirements.txt` — dependencies

## Run locally (optional)

```
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL it prints (usually http://localhost:8501).

## Deploy on Streamlit Community Cloud

1. Create a new public GitHub repository and add every file in this folder,
   keeping the `.streamlit/config.toml` path intact.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click New app, pick the repository and branch, and set the main file to `app.py`.
4. Click Deploy. The first build takes a minute or two.
5. Streamlit gives you a public URL. Paste that into the essay appendix in place of
   the bracketed placeholder.

## Notes on appearance

The theme is pinned to a white background with dark text in two places at once:
the Streamlit config, and inline CSS inside both the app and the graph HTML. This is
deliberate, so the page looks the same whether or not a reader has dark mode on, and
so hover tooltips never blend into the background.

## Notes on the data

Everything is a schematic reconstruction from the public sources listed in the app.
The graph shows the structure of control, not a complete census of every relationship.
The 2017 bank loan is shown to illustrate the interlock between factory boards and
their financing banks; it was a loan to a Vikhe Patil sugarcane venture, not
necessarily to the Pravara factory itself.
