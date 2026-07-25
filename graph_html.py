import json


def build_html(nodes, edges, legend, height=640):
    """Return a self-contained HTML string rendering the network with vis-network.
    Colours, background and tooltips are hard-set so the appearance does not
    change under a browser or OS dark-mode setting."""
    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)
    legend_json = json.dumps(legend)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="light only">
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  :root {{ color-scheme: only light; }}
  html, body {{
    background: #ffffff !important;
    color: #111111;
    margin: 0; padding: 0;
    font-family: Georgia, 'Times New Roman', serif;
    forced-color-adjust: none;
  }}
  #net {{
    width: 100%; height: {height}px;
    background: #ffffff;
    border: 1px solid #d7d7d7; border-radius: 4px;
  }}
  .vis-tooltip {{
    position: absolute;
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #2b2b2b !important;
    border-radius: 4px !important;
    padding: 9px 11px !important;
    font-family: Georgia, serif !important;
    font-size: 13px !important;
    line-height: 1.4 !important;
    max-width: 330px !important;
    white-space: normal !important;
    box-shadow: 0 2px 9px rgba(0,0,0,0.20) !important;
    z-index: 1000;
  }}
  .legend {{
    font-family: Georgia, serif; font-size: 13px; color: #111111;
    margin: 12px 2px 2px 2px; display: flex; flex-wrap: wrap; gap: 8px 18px;
  }}
  .legend .item {{ display: inline-flex; align-items: center; }}
  .legend .dot {{
    display: inline-block; width: 12px; height: 12px; border-radius: 50%;
    margin-right: 6px; border: 1px solid rgba(0,0,0,0.25);
  }}
</style>
</head>
<body>
  <div id="net"></div>
  <div class="legend" id="legend"></div>
<script>
  const nodes = new vis.DataSet({nodes_json});
  const edges = new vis.DataSet({edges_json});
  const container = document.getElementById('net');
  const options = {{
    nodes: {{
      shape: 'dot',
      borderWidth: 2,
      font: {{ color: '#111111', face: 'Georgia', size: 15, strokeWidth: 4, strokeColor: '#ffffff' }}
    }},
    edges: {{
      font: {{ color: '#3a3a3a', face: 'Georgia', size: 11, strokeWidth: 4, strokeColor: '#ffffff' }},
      arrows: {{ to: {{ enabled: true, scaleFactor: 0.55 }} }},
      smooth: {{ type: 'dynamic' }},
      color: {{ inherit: false }}
    }},
    physics: {{
      barnesHut: {{ gravitationalConstant: -9000, centralGravity: 0.35, springLength: 150, springConstant: 0.05 }},
      stabilization: {{ iterations: 300 }}
    }},
    interaction: {{ hover: true, tooltipDelay: 70, navigationButtons: false, keyboard: false }}
  }};
  const network = new vis.Network(container, {{ nodes: nodes, edges: edges }}, options);
  network.once('stabilizationIterationsDone', function () {{ network.setOptions({{ physics: false }}); }});

  const legendItems = {legend_json};
  const lg = document.getElementById('legend');
  legendItems.forEach(function (it) {{
    const wrap = document.createElement('span');
    wrap.className = 'item';
    const dot = document.createElement('span');
    dot.className = 'dot';
    dot.style.background = it.color;
    wrap.appendChild(dot);
    wrap.appendChild(document.createTextNode(it.label));
    lg.appendChild(wrap);
  }});
</script>
</body>
</html>"""
