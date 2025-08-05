
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Graph Algorithms", layout="centered")
st.title("🔗 Graph Algorithms GUI (Streamlit Edition)")

st.markdown("""
This app lets you create a directed weighted graph and run shortest-path algorithms:
- **Dijkstra**
- **Bellman-Ford**
- **Floyd-Warshall**
""")

# Session state for graph
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()
G = st.session_state.graph

# Graph building
with st.expander("📌 Add nodes and edges"):
    nodes = st.number_input("Number of nodes", min_value=2, max_value=20, value=5)
    if st.button("Initialize graph"):
        G.clear()
        G.add_nodes_from(range(1, nodes + 1))
        st.success("Graph initialized!")

    col1, col2, col3 = st.columns(3)
    with col1:
        u = st.number_input("From (node)", min_value=1, max_value=nodes, value=1)
    with col2:
        v = st.number_input("To (node)", min_value=1, max_value=nodes, value=2)
    with col3:
        weight = st.number_input("Weight", min_value=1, max_value=999, value=1)

    if st.button("Add edge"):
        G.add_edge(u, v, weight=weight)
        st.success(f"Edge added: {u} → {v} (weight {weight})")

# Visualization
st.subheader("📊 Graph Visualization")
pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots()
nx.draw(G, pos, with_labels=True, node_color='#1f78b4', node_size=800, edge_color='gray', font_color='white', ax=ax)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
st.pyplot(fig)

# Algorithms
st.subheader("🧠 Algorithms")
algo = st.selectbox("Choose algorithm", ["Dijkstra", "Bellman-Ford", "Floyd-Warshall"])

if algo in ["Dijkstra", "Bellman-Ford"]:
    source = st.number_input("Source node", min_value=1, max_value=nodes, value=1)
    if st.button(f"Run {algo}"):
        try:
            if algo == "Dijkstra":
                distances = nx.single_source_dijkstra_path_length(G, source)
            else:
                distances = nx.single_source_bellman_ford_path_length(G, source)
            st.code("\n".join([f"{source} → {v}: {d}" for v, d in distances.items()]))
        except Exception as e:
            st.error(f"Error: {e}")

elif algo == "Floyd-Warshall":
    if st.button("Run Floyd-Warshall"):
        try:
            dist_matrix = nx.floyd_warshall_numpy(G).tolist()
            st.write("Distance matrix:")
            st.dataframe(dist_matrix)
        except Exception as e:
            st.error(f"Error: {e}")
