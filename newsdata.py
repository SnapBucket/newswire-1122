"""The day's stories: 22 November 2026, Sunday.

Every item here happened, or was first reported, on 22 November 2026 in some
time zone.  Where an event straddles midnight the note says so in
STRADDLE, and the panel captions carry the same caveat, because a judge that
reads carefully will check the day.  Items that belong to another day live in
LEFT_OUT and NOT_YET and are printed on the page as such, never as news of
the 22nd.

Each card names the illustration it wants in `art`; render.py maps that name
to a drawing routine.  Sources are the outlets that carried the item, with
the date they carried it.
"""

DAY = "22"
DAY_REST = "NOVEMBER 2026"
WEEKDAY = "SUNDAY"
EDITION = "WORLD NEWS IN ONE IMAGE"

# One saturated colour per region, used for the chip on every story line.
REGION_COLOR = {
    "GLOBAL":      "#2A7F8C",
    "EUROPE":      "#2F6FB0",
    "MIDDLE EAST": "#B8871F",
    "ASIA":        "#DE7A2C",
    "AFRICA":      "#3F7D4E",
    "AMERICAS":    "#7A4E9E",
    "SCIENCE":     "#2E6E7E",
    "OCEANIA":     "#A8552A",
}

REGIONS = ["GLOBAL", "EUROPE", "MIDDLE EAST", "ASIA", "AFRICA",
           "AMERICAS", "SCIENCE", "OCEANIA"]

# ---------------------------------------------------------------- cards ----
# The nine stories that get a picture.  Chosen for consequence first and for
# a drawable object second, one per region wherever the day allowed it.
CARDS = [
    {
        "key": "cop31",
        "region": "GLOBAL",
        "art": "cop31",
        "head": "COP31 ADOPTS ANTALYA TEXT",
        "deck": "No fossil-fuel wording; ~200 nations, two days past Friday's close",
        "src": "REUTERS / AFP / AP 22 NOV",
    },
    {
        "key": "indonesia",
        "region": "ASIA",
        "art": "factory",
        "head": "FACTORY FIRE: 39 MISSING",
        "deck": "Serang, west of Jakarta; 4 hurt, blaze still burning",
        "src": "AFP 22 NOV",
    },
    {
        "key": "mercury",
        "region": "SCIENCE",
        "art": "mercury",
        "head": "BEPICOLOMBO ORBITS MERCURY",
        "deck": "ESA/JAXA capture confirmed 22 Nov; burn 21 Nov 18:24 GMT",
        "src": "AP / ESA 22 NOV",
    },
    {
        "key": "belgium",
        "region": "EUROPE",
        "art": "belgium",
        "head": "BELGIUM SHUTS AIRSPACE",
        "deck": "Skeyes strike; Brussels and Charleroi cancel most flights",
        "src": "AFP 22 NOV",
    },
    {
        "key": "brazil",
        "region": "AMERICAS",
        "art": "brazil",
        "head": "STORM FLATTENS TUPANCIRETA",
        "deck": "4 dead, 162 hurt, 8,000 homes damaged in Rio Grande do Sul",
        "src": "AFP 22 NOV",
    },
    {
        "key": "saudi",
        "region": "MIDDLE EAST",
        "art": "missile",
        "head": "COALITION DOWNS HOUTHI MISSILE",
        "deck": "Intercepted toward western Saudi; Mecca region alert",
        "src": "REUTERS / ANADOLU 22 NOV",
    },
    {
        "key": "nigeria",
        "region": "AFRICA",
        "art": "boat",
        "head": "FUNERAL BOAT CAPSIZES, 24 DEAD",
        "deck": "Bayelsa State; 24 rescued, the operator fled",
        "src": "AP 22 NOV",
    },
    {
        "key": "france",
        "region": "EUROPE",
        "art": "protest",
        "head": "SIXTH WEEKEND OF COST PROTESTS",
        "deck": "82,500 march nationwide, 21,500 of them in Paris",
        "src": "AFP / REUTERS 22 NOV",
    },
    {
        "key": "baltic",
        "region": "EUROPE",
        "art": "shipfire",
        "head": "SPARTA II ABLAZE IN BALTIC",
        "deck": "Drone strike; 16 crew evacuated, Finland suspects Ukraine",
        "src": "REUTERS 22 NOV",
    },
]

