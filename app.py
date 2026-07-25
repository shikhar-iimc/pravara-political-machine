import json

import networkx as nx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import data
from graph_html import build_html

st.set_page_config(page_title="Pravara: the sugar-bank-party network",
                   layout="wide", initial_sidebar_state="collapsed")

# Light appearance. The real fix for dark-mode browsers lives in
# .streamlit/config.toml (base="light" + explicit colors) because that's
# what st.dataframe's canvas grid and BaseWeb widget internals (radio dot,
# toggle knob/track) actually read. CSS injected here can't reach into a
# <canvas> element, and blanket-overriding div backgrounds like the old
# version did was also stripping the fill color off the radio dot and the
# toggle knob, making them invisible even though they still worked.
# So this block is now deliberately narrow: cosmetic touches only, nothing
# that reaches into stRadio/stCheckbox/stDataFrame internals.
st.markdown(
    """
    <style>
      :root { color-scheme: only light; }

      h1, h2, h3, h4 { color: #111111 !important; font-family: Georgia, 'Times New Roman', serif !important; }

      /* captions */
      [data-testid="stCaptionContainer"] p { color: #5c5c5c !important; }

      /* tab underline / active tab color only - not backgrounds */
      [aria-selected="true"] p, [aria-selected="true"] div { color: #1f3a5f !important; }
      [data-baseweb="tab-highlight"] { background-color: #1f3a5f !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- styling helpers for nodes and edges ----------
EDGE_STYLE = {
    "family":       {"color": "#8a8a8a", "dashes": True,  "width": 1.5},
    "founding":     {"color": "#b0b0b0", "dashes": False, "width": 1.5},
    "directorship": {"color": "#1f3a5f", "dashes": False, "width": 2.5},
    "loan":         {"color": "#c07b18", "dashes": False, "width": 3.0},
    "ownership":    {"color": "#9a9a9a", "dashes": False, "width": 1.5},
    "mobilise":     {"color": "#7a7a7a", "dashes": True,  "width": 1.5},
    "votes":        {"color": "#556", "dashes": False, "width": 2.0},
    "affiliation":  {"color": "#666", "dashes": False, "width": 2.0},
    "rival":        {"color": "#9a5b5b", "dashes": True,  "width": 1.5},
}

LOOP_EDGE_COLOR = "#c0392b"
DIM_EDGE_COLOR = "#e7e7e7"


def compute_sizes(edge_pairs):
    """Node size by betweenness centrality on the undirected projection."""
    g = nx.Graph()
    g.add_nodes_from([n["id"] for n in data.NODES])
    g.add_edges_from(edge_pairs)
    bt = nx.betweenness_centrality(g)
    dg = dict(g.degree())
    mx = max(bt.values()) or 1.0
    sizes = {k: 16 + 30 * (v / mx) for k, v in bt.items()}
    return sizes, bt, dg


def build(period, highlight_loop):
    edges_raw = list(data.STATIC_EDGES) + data.party_edges(period)
    pairs = [(e["src"], e["dst"]) for e in edges_raw]
    sizes, bt, dg = compute_sizes(pairs)

    # nodes
    vis_nodes = []
    for n in data.NODES:
        grp = n["group"]
        col = data.COLORS[grp]
        node = {
            "id": n["id"],
            "label": n["label"],
            "title": n.get("title", n["label"]),
            "size": round(sizes.get(n["id"], 16), 1),
            "color": {"background": col["bg"], "border": col["border"],
                      "highlight": {"background": col["bg"], "border": "#000000"}},
            "font": {"color": "#111111"},
        }
        if highlight_loop:
            if n["id"] in data.LOOP_NODES:
                node["color"]["border"] = LOOP_EDGE_COLOR
                node["borderWidth"] = 4
            else:
                node["color"] = {"background": data.DIM_NODE["bg"], "border": data.DIM_NODE["border"]}
                node["font"] = {"color": data.DIM_NODE["font"]}
        vis_nodes.append(node)

    # edges
    vis_edges = []
    for e in edges_raw:
        style = EDGE_STYLE[e["type"]]
        is_loop = e.get("loop", False)
        edge = {
            "from": e["src"], "to": e["dst"],
            "label": e.get("label", ""),
            "title": e.get("title", ""),
            "dashes": style["dashes"],
            "width": style["width"],
            "color": {"color": style["color"], "highlight": "#000000"},
            "font": {"align": "middle"},
        }
        if highlight_loop:
            if is_loop:
                edge["color"] = {"color": LOOP_EDGE_COLOR, "highlight": LOOP_EDGE_COLOR}
                edge["width"] = 4
            else:
                edge["color"] = {"color": DIM_EDGE_COLOR, "highlight": DIM_EDGE_COLOR}
                edge["width"] = 1
                edge["label"] = ""
                edge["font"] = {"color": DIM_EDGE_COLOR}
        vis_edges.append(edge)

    return vis_nodes, vis_edges, bt, dg


# ---------- header ----------
st.title("The Factory as Political Machine")
st.write(
    "An interactive map of how ownership, control and credit overlap in the Pravara "
    "cooperative sugar factory and its surrounding institutions. This companion to the essay "
    "lets you see the mechanism the text describes, and change the political period to watch "
    "the machine stay put while the party label moves."
)
st.caption(
    "Schematic reconstruction from the public sources listed under Sources and notes. "
    "It shows the structure of control, and is not an exhaustive census of every tie."
)

tab_net, tab_board, tab_district, tab_src = st.tabs(
    ["Network", "Actual board, 2021", "Ahilyanagar mills, FRP comparison", "Sources and notes"]
)

# ---------- network tab ----------
with tab_net:
    left, right = st.columns([3, 2], gap="large")

    with right:
        st.subheader("Controls")
        period_label = st.radio(
            "Political period",
            ["Before 2019 (Congress)", "After 2019 (BJP)"],
            index=1,
        )
        period = "before" if period_label.startswith("Before") else "after"

        highlight_loop = st.toggle("Highlight the capture loop", value=False)
        st.write(
            "The loop is the triangle of factory board seat, bank board seat and the loan that "
            "runs between them. When one person holds both seats, ownership, control and credit "
            "close onto the same point. That is control-rights capture."
        )

        st.subheader("A single data point")
        m1, m2, m3 = st.columns(3)
        m1.metric("FRP paid", data.FRP["paid_pct"])
        m2.metric("Arrears owed", data.FRP["arrears"])
        m3.metric("As on", data.FRP["asof"])
        st.caption("Sugar Commissionerate, Maharashtra, season 2025-26.")

    vis_nodes, vis_edges, bt, dg = build(period, highlight_loop)

    with left:
        html = build_html(vis_nodes, vis_edges, data.LEGEND, height=620)
        components.html(html, height=720, scrolling=False)

    # centrality table under the graph
    st.subheader("Who sits at the centre")
    df = pd.DataFrame({
        "Actor": [n["label"] for n in data.NODES],
        "Betweenness": [round(bt[n["id"]], 3) for n in data.NODES],
        "Degree": [dg[n["id"]] for n in data.NODES],
    }).sort_values("Betweenness", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True, height=330)
    st.write(
        "Radhakrishna Vikhe Patil scores highest on betweenness because he stands between the "
        "family, the factory, the bank and the party. Switch the period above and recompute: the "
        "structure barely changes, which is the point. The machine is stable, and only its party "
        "attachment moves."
    )

# ---------- board tab ----------
with tab_board:
    st.subheader("Board of directors, 2021")
    st.write(
        "The full roster from the factory's own filing. Two of the twenty-six seats, the two most "
        "powerful, are held by the family: the Chairman and an Expert Director. The remaining seats "
        "sit with the surrounding landed elite. Nearly every name carries the title Patil, which is "
        "a lineage marker rather than proof of one family, and that breadth is itself the point: the "
        "cooperative institutionalises the dominance of a whole landholding stratum, with the dynasty "
        "at its apex."
    )
    board_df = pd.DataFrame(
        [(sr, name, desig, "Vikhe Patil family" if fam else "")
         for sr, name, desig, fam in data.BOARD],
        columns=["No.", "Name", "Designation", "Note"],
    )
    st.dataframe(board_df, use_container_width=True, hide_index=True, height=560)
    st.caption("Transcribed from the Pre-Feasibility Report filed with MoEF&CC, 2021.")

# ---------- district comparison tab ----------
with tab_district:
    st.subheader("Fair and Remunerative Price: Ahilyanagar district, season 2025-26")
    st.write(
        "All twenty-one sugar mills operating in Pravara's own district, drawn from the same "
        "official report and the same market conditions and sugar prices. If arrears were only "
        "about the sugar cycle, mills in one district would cluster together. They do not, which "
        "is the point: how much a mill pays its farmers tracks its governance, not just its price "
        "environment."
    )

    frp_df = pd.read_csv("data/frp_statement_a_2025_26.csv")
    ahil = frp_df[frp_df["district"] == "Ahilyanagar"].copy()
    ahil = ahil.sort_values("pct_frp_paid", ascending=True)
    ahil["short_name"] = ahil["factory_name"].str.split(",").str[0].str.slice(0, 40)
    ahil["is_pravara"] = ahil["factory_name"].str.contains("Vitthalrao Vikhe Patil")

    chart_df = ahil.set_index("short_name")[["pct_frp_paid"]].rename(
        columns={"pct_frp_paid": "% FRP paid"}
    )
    st.bar_chart(chart_df, height=520)

    pravara_row = ahil[ahil["is_pravara"]].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Pravara: % FRP paid", f"{pravara_row['pct_frp_paid']:.1f}%")
    c2.metric("Pravara: arrears", f"Rs {pravara_row['arrears_lakh']/100:.1f} cr")
    c3.metric("District range", f"{ahil['pct_frp_paid'].min():.1f}% to {ahil['pct_frp_paid'].max():.1f}%")

    st.write(
        "Pravara sits in the middle of its own district, better than several neighbours and worse "
        "than others, all facing the same season. The spread from roughly 40 per cent to 100 per "
        "cent paid, among mills with the same crop and the same market, is the empirical trace of "
        "the argument made in Sections 4 and 5 of the essay: FRP payment is discretionary in "
        "practice, whatever its statutory form."
    )

    with st.expander("See the full table"):
        show_cols = ["sr_no", "factory_name", "type", "tcd", "crushing_mt",
                     "total_net_frp_payable_lakh", "total_frp_paid_excl_ht_lakh",
                     "arrears_lakh", "pct_frp_paid"]
        st.dataframe(
            ahil[show_cols].sort_values("sr_no").rename(columns={
                "sr_no": "Sr.", "factory_name": "Factory", "type": "Type", "tcd": "TCD",
                "crushing_mt": "Crushing (MT)", "total_net_frp_payable_lakh": "Net FRP payable (Rs lakh)",
                "total_frp_paid_excl_ht_lakh": "FRP paid, excl. H&T (Rs lakh)",
                "arrears_lakh": "Arrears (Rs lakh)", "pct_frp_paid": "% FRP paid",
            }),
            use_container_width=True, hide_index=True, height=420,
        )
    st.caption(
        "Sugar Commissionerate, Maharashtra, Statement A, season 2025-26, as on 28 February 2026. "
        "Transcribed from the original scanned report; see Sources and notes for the cleanup method."
    )

# ---------- sources tab ----------
with tab_src:
    st.subheader("Sources and notes")
    for title, detail in data.SOURCES:
        st.markdown(f"**{title}.** {detail}")
    st.write("")
    st.write(
        "On the 2017 loan: the reported transaction was a loan to a Vikhe Patil sugarcane venture "
        "from a district cooperative bank on whose board the borrower also sat. It is shown here to "
        "illustrate the interlock between factory boards and the banks that finance them, not to "
        "assert that this particular loan was drawn by the Pravara factory."
    )
    st.write(
        "On method: node size reflects betweenness centrality, a standard measure of how far an "
        "actor sits on the paths between others. The network is drawn only from the public sources "
        "above."
    )
    st.write(
        "On the district FRP table: it was converted from a scanned government PDF, which "
        "introduces the usual optical-character-recognition noise. District names were normalised "
        "against the standard list of Maharashtra districts and cross-checked against each "
        "factory's own printed address. Every one of the 206 mill rows in the underlying report "
        "was validated by summing the payable, paid and crushing columns and comparing the totals "
        "to the Commissionerate's own summary block, which they reconcile against closely. The "
        "cleaned data file sits in this repository under data/."
    )
