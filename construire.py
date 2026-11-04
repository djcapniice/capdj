"""Fabrique docs/index.html (à partir de modele.html), favicon.svg et apple-touch-icon.png
avec le symbole CAP DJ tiré des fichiers de l'app (app/Outils/symbole*.txt)."""
import os, re, subprocess

ICI = os.path.dirname(os.path.abspath(__file__))
OUTILS = os.path.join(ICI, "..", "app", "Outils")
ROSE = "#FF375F"


def lire(nom):
    lignes = open(os.path.join(OUTILS, nom), encoding="utf-8").read().strip().split("\n")
    cercles = [tuple(float(v) for v in l.split()) for l in lignes[1:4]]
    return lignes[0], cercles, lignes[4]


def boite(contour, cercles, marge=1.5):
    nombres = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", contour)]
    xs, ys = nombres[0::2], nombres[1::2]
    for (cx, cy, r) in cercles:
        xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
    x0, y0, x1, y1 = min(xs) - marge, min(ys) - marge, max(xs) + marge, max(ys) + marge
    return f"{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}"


def interieur(contour, cercles):
    (a, b, c) = cercles
    return (f'<path fill="currentColor" d="{contour}"/>'
            f'<circle fill="currentColor" cx="{a[0]}" cy="{a[1]}" r="{a[2]}"/>'
            f'<circle fill="currentColor" cx="{b[0]}" cy="{b[1]}" r="{b[2]}"/>'
            f'<circle fill="{ROSE}" cx="{c[0]}" cy="{c[1]}" r="{c[2]}"/>')


fin_c, fin_cercles, fin_centre = lire("symbole.txt")
ep_c, ep_cercles, _ = lire("symbole-icone.txt")
vue_fin, vue_epais = boite(fin_c, fin_cercles), boite(ep_c, ep_cercles)

# Grand logo de l'ouverture : le trait se dessine (masque qui suit la ligne centrale), puis le point apparaît.
(a, b, c) = fin_cercles
anime = (f'<svg viewBox="{vue_fin}" aria-hidden="true"><defs><mask id="masque-trace" maskUnits="userSpaceOnUse">'
         f'<path class="trace-masque" d="{fin_centre}" pathLength="1" fill="none" stroke="#fff" stroke-width="18" '
         f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 1"/></mask></defs>'
         f'<g mask="url(#masque-trace)" fill="currentColor"><path d="{fin_c}"/>'
         f'<circle cx="{a[0]}" cy="{a[1]}" r="{a[2]}"/><circle cx="{b[0]}" cy="{b[1]}" r="{b[2]}"/></g>'
         f'<circle class="point" fill="{ROSE}" cx="{c[0]}" cy="{c[1]}" r="{c[2]}"/></svg>')

page = open(os.path.join(ICI, "modele.html"), encoding="utf-8").read()
for cle, val in {"{{VUE_FIN}}": vue_fin, "{{VUE_EPAIS}}": vue_epais, "{{SYMBOLE_FIN}}": interieur(fin_c, fin_cercles),
                 "{{SYMBOLE_EPAIS}}": interieur(ep_c, ep_cercles), "{{SYMBOLE_ANIME}}": anime}.items():
    page = page.replace(cle, val)
assert "{{" not in page
open(os.path.join(ICI, "docs", "index.html"), "w", encoding="utf-8").write(page)

# Icône d'onglet : carré noir arrondi, symbole épais blanc et point rose.
vx, vy, vw, vh = [float(v) for v in vue_epais.split()]
cote = max(vw, vh) * 1.42
ox, oy = vx - (cote - vw) / 2, vy - (cote - vh) / 2
favicon = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ox:.1f} {oy:.1f} {cote:.1f} {cote:.1f}">'
           f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{cote:.1f}" height="{cote:.1f}" rx="{cote * 0.22:.1f}" fill="#000"/>'
           f'<g style="color:#fff">{interieur(ep_c, ep_cercles)}</g></svg>')
open(os.path.join(ICI, "docs", "favicon.svg"), "w", encoding="utf-8").write(favicon)

# Icône pour l'écran d'accueil (iPhone, iPad) : tirée des icônes de l'app.
icone = "/tmp/capdj_icones/icon_512x512@2x.png"
if os.path.exists(icone):
    subprocess.run(["sips", "-z", "180", "180", icone, "--out", os.path.join(ICI, "docs", "apple-touch-icon.png")],
                   check=True, capture_output=True)
print("page, favicon et icône fabriqués ·", vue_fin, "·", vue_epais)
