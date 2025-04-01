import requests
import pandas as pd
import matplotlib
import folium
from datetime import datetime as dt
import sys

def download():
    resp = requests.get("http://www.datiopen.it/export/csv/Mappa-dei-telefoni-pubblici-in-Italia.csv")
    if resp.ok:
        data = resp.text
        f = open("input.csv", "w")
        f.write(data)
        f.close()

def createPlots(regionname, dfprovincia):
    plot = dfprovincia.plot(kind="pie", y="Provincia")
    fig = plot.get_figure()
    fig.savefig("itphones_outputs/" + regionname + ".png")
    fig.clear()

timeoffset = -8
timeperiod = 2
center = (41.902782, 12.496366)
bounds = [[46.62115209225544, 5.669698244577547],[36.04096044837196, 21.97861416589663]]
colors = ["darkgreen","green","orange","red"]

if len(sys.argv) > 1:
    timeoffset = int(sys.argv[1])

if len(sys.argv) > 2:
    timeperiod = int(sys.argv[2])

if len(sys.argv) == 7 :
    bounds = [[float(sys.argv[3]),float(sys.argv[4])],[float(sys.argv[5]),float(sys.argv[6])]]

print(timeoffset, timeperiod, bounds)

print("Downloading data from  IT open data")
download()

print("Parsing CSV into pandas")
df = pd.read_csv("input.csv", sep=";")

print("Extracting region names")
regioni = df["Regione"].unique()

for reg in regioni:
    dfregione = df[df["Regione"] == reg]
    dfprovincia = dfregione.groupby("Provincia")["Provincia"].count()
    print("Generating pie charts for", reg)
    createPlots(reg, dfprovincia)

print("Initializing map with center ", center, "and bounds", bounds)
m = folium.Map(center, zoom_start=7)
m.fit_bounds(bounds)

print("Extracting lt/lon coordinates from dataframe")
locations = list(zip(df["Latitudine"], df["Longitudine"]))
for i in range(len(locations)):
    loc = locations[i]
    isinside = (loc[0] <= bounds[0][0] and loc[0] >= bounds[1][0]) and (loc[1] >= bounds[0][1] and loc[1] <= bounds[1][1])
    if isinside:
        insdate = int(df["Anno inserimento"][i])
        agecolorindex = min(3, (dt.now().year + timeoffset - insdate) // timeperiod)
        color = colors[agecolorindex]
        icon = folium.Icon(color=color, fill_color=color)
        folium.Marker([loc[0], loc[1]], icon=icon).add_to(m)

print("Saving HTML file")
m.save("itphones_outputs/index.html")
    