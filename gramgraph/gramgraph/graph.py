import os
import pickle
import json
from typing import Dict, List, Tuple

import plotly.graph_objects as go
import plotly
import networkx as nx

from .config import (
    DATA_DIRECTORY,
    PRUNED_FIGURE_FILENAME,
    UNPRUNED_FIGURE_FILENAME,
    PICKLE_FILENAME,
)

test_data = {
    "a": ["b", "c"],
    "b": ["c"],
    # "c": [],
    "d": ["a", "b", "c"],
    "e": ["a"],
}
test_data = nx.random_geometric_graph(200, 0.125)


def main():
    # G = GramGraph(test_data, prune=True)
    # G.show_graph()

    GG = GramGraph(test_data)
    GG.show_graph()


class GramGraph(nx.DiGraph):
    def __init__(self, data: Dict[str, List[str]], prune: bool = False):
        super().__init__(data)
        if prune:
            self._prune_graph()
        self.node_size = 10

    def _position_graph(self):
        """Adds 'pos' attribute to each node, used to draw graph later"""
        position = nx.spring_layout(self)
        for node in self.nodes():
            self.nodes[node]["pos"] = list(position[node])

    def _create_edge_trace(self) -> go.Scatter:
        edge_x = []
        edge_y = []
        for edge in self.edges():
            x0, y0 = self.nodes[edge[0]]["pos"]
            x1, y1 = self.nodes[edge[1]]["pos"]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        return go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(
                width=0.5,
                color="#888",
            ),
            hoverinfo="none",
            mode="lines",
        )

    def _create_node_trace(self) -> go.Scatter:
        node_x = []
        node_y = []
        for node in self.nodes():
            x, y = self.nodes[node]["pos"]
            node_x.append(x)
            node_y.append(y)

        return go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                showscale=True,
                colorscale="YlGnBu",
                color=[],
                size=self.node_size,
                colorbar=dict(
                    thickness=15,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right",
                ),
                line_width=2,
            ),
        )

    def plot_graph(self) -> go.Figure:
        self._position_graph()
        edge_trace = self._create_edge_trace()
        node_trace = self._create_node_trace()

        node_adjacencies = []
        node_text = []
        for node, adjacencies in self.adjacency():
            n_adjacencies = len(adjacencies)
            node_adjacencies.append(n_adjacencies)
            node_text.append(f"{node}: {n_adjacencies} connections")

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        return go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                height=600,
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                ),
            ),
        )

    def show_graph(self):
        self.plot_graph().show()

    def _prune_graph(self):

        nodes_to_remove = []
        edges_to_remove = []

        for node, adjacent in self.adjacency():
            n_adjacent = len(adjacent)
            if n_adjacent <= 1:
                nodes_to_remove.append(node)
                edges_to_remove.extend(self.edges(node))

        self.remove_nodes_from(nodes_to_remove)
        self.remove_edges_from(edges_to_remove)


def get_figures_JSON() -> Tuple[str, str]:
    """Preloads JSON for both pruned and unpruned graphs"""
    with open(PICKLE_FILENAME, "rb") as f:
        followers = pickle.load(f)
    G = GramGraph(followers, prune=False)
    GP = GramGraph(followers, prune=True)
    unpruned_fig = G.plot_graph()
    pruned_fig = GP.plot_graph()
    return (
        json.dumps(pruned_fig, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(unpruned_fig, cls=plotly.utils.PlotlyJSONEncoder),
    )


def save_figures_JSON():
    """converts followers data into pruned and unpruned data"""
    pruned_json, unpruned_json = get_figures_JSON()

    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)

    for json_file, filename in [
        (pruned_json, PRUNED_FIGURE_FILENAME),
        (unpruned_json, UNPRUNED_FIGURE_FILENAME),
    ]:
        with open(filename, "w") as f:
            f.write(json_file)

    print("graph json prepared (pruned and unpruned)")


if __name__ == "__main__":
    main()
