# Pravara: the sugar-bank-party network

An interactive companion to the Politics of Development essay. It maps how ownership,
control and credit overlap in the Pravara cooperative sugar factory, lets you switch
the political period to watch the machine stay fixed while the party label moves, and
highlights the capture loop on demand.

## Files

- `app.py` — the Streamlit application
- `data.py` — all nodes, edges, the 2021 board roster, and sources
- `graph_html.py` — builds the vis-network graph as self-contained HTML
- `.streamlit/config.toml` — pins a light theme so the look holds under dark mode
- `requirements.txt` — dependencies

## Run locally (optional)

```
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL it prints (usually http://localhost:8501).

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
