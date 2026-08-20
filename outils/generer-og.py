"""Vignettes de partage (Open Graph), 1200x630.

Une par page : c'est l'image qu'affichent LinkedIn, WhatsApp, Slack ou
Facebook quand quelqu'un partage un lien. Reprend l'identité du site —
fond crème, carte indigo, anneau de solde, police Roboto.
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

SORTIE = pathlib.Path("img/og")
SORTIE.mkdir(parents=True, exist_ok=True)
POLICES = "assets/fonts"  # copiées depuis le dépôt de l'application

W, H = 1200, 630
BG = "#f5f2ec"
INK = "#19202b"
MUTED = "#646c7b"
BRAND = "#4f46e5"
BRAND2 = "#6d5ef0"
ACC = "#f0a028"
WHITE = "#ffffff"

bd = lambda t: ImageFont.truetype(f"{POLICES}/Roboto-Bold.ttf", t)
rg = lambda t: ImageFont.truetype(f"{POLICES}/Roboto-Regular.ttf", t)


def anneau(d, x, y, t):
    """Icône de l'app : carré indigo, anneau blanc, arc orange."""
    d.rounded_rectangle([x, y, x + t, y + t], radius=int(t * 0.22), fill=BRAND)
    m, r = t * 0.5, t * 0.31
    cx, cy = x + m, y + m
    lw = max(2, int(t * 0.095))
    box = [cx - r, cy - r, cx + r, cy + r]
    d.arc(box, 0, 360, fill="#ffffff55", width=lw)
    d.arc(box, -90, 0, fill=WHITE, width=lw)
    d.arc(box, 0, 45, fill=ACC, width=lw)


def couper(d, txt, police, larg):
    """Découpe un texte à la largeur voulue."""
    mots, lignes, cur = txt.split(), [], ""
    for mot in mots:
        essai = (cur + " " + mot).strip()
        if d.textlength(essai, font=police) <= larg:
            cur = essai
        else:
            if cur:
                lignes.append(cur)
            cur = mot
    if cur:
        lignes.append(cur)
    return lignes


def vignette(nom, marque, titre, sous_titre, chiffre=None, legende=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    # Bandeau indigo à droite quand il y a un chiffre à mettre en avant.
    larg_texte = W - 130 - (330 if chiffre else 60)
    if chiffre:
        d.rounded_rectangle([W - 350, 90, W - 70, H - 90], radius=34, fill=BRAND)
        f = bd(150 if len(chiffre) <= 2 else 110)
        bb = d.textbbox((0, 0), chiffre, font=f)
        d.text((W - 210 - (bb[2] - bb[0]) / 2, 250 - (bb[3] - bb[1]) / 2),
               chiffre, font=f, fill=WHITE)
        if legende:
            fl = rg(26)
            for i, l in enumerate(couper(d, legende, fl, 230)):
                bb = d.textbbox((0, 0), l, font=fl)
                d.text((W - 210 - (bb[2] - bb[0]) / 2, 360 + i * 34),
                       l, font=fl, fill="#ffffffdd")

    anneau(d, 70, 66, 58)
    d.text((146, 80), marque, font=bd(30), fill=INK)

    ft = bd(64)
    lignes = couper(d, titre, ft, larg_texte)[:3]
    y = 210
    for l in lignes:
        d.text((70, y), l, font=ft, fill=INK)
        y += 76

    fs = rg(30)
    y += 18
    for l in couper(d, sous_titre, fs, larg_texte)[:3]:
        d.text((70, y), l, font=fs, fill=MUTED)
        y += 42

    im.save(SORTIE / f"{nom}.png", "PNG", optimize=True)
    return (SORTIE / f"{nom}.png").stat().st_size


PAGES = [
    ("accueil", "G-conges", "Suis tes congés payés et tes RTT",
     "Soldes, calendrier, meilleurs ponts. Hors connexion.", None, None),
    ("ponts-2027", "G-conges", "Ponts 2027 : le calendrier complet",
     "4 ponts à saisir, et 4 week-ends de 3 jours offerts.",
     "18", "jours de repos pour 6 posés"),
    ("brueckentage-2027", "Hab-Frei", "Brückentage 2027",
     "Alle 16 Bundesländer im Vergleich.",
     "19", "freie Tage in Bayern für 6 Urlaubstage"),
    ("brugdagen-2027", "Heb-vrij", "Brugdagen 2027",
     "Twee brugdagen, allebei in het voorjaar.",
     "8", "dagen vrij voor 2 vakantiedagen"),
    ("klamdagar-2027", "ÄR-ledig", "Klämdagar 2027",
     "Tre tillfällen, varav två i januari.",
     "16", "lediga dagar för 5 semesterdagar"),
    ("en", "Im-off", "Track your paid leave without the guesswork",
     "Balances, calendar, best bridge days. Works offline.", None, None),
    ("de", "Hab-Frei", "Deinen Urlaub im Blick, ohne Rätselraten",
     "Salden, Kalender, die besten Brückentage. Offline.", None, None),
    ("nl", "Heb-vrij", "Je vakantiedagen in beeld",
     "Saldo's, kalender, de beste brugdagen. Offline.", None, None),
    ("sv", "ÄR-ledig", "Koll på semestern, utan gissningar",
     "Saldon, kalender, de bästa klämdagarna. Offline.", None, None),
    ("confidentialite", "G-conges", "Politique de confidentialité",
     "Tes données restent sur ton téléphone. Aucun compte, aucun serveur.",
     None, None),
    ("privacy", "Im-off", "Privacy policy",
     "Your data stays on your phone. No account, no server.", None, None),
]

for args in PAGES:
    taille = vignette(*args)
    print(f"  {args[0]:20s} {taille / 1024:5.0f} Ko")
