import pandas as pd
import plotly.graph_objects as go
from config import configuration as config


class Color:
    GREEN = "#8cb369"
    RED = "#bc4b51"
    YELLOW = "#d2ac4b"
    OPACITY = 0.65

    @staticmethod
    def _hex_to_rgb(hex):
        return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2 ,4))
    @staticmethod
    def hex_to_rgb(hex):
        return f"rgba({Color._hex_to_rgb(hex)})"
    @staticmethod
    def hex_to_rgba(hex, opacity):
        color = Color._hex_to_rgb(hex)
        return f"rgba({color[0]}, {color[1]}, {color[2]}, {opacity})"


def get_parent_keys(dictionary):
    result = []
    for k, v in dictionary.items():
        for _ in v.keys():
            result.append(k)
    return result

def main():
    umsatz_df = pd.read_csv(config["inputFile"], sep=';')

    einkommen = {}
    ausgaben = {}

    for _, row in umsatz_df.iterrows():
        if int(row["Buchungstag"].split('.')[1]) != config["filterMonth"] and config["filterMonth"] != 0: continue
        empfaenger = row["Zahlungsempfaenger"].split(" ")
        betrag = row["Umsatz"]

        for name in empfaenger:
            if name.lower() in [x.lower() for x in config["einkommen"]]:
                if name in einkommen:
                    einkommen[name] += float(betrag.replace(",", "."))
                else:
                    einkommen[name] = float(betrag.replace(",", "."))
                break

            for key, value in {k.lower(): v for k, v in config["ausgaben"].items()}.items():
                if name.lower() in [x.lower() for x in value]:
                    shop = value[[x.lower() for x in value].index(name.lower())]
                    if not key in ausgaben:
                        ausgaben[key] = {}
                    if shop in ausgaben[key]:
                        ausgaben[key][shop] += float(betrag.replace(",", "."))
                    else:
                        ausgaben[key][shop] = float(betrag.replace(",", "."))

    labels = [k for k in einkommen.keys()] + ["Einkommen", "Ausgaben", "Sparen"] + [f"{k[0].upper()}{k[1:]}" for k in ausgaben.keys()] + [y for x in [list(v.keys()) for v in ausgaben.values()] for y in x]
    color_nodes = [Color.GREEN for _ in einkommen.keys()] + [Color.GREEN, Color.RED, Color.GREEN] + [Color.RED for _ in [v for v in ausgaben.values()]] + [Color.RED for _ in [y for x in [list(v.keys()) for v in ausgaben.values()] for y in x]]
    einkommen_summe = sum([v for v in einkommen.values()])
    ausgaben_summe = sum([sum(i.values()) for i in [v for v in ausgaben.values()]])


    sources = [labels.index(k) for k in einkommen.keys()] + [labels.index("Einkommen")] + [labels.index("Einkommen")] + [labels.index("Ausgaben") for _ in ausgaben.keys()] + [labels.index(f"{k[0].upper()}{k[1:]}") for k in get_parent_keys(ausgaben)]
    targets = [labels.index("Einkommen") for _ in einkommen.keys()] + [labels.index("Ausgaben")] + [labels.index("Sparen")] + [labels.index(f"{k[0].upper()}{k[1:]}") for k in ausgaben.keys()] + [labels.index(y) for x in [list(v.keys()) for v in ausgaben.values()] for y in x]
    values = [v for v in einkommen.values()] + [einkommen_summe if ausgaben_summe > einkommen_summe else ausgaben_summe] + [einkommen_summe - ausgaben_summe] + [sum(v.values()) for v in ausgaben.values()] + [y for x in [list(v.values()) for v in ausgaben.values()] for y in x]
    color_links = [Color.GREEN for _ in einkommen.keys()] + [Color.YELLOW, Color.GREEN] + [Color.RED for _ in [v for v in ausgaben.values()]] + [Color.RED for _ in [y for x in [list(v.keys()) for v in ausgaben.values()] for y in x]]

    if ausgaben_summe > einkommen_summe:
        labels.append("Erspartes")
        color_nodes.append(Color.GREEN)
        sources.append(labels.index("Erspartes"))
        targets.append(labels.index("Ausgaben"))
        values.append(ausgaben_summe - einkommen_summe)
        color_links.append(Color.YELLOW)

    fig = go.Figure(data=[go.Sankey(
        valueformat = ".2f",
        valuesuffix = " EUR",
        arrangement = "snap",
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = color_nodes
        ),
        link = dict(
            source = sources,
            target = targets,
            value = values,
            color = [Color.hex_to_rgba(c, Color.OPACITY) for c in color_links]
    ))])

    if config["debug"]:
        print(f"Einkommen: {einkommen}")
        print(f"Ausgaben: {ausgaben}")
        print("Tabelle:")
        print(sources)
        print(targets)
        print(values)

    if config["htmlOutput"]:
        fig.update_layout(hovermode="x", title_text=f"Sankey Diagram ({config['inputFile']})", font_size=18)
        fig.write_html("fig.html")
    else:
        fig.update_layout(hovermode="x", title_text=f"Sankey Diagram ({config['inputFile']})", font_size=10)
        fig.write_image("fig.jpeg")

if __name__ == '__main__':
    main()
