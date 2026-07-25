import json

import networkx as nx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import data
from graph_html import build_html

st.set_page_config(page_title="Pravara: the sugar-bank-party network",
                   layout="wide", initial_sidebar_state="collapsed")

# Force a light appearance even when the browser or OS is set to dark mode,
# and keep text dark so nothing camouflages against the background.
st.markdown(
    """
    <style>
      :root { color-scheme: only light; }
      html, body, .stApp,
      [data-testid="stAppViewContainer"],
      [data-testid="stHeader"] {
        background-color: #ffffff !important;
        color: #111111 !important;
      }
      .stApp, .stMarkdown p, .stMarkdown li, label, h1, h2, h3, h4,
      [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #111111 !important;
      }
      /* keep the heading family consistent and un-templated */
      h1, h2, h3, h4 { font-family: Georgia, 'Times New Roman', serif !important; }
      [data-testid="stMetricValue"] { font-family: Georgia, serif !important; }
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

tab_net, tab_board, tab_src = st.tabs(["Network", "Actual board, 2021", "Sources and notes"])

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
