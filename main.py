import tkinter as tk
from tkinter import messagebox
import plotly.graph_objects as go
import genetic_for_tsp as tsp

# Interface configuration
BG_COLOR = "#FFFFFF"
ACCENT_BLUE = "#87CEEB"
TEXT_COLOR = "#2C3E50"
INPUT_BG = "#EEF4FB"
TEXTAREA_BG = "#F4F8FC"
BUTTON_BG = "#2F80C1"
BORDER_SOFT = "#D7E4F1"
BORDER_FOCUS = "#7EA9CF"
FONT_MAIN = ("Inter", 11)
FONT_TITLE = ("Inter", 13, "bold")


def run_tsp():
    try:
        n = int(entree_n.get())
        nb_generations = 500
        villes_init = tsp.generate_random_villes(n)
        chemin, distance = tsp.tsp_algorithm(villes_init, gens=nb_generations)
        label_resultat.config(
            text=f"Distance : {distance:.2f} km | Générations : {nb_generations}"
        )

        zone_texte.delete("1.0", tk.END)
        zone_texte.tag_configure(
            "header", foreground=ACCENT_BLUE, font=FONT_MAIN + ("bold",)
        )
        zone_texte.tag_configure("ville", foreground=TEXT_COLOR)

        zone_texte.insert(tk.END, "ENSEMBLE DES VILLES:\n", "header")
        for v in villes_init:
            zone_texte.insert(tk.END, f"  • {v.nom}\n", "ville")
        zone_texte.insert(tk.END, "\n" + "=" * 30 + "\n\n")

        zone_texte.insert(
            tk.END,
            f" Chemin optimal trouvé (Départ choisi : {chemin[0].nom})\n",
            "header",
        )
        for i, v in enumerate(chemin, start=1):
            zone_texte.insert(tk.END, f"  {i}. {v.nom}\n", "ville")
        zone_texte.insert(
            tk.END, f"  {len(chemin)+1}. {chemin[0].nom} (Retour)\n", "header"
        )

        afficher_carte(chemin, distance)

    except FileNotFoundError:
        messagebox.showerror(
            "Erreur", "Le fichier 'villes_france.json' est introuvable."
        )
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


def afficher_carte(chemin, distance):
    trace = chemin + [chemin[0]]
    mode_affichage = "lines+markers+text" if len(chemin) < 25 else "lines+markers"

    fig = go.Figure(
        go.Scattermapbox(
            lat=[v.latitude for v in trace],
            lon=[v.longitude for v in trace],
            mode=mode_affichage,
            text=[f"{i+1}. {v.nom}" for i, v in enumerate(chemin)] + ["Arrivée"],
            textposition="top right",
            marker=dict(size=8, color=ACCENT_BLUE),
            line=dict(width=2, color=ACCENT_BLUE),
            hoverinfo="text",
        )
    )

    fig.update_layout(
        title=f"Circuit IA - {distance:.2f} km",
        mapbox_style="open-street-map",
        mapbox=dict(center=dict(lat=46.6, lon=2.2), zoom=5),
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
    )
    fig.show()


root = tk.Tk()
root.title("Résolution du TSP avec Algorithme Génétique")
root.geometry("900x650")
root.configure(bg=BG_COLOR)

header = tk.Frame(root, bg=ACCENT_BLUE, height=60)
header.pack(fill=tk.X)
tk.Label(
    header,
    text="TSP : Algorithme Génétique",
    bg=ACCENT_BLUE,
    fg="white",
    font=FONT_TITLE,
).pack(pady=15)

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)

frame_ctrl = tk.Frame(main_frame, bg=BG_COLOR)
frame_ctrl.pack(side=tk.LEFT, anchor="n", padx=10)

tk.Label(frame_ctrl, text="Nombre de villes", bg=BG_COLOR, font=FONT_MAIN).pack(
    pady=(0, 5)
)
entree_n = tk.Entry(
    frame_ctrl,
    font=FONT_MAIN,
    justify="center",
    width=8,
    bg=INPUT_BG,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER_SOFT,
    highlightcolor=BORDER_FOCUS,
)
entree_n.insert(0, "20")
entree_n.pack(pady=5)

btn_calcul = tk.Button(
    frame_ctrl,
    text="CALCULER",
    command=run_tsp,
    bg=BUTTON_BG,
    fg="white",
    activebackground="#256AA2",
    activeforeground="white",
    font=FONT_TITLE,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER_SOFT,
    highlightcolor=BORDER_FOCUS,
    cursor="hand2",
    padx=20,
)
btn_calcul.pack(pady=20)

label_resultat = tk.Label(
    frame_ctrl, text="Résolution du TSP", bg=BG_COLOR, font=FONT_MAIN, fg=TEXT_COLOR
)
label_resultat.pack(pady=10)

frame_liste = tk.Frame(main_frame, bg=BG_COLOR)
frame_liste.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

tk.Label(
    frame_liste,
    text="Liste des villes et chemin optimal trouvé :",
    bg=BG_COLOR,
    font=FONT_TITLE,
    fg=TEXT_COLOR,
).pack(anchor="w")

scrollbar = tk.Scrollbar(
    frame_liste,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER_SOFT,
    activebackground="#B5CBE0",
    troughcolor="#EDF3F9",
)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

zone_texte = tk.Text(
    frame_liste,
    font=FONT_MAIN,
    bg=TEXTAREA_BG,
    fg=TEXT_COLOR,
    relief="flat",
    bd=0,
    padx=10,
    pady=10,
    highlightthickness=1,
    highlightbackground=BORDER_SOFT,
    highlightcolor=BORDER_FOCUS,
    yscrollcommand=scrollbar.set,
)
zone_texte.pack(expand=True, fill=tk.BOTH, pady=5)
scrollbar.config(command=zone_texte.yview)

root.mainloop()
