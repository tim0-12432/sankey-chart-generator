configuration = {
    # csv export of bank account
    "inputFile": "Umsatz-Example.csv",
    # month to analyze (0 = all)
    "filterMonth": 0,
    # html should be generated (otherwise just jpeg)
    "htmlOutput": True,
    # list of names to be considered as income
    "einkommen": [
        "Musterunternehmen"
    ],
    # list of names to be considered as expenses
    "ausgaben": {
        "nahrungsmittel": [
            "Lidl",
            "Rewe",
            "Aldi",
            "Kaufland",
            "Real",
            "Netto",
            "Edeka",
            "MCDonalds"
        ],
        "hygiene": [
            "Muller",
            "Tedi",
            "Rossmann",
            "Dm"
        ],
        "transport": [
            "DB"
        ],
        "internet": [
            "Internetanbieter",
            "Allnet"
        ],
        "miete": [
            "Immobilien",
            "ARD"
        ],
        "shopping": [
            "AMAZON",
            "Ebay",
            "PayPal",
            "PUSTET",
            "SATURN"
        ]
    },
    # debugging information
    "debug": False
}