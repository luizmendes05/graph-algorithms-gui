import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, Canvas, Frame, VERTICAL, RIGHT, Y
import random

root = tk.Tk()
root.title("Graph Menu")
root.state('zoomed')
graph = nx.DiGraph()

def show_graph_func(graph):
    plt.figure(figsize=(8, 6))
    n = graph.number_of_nodes()
    if n <= 6:
        pos = nx.circular_layout(graph)
    else:
        pos = nx.spring_layout(graph, seed=42, k=0.5)
    nx.draw_networkx_nodes(graph, pos, node_color='#1f78b4', node_size=900)
    nx.draw_networkx_edges(graph, pos, edge_color='#333333', width=2, arrowsize=25, connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_labels(graph, pos, font_size=14, font_color='white', font_weight='bold')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='red', font_size=12)
    plt.title("Graph Visualization", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def show_result(text):
    result_window = tk.Toplevel(root)
    result_window.title("Result")
    result_window.geometry("420x320")
    txt = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, font=("Consolas", 12))
    txt.insert(tk.END, text)
    txt.configure(state='disabled')
    txt.pack(expand=True, fill='both')

def dijkstra_func():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    for u, v, d in graph.edges(data=True):
        if d.get('weight', 0) < 0:
            messagebox.showerror("Error", "Dijkstra's algorithm does not support negative edge weights.")
            return
    source = simpledialog.askinteger("Dijkstra", "Source vertex:")
    if source not in graph.nodes:
        messagebox.showerror("Error", "Invalid vertex.")
        return
    try:
        distances = nx.single_source_dijkstra_path_length(graph, source)
        result = f"Minimum distances from vertex {source}:\n"
        for v, d in distances.items():
            result += f"Vertex {v}: {d}\n"
        show_result(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def bellman_ford_func():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    source = simpledialog.askinteger("Bellman-Ford", "Source vertex:")
    if source not in graph.nodes:
        messagebox.showerror("Error", "Invalid vertex.")
        return
    try:
        distances = nx.single_source_bellman_ford_path_length(graph, source)
        result = f"Minimum distances from vertex {source}:\n"
        for v, d in distances.items():
            result += f"Vertex {v}: {d}\n"
        show_result(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def floyd_warshall_func():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    try:
        dist = nx.floyd_warshall_numpy(graph)
        matrix = dist.tolist()
        text = "Distance matrix (Floyd-Warshall):\n"
        text += "    " + "  ".join(f"{i+1:3}" for i in range(len(matrix))) + "\n"
        text += "   " + "---" * len(matrix) + "\n"
        for i, row in enumerate(matrix):
            text += f"{i+1:2} | " + "  ".join(
                f"{'∞':3}" if v == float('inf') else f"{int(v):3}" for v in row
            ) + "\n"
        show_result(text)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def initialize_graph():
    global graph
    n = simpledialog.askinteger("Initialize Graph", "Enter the number of vertices:")
    if n and n > 0:
        graph.clear()
        graph.add_nodes_from(range(1, n+1))
        messagebox.showinfo("Success", "Graph initialized.")
    else:
        messagebox.showerror("Error", "Invalid number of vertices.")

def add_edge():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    a = simpledialog.askinteger("Edge", "Source vertex:")
    b = simpledialog.askinteger("Edge", "Destination vertex:")
    weight = simpledialog.askinteger("Edge", "Edge weight:")
    if a in graph.nodes and b in graph.nodes and weight is not None:
        graph.add_edge(a, b, weight=weight)
        messagebox.showinfo("Success", f"Edge added: {a} -> {b} (weight {weight})")
    else:
        messagebox.showerror("Error", "Invalid data.")

def insert_value():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    root.lift()
    root.focus_force()
    a = simpledialog.askinteger("Insert value", "Source vertex:", parent=root)
    b = simpledialog.askinteger("Insert value", "Destination vertex:", parent=root)
    weight = simpledialog.askinteger("Insert value", "Edge weight:", parent=root)
    if a in graph.nodes and b in graph.nodes and weight is not None:
        graph.add_edge(a, b, weight=weight)
        messagebox.showinfo("Success", f"Value inserted: {a} -> {b} (weight {weight})")
    else:
        messagebox.showerror("Error", "Invalid data.")

def show_matrix():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    matrix = nx.to_numpy_array(graph, dtype=int)
    order = len(matrix)
    text = "Adjacency matrix:\n"
    text += "    " + "  ".join(f"{i+1:2}" for i in range(order)) + "\n"
    text += "   " + "---" * order + "\n"
    for i, row in enumerate(matrix):
        text += f"{i+1:2} | " + "  ".join(f"{int(v):2}" for v in row) + "\n"
    show_result(text)

def show_graph():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    show_graph_func(graph)

def fill_random():
    if graph.number_of_nodes() == 0:
        messagebox.showerror("Error", "Initialize the graph first.")
        return
    n = graph.number_of_nodes()
    graph.clear()
    graph.add_nodes_from(range(1, n+1))
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j and random.random() < 0.4:
                weight = random.randint(1, 10)
                graph.add_edge(i, j, weight=weight)
    messagebox.showinfo("Success", f"Graph filled with random values for {n} vertices.")

def exit_app():
    root.destroy()

main_frame = Frame(root, bg="#222831")
main_frame.pack(fill='both', expand=True)

canvas = Canvas(main_frame, bg="#222831", highlightthickness=0)
canvas.pack(side='left', fill='both', expand=True)

scrollbar = tk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

button_frame = Frame(canvas, bg="#222831")

button_window = canvas.create_window((canvas.winfo_width()//2, 0), window=button_frame, anchor='n')

def on_configure(event):
    canvas_width = event.width
    canvas.coords(button_window, canvas_width // 2, 0)
    canvas.configure(scrollregion=canvas.bbox('all'))

canvas.bind('<Configure>', on_configure)
button_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

center_frame = Frame(button_frame, bg="#222831")
center_frame.pack()

lbl = tk.Label(center_frame, text="GRAPH MENU", font=("Arial", 22, "bold"), fg="#00adb5", bg="#222831")
lbl.pack(pady=(40, 30))

def on_enter(e):
    e.widget['bg'] = "#00adb5"
    e.widget['fg'] = "white"

def on_leave(e):
    if e.widget == btn8:
        e.widget['bg'] = "#222831"
        e.widget['fg'] = "#00adb5"
    elif e.widget == btn9:
        e.widget['bg'] = "#00adb5"
        e.widget['fg'] = "white"
    else:
        e.widget['bg'] = "#393e46"
        e.widget['fg'] = "white"

btn1 = tk.Button(center_frame, text="Initialize graph", command=initialize_graph, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn2 = tk.Button(center_frame, text="Add edge", command=add_edge, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn2_1 = tk.Button(center_frame, text="Insert value", command=insert_value, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn3 = tk.Button(center_frame, text="Show adjacency matrix", command=show_matrix, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn4 = tk.Button(center_frame, text="Show graph (visualization)", command=show_graph, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn5 = tk.Button(center_frame, text="Dijkstra algorithm", command=dijkstra_func, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn6 = tk.Button(center_frame, text="Bellman-Ford algorithm", command=bellman_ford_func, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn7 = tk.Button(center_frame, text="Floyd-Warshall algorithm", command=floyd_warshall_func, width=30, height=2, bg="#393e46", fg="white", font=("Arial", 12, "bold"))
btn8 = tk.Button(center_frame, text="Fill with random values", command=fill_random, width=30, height=2, bg="#222831", fg="#00adb5", font=("Arial", 12, "bold"))
btn9 = tk.Button(center_frame, text="Exit", command=exit_app, width=30, height=2, bg="#00adb5", fg="white", font=("Arial", 12, "bold"))

button_list = [btn1, btn2, btn2_1, btn3, btn4, btn5, btn6, btn7, btn8, btn9]
for btn in button_list:
    btn.pack(pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

root.mainloop()