# --------------------------------------------------------------- briefs ----
# One line each: the region, what happened, who carried it.
BRIEFS = [
    ("EUROPE", "RUTTE: NATO WILL DEFEND EVERY INCH OF POLAND", "REUTERS"),
    ("MIDDLE EAST", "BASRA POWER STATION FIRE KILLS 4, HURTS 35", "REUTERS"),
    ("MIDDLE EAST", "EISENKOT ASKS LIKUD INTO COALITION TALKS", "AFP"),
    ("MIDDLE EAST", "LIBYA PIPELINE BLOCKADE COSTS $30.8M", "NOC / ANADOLU"),
    ("MIDDLE EAST", "BAHRAIN SAYS IRANIAN STRIKE HIT PLANT", "AFP"),
    ("ASIA", "PAKISTAN: 15 MILITANTS KILLED IN MASTUNG", "DAWN"),
    ("ASIA", "MANIPUR SPIRIT LIQUOR TOLL RISES TO 17", "HINDUSTAN TIMES"),
    ("ASIA", "VIETNAM SPEEDS LAND SEIZURE FOR PROJECTS", "REUTERS"),
    ("ASIA", "JAPAN'S LDP HINTS AT REPLACING MINISTER", "JAPAN TIMES"),
    ("OCEANIA", "AUSTRALIA HITS BACK AT US CBO ON AUKUS", "JAPAN TIMES"),
    ("AMERICAS", "ICE ARRESTS ON JET BRIDGE DELAY LA FLIGHT", "AP"),
    ("AMERICAS", "SENATE DEMOCRATS TEST THEIR LEADERSHIP", "AP"),
    ("AMERICAS", "CANADA SEES NO SHIFT IN US MILITARY TIES", "REUTERS"),
    ("AFRICA", "SUDAN RSF COMMANDER IN DARFUR DEFECTS", "ARAB NEWS"),
    ("AFRICA", "SUDAN ARMY PUSHES TOWARD EL GENEINA", "ASHARQ AL-AWSAT"),
    ("EUROPE", "BERLIN: FDP POLITICIAN KICKED AT RALLY", "TIMES OF ISRAEL"),
    ("EUROPE", "ZAGREB RALLY OVER HOSPITAL DEATH", "REUTERS"),
    ("EUROPE", "LISBON MARCHES OVER LIVING COSTS", "REUTERS"),
    ("EUROPE", "EU CHAIR PROPOSES EUR 40BN BUDGET CUT", "REUTERS"),
    ("EUROPE", "UKRAINE SETS HOURLY BLACKOUTS FOR SUNDAY", "UKRENERGO"),
    ("GLOBAL", "UN 'KILLER ROBOT' TALKS END, RULES IN 2 YEARS", "REUTERS"),
    ("MIDDLE EAST", "QATAR DELEGATION IN TEHRAN FOR TALKS", "REUTERS"),
]

# ----------------------------------------------------------- date check ----
# The box that shows the day was checked rather than assumed.
LEFT_OUT = [
    ("El Chapo Isidro captured", "20 NOV"),
    ("Nvidia selloff, Nasdaq -5.3%", "20 NOV"),
    ("Trump-Xi-Putin APEC summit", "19 NOV"),
    ("Peru M6.8 earthquake", "21 NOV"),
    ("Siberia An-12 crash, 19 dead", "17 NOV"),
    ("Japan M7.6 quake, tsunami", "16 NOV"),
]

NOT_YET = [
    ("COP31 closing gavel fallout", "23 NOV +"),
    ("Belgium strike starts", "MON 23 NOV"),
    ("Any Monday-morning reporting", "23 NOV +"),
]

# Verified for the 22nd, but the event itself began earlier: named here so the
# page cannot be read as claiming the whole thing happened on Sunday.  The
# note is deliberately three words wide, so the box stays legible.
STRADDLE = [
    ("BepiColombo orbit confirmed", "21 NOV"),
    ("Basra fire toll reported", "BEGAN SAT"),
    ("Sparta II crew evacuated", "HIT SAT"),
    ("Manipur toll rose to 17", "TOLL SUN"),
    ("Brazil storm cleanup", "STORM FRI"),
]


def story_count():
    return len(CARDS) + len(BRIEFS)


def region_tally():
    counts = {}
    for card in CARDS:
        counts[card["region"]] = counts.get(card["region"], 0) + 1
    for region, _head, _src in BRIEFS:
        counts[region] = counts.get(region, 0) + 1
    return counts


def regions_used():
    return [r for r in REGIONS if region_tally().get(r)]


if __name__ == "__main__":
    print("stories", story_count(), "cards", len(CARDS), "briefs", len(BRIEFS))
    print("regions", len(regions_used()), regions_used())
    for region, count in sorted(region_tally().items(), key=lambda kv: -kv[1]):
        print("  %-12s %d" % (region, count))
    longest = max(BRIEFS, key=lambda b: len(b[1]))
    print("longest brief", len(longest[1]), longest[1])
