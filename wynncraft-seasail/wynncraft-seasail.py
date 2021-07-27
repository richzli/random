INFTY = 10**8

def read_data():
    f = open("data.txt", "r")
    g = {}
    l = set()

    for line in f:
        if line.startswith("#"):
            continue

        u, v, w = line.strip().split()
        u = u.replace("_", " ")
        v = v.replace("_", " ")
        w = int(w)
        l.add(u)
        l.add(v)
        
        if u in g:
            g[u][v] = w
        else:
            g[u] = {v: w}
    for loc in l:
        g[loc][loc] = 0

    return (g, l)

def solve(graph, locations):
    paths = {}
    for u in locations:
        paths[u] = {}
        for v in locations:
            paths[u][v] = (INFTY, [])

    for u in graph:
        for v in graph[u]:
            paths[u][v] = (graph[u][v], [u, v] if u != v else [u])

    for i in locations:
        for j in locations:
            if i != j:
                for k in locations:
                    if paths[i][k][0] + paths[k][j][0] < paths[i][j][0]:
                        paths[i][j] = (
                            paths[i][k][0] + paths[k][j][0],
                            paths[i][k][1] + paths[k][j][1][1:]
                        )
    
    return paths

def main():
    g, l = read_data()
    p = solve(g, l)
    ls = sorted(list(l))

    import tkinter as tk

    class SeasailGUI(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title("V.S.S. Seaskipper Cheapest Routes")
            self.resizable(False, False)

            self.mainframe = tk.Frame(self)
            self.mainframe.grid(row=0, column=0, padx=10, pady=10)

            self.labelsource = tk.Label(self.mainframe, text = "Source Port")
            self.labelsource.pack(side="top")
            self.sourcevar = tk.StringVar(self, ls[0])
            self.sourceoptions = tk.OptionMenu(self.mainframe, self.sourcevar, *ls)
            self.sourceoptions.pack(side="top")

            self.labeldest = tk.Label(self.mainframe, text = "Destination Port")
            self.labeldest.pack(side="top")
            self.destvar = tk.StringVar(self, ls[0])
            self.destoptions = tk.OptionMenu(self.mainframe, self.destvar, *ls)
            self.destoptions.pack(side="top")

            self.calcbutton = tk.Button(self.mainframe, text = "Get Route", command = self.calculate)
            self.calcbutton.pack(side="top", pady=20)

            self.display = tk.Text(self.mainframe, state="disabled", width=25, height=7)
            self.display.pack(side="top")

        def calculate(self):
            dist, path = p[self.sourcevar.get()][self.destvar.get()]
            self.display.configure(state="normal")
            self.display.delete("1.0", "end")
            self.display.insert("1.0", "\n".join([f"{dist} Emeralds"] + path))
            self.display.configure(state="disabled")
    
    app = SeasailGUI()
    app.mainloop()

if __name__ == "__main__":
    main()