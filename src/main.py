import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib as mpl
import math

COUNTIES = {
    "Flagler": {
        "shapefile": "./data/boundaries/Flagler/PRECINCTGRP12035_region.shp",
        "precincts": ["101", "102", "103", "201", "202", "401", "501", "502", "503", "504", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515"],
        "precinct_col": "PRECINCT",
        "results_csv": "./data/votes/Flagler/results.csv"
    },
    "Lake": {
        "shapefile": "./data/boundaries/Lake/Votingprecincts.shp",
        "precincts": ["300", "320", "325", "330", "335", "355", "400", "405", "410", "415", "420", "425", "430", "435", "440", "445", "450", "455", "465", "470", "475", "480", "485", "490", "500", "505", "510", "515", "520", "525"],
        "precinct_col": "Precinct",
        "results_csv": "./data/votes/Lake/results.csv"
    },
    "Marion": {
        "shapefile": "./data/boundaries/Marion/2023 Marion Precincts.shp",
        "precincts": ["0040", "1000", "1010", "1020", "1021", "1030", "1040", "1050", "1060", "1070", "1080", "1090", "1100", "1110", "3000", "3010", "3020", "3030", "3040", "3050", "3060", "3070", "3080", "3090", "3110", "3120", "3130", "3140", "3150", "3170", "3180", "3190", "3200", "3210", "3220", "3230", "3240", "3250", "3260", "3270", "3280", "3290", "3300", "3310", "3320"],
        "precinct_col": "NAME",
        "results_csv": "./data/votes/Marion/results.csv"
    },
    "Putnam": {
        "shapefile": "./data/boundaries/Putnam/Voting_Precincts_hub.shp",
        "precincts": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37"],
        "precinct_col": "PRECINCTID",
        "results_csv": "./data/votes/Putnam/results.csv"
    },
    "St Johns": {
        "shapefile": "./data/boundaries/St Johns/PRECINCTGRP_12109_2022.shp",
        "precincts": ["212", "213", "303.0", "303.1", "304", "305.0", "306.0", "306.1", "307.1", "308.0", "309", "310.0", "310.1", "311"],
        "precinct_col": "PCT_W_GRP",
        "results_csv": "./data/votes/St Johns/results.csv"
    },
    "Volusia": {
        "shapefile": "./data/boundaries/Volusia/Election_Precincts.shp",
        "precincts": ["101", "102", "103", "104", "105", "201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "214", "215", "216", "501", "502", "503", "504", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515", "516", "517", "518", "519", "520", "521", "601", "602", "603", "604", "605", "606", "607", "608", "609", "610", "611", "612", "613", "614", "615", "616", "617", "618", "619", "620", "621", "622", "623", "624", "625", "701", "702", "814"],
        "precinct_col": "Precinct_1",
        "results_csv": "./data/votes/Volusia/results.csv"
    }
}

PATHS_TO_SHAPEFILES = {
    "Florida": "./data/boundaries/Florida/Detailed_Florida_State_Boundary.shp",
    "Flagler": "./data/boundaries/Flagler/PRECINCTGRP12035_region.shp",
    "Lake": "./data/boundaries/Lake/Votingprecincts.shp",
    "Marion": "./data/boundaries/Marion/2023 Marion Precincts.shp",
    "Putnam": "./data/boundaries/Putnam/Voting_Precincts_hub.shp",
    "St Johns": "./data/boundaries/St Johns/PRECINCTGRP_12109_2022.shp",
    "Volusia": "./data/boundaries/Volusia/Election_Precincts.shp"
}

PATHS_TO_VOTES = {
    "Flagler": "./data/votes/Flagler/results.csv",
    "Lake": "./data/votes/Lake/results.csv",
    "Marion": "./data/votes/Marion/results.csv",
    "Putnam": "./data/votes/Putnam/results.csv",
    "St Johns": "./data/votes/St Johns/results.csv",
    "Volusia": "./data/votes/Volusia/results.csv"
}

PRECINCTS = {
    "Flagler": ["101", "102", "103", "201", "202", "401", "501", "502", "503", "504", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515"],
    "Lake": ["300", "320", "325", "330", "335", "355", "400", "405", "410", "415", "420", "425", "430", "435", "440", "445", "450", "455", "465", "470", "475", "480", "485", "490", "500", "505", "510", "515", "520", "525"],
    "Marion": ["0040", "1000", "1010", "1020", "1021", "1030", "1040", "1050", "1060", "1070", "1080", "1090", "1100", "1110", "3000", "3010", "3020", "3030", "3040", "3050", "3060", "3070", "3080", "3090", "3110", "3120", "3130", "3140", "3150", "3170", "3180", "3190", "3200", "3210", "3220", "3230", "3240", "3250", "3260", "3270", "3280", "3290", "3300", "3310", "3320"],
    "Putnam": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37"],
    "St Johns": ["212", "213", "303.0", "303.1", "304", "305.0", "306.0", "306.1", "307.1", "308.0", "309", "310.0", "310.1", "311"],
    "Volusia": ["101", "102", "103", "104", "105", "201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "214", "215", "216", "501", "502", "503", "504", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515", "516", "517", "518", "519", "520", "521", "601", "602", "603", "604", "605", "606", "607", "608", "609", "610", "611", "612", "613", "614", "615", "616", "617", "618", "619", "620", "621", "622", "623", "624", "625", "701", "702", "814"]
}

PRECINCT_COLUMN_NAMES = {
    "Flagler": "PRECINCT",
    "Lake": "Precinct",
    "Marion": "NAME",
    "Putnam": "PRECINCTID",
    "St Johns": "PCT_W_GRP",
    "Volusia": "Precinct_1"
}

colors = ["royalblue", "cornflowerblue", "lightskyblue", "lightslategray", "rosybrown", "pink", "lightcoral", "crimson"]
cmap = ListedColormap(colors)
bounds = [-20, -15, -10, -5, 0, 5, 10, 15, 20]
norm = BoundaryNorm(bounds, cmap.N)

def _calculate_margin(precinct_results):
    pass

def _load_shapefile(path_to_shapefile, precincts=None, precinct_col=None, path_to_results=None):
    shp = gpd.read_file(path_to_shapefile)
    shp = shp.to_crs(epsg=4326)

    # Selects only the precincts in FL-06
    if precincts:
        shp[precinct_col] = shp[precinct_col].map(str)
        shp = shp[shp[precinct_col].isin(precincts)]

        if path_to_results:
            results = pd.read_csv(path_to_results, converters={'Precinct Name': str})
            results["Early Votes"] = pd.to_numeric(results["Early Votes"], errors="coerce")

            for precinct in precincts:
                if results[results["Precinct Name"] == precinct].empty:
                    temp_precinct = str(math.trunc(float(precinct)))
                    if results[results["Precinct Name"] == temp_precinct].empty:
                        print(f"No results found for precinct {precinct}")
                        continue
                    else:
                        precinct_results = results[results["Precinct Name"] == temp_precinct]
                else:
                    precinct_results = results[results["Precinct Name"] == precinct]
                
                if precinct_results["Early Votes"].astype(str).str.contains("-").any():
                    margin = 0
                else:
                    rep_total = precinct_results.loc[precinct_results["Party"] == "REP", "Early Votes"].values
                    dem_total = precinct_results.loc[precinct_results["Party"] == "DEM", "Early Votes"].values
                    rep_total = rep_total[0] if len(rep_total) > 0 else 0
                    dem_total = dem_total[0] if len(dem_total) > 0 else 0
                    total = precinct_results["Early Votes"].sum()
                    print(path_to_results, precinct, rep_total, dem_total, total)
                    margin = (rep_total / total) * 100 - (dem_total / total) * 100
                shp.loc[shp[precinct_col] == precinct, "Margin"] = margin
    
    return shp

def plot_map():
    # Loads the shapefiles of the state and relevant counties
    florida = _load_shapefile(PATHS_TO_SHAPEFILES["Florida"])
    flagler_p = _load_shapefile(PATHS_TO_SHAPEFILES["Flagler"], PRECINCTS["Flagler"], PRECINCT_COLUMN_NAMES["Flagler"], PATHS_TO_VOTES["Flagler"])
    lake_p = _load_shapefile(PATHS_TO_SHAPEFILES["Lake"], PRECINCTS["Lake"], PRECINCT_COLUMN_NAMES["Lake"], PATHS_TO_VOTES["Lake"])
    marion_p = _load_shapefile(PATHS_TO_SHAPEFILES["Marion"], PRECINCTS["Marion"], PRECINCT_COLUMN_NAMES["Marion"], PATHS_TO_VOTES["Marion"])
    putnam_p = _load_shapefile(PATHS_TO_SHAPEFILES["Putnam"], PRECINCTS["Putnam"], PRECINCT_COLUMN_NAMES["Putnam"], PATHS_TO_VOTES["Putnam"])
    stjohns_p = _load_shapefile(PATHS_TO_SHAPEFILES["St Johns"], PRECINCTS["St Johns"], PRECINCT_COLUMN_NAMES["St Johns"], PATHS_TO_VOTES["St Johns"])
    volusia_p = _load_shapefile(PATHS_TO_SHAPEFILES["Volusia"], PRECINCTS["Volusia"], PRECINCT_COLUMN_NAMES["Volusia"], PATHS_TO_VOTES["Volusia"])

    # Plot the map
    fig, ax = plt.subplots(figsize=(10, 10))
    florida.plot(ax=ax, edgecolor="black", color="gainsboro")

    counties = [flagler_p, lake_p, marion_p, putnam_p, stjohns_p, volusia_p]
    for county in counties:
        county.plot(ax=ax, edgecolor="black", color="black")
        # county[county["Margin"] == 0].plot(ax=ax, edgecolor="black", color="gainsboro")
        county[county["Margin"] != 0].plot(column="Margin", ax=ax, edgecolor="black", cmap=cmap, norm=norm)

    # Add legend only once
    volusia_p.plot(column="Margin", ax=ax, edgecolor="black", cmap=cmap, norm=norm, legend=True)

    # Set the bounds of the map so it's focused on FL-06 and not the entire state
    padding = 0.05
    ax.set_facecolor("paleturquoise")
    ax.set_xlim(marion_p.total_bounds[0] - padding, volusia_p.total_bounds[2] + padding)  # minX, maxX
    ax.set_ylim(lake_p.total_bounds[1] - padding, stjohns_p.total_bounds[3] + padding)  # minY, maxY

    plt.title("FL-06 House of Representatives 2024 Election, Margin per Precinct (Early Votes)")
    plt.tight_layout()
    plt.show()


def main():
    plot_map()

main()