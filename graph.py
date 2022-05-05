from typing import Dict, List

import plotly.graph_objects as go
import networkx as nx

# test_data = {
#     "a": ["b", "c"],
#     "b": ["c"],
#     "c": [],
#     "d": ["a", "b", "c", "d"],
# }
test_data = nx.random_geometric_graph(200, 0.125)


def main():
    G = GramGraph(test_data)
    fig = G.plot_graph()
    fig.show()


class GramGraph(nx.Graph):
    def __init__(self, data: Dict[str, List[str]]):
        super().__init__(data)

    def _position_graph(self):
        """Adds 'pos' attribute to each node, used to draw graph later"""
        position = nx.spring_layout(self)
        for node in self.nodes():
            self.nodes[node]["pos"] = list(position[node])

    def _create_edge_traces(self) -> go.Scatter:
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

    def _create_node_traces(self) -> go.Scatter:
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
                size=10,
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
        edge_trace = self._create_edge_traces()
        node_trace = self._create_node_traces()

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
                title="Network graph made with Python",
                titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
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


if __name__ == "__main__":
    main()
