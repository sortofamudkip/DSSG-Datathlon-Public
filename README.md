# DSSG Berlin 2021: ADFC Bike & Covid overlay map (Jake)

Wishyut (Jake Pita)'s contribution to the datathlon ADFC team.

## Introduction

For the datathlon, I created a simple web server (hosted on Heroku) to display an HTML file that displayed bike ridership and COVID information in Berlin on a Leaflet.js map.

## Features
* A map that shows the following information:
    * Boundaries of the boroughs of Berlin
    * Daily coronavirus incidence rate of each borough 
    * Bike stations and their respective daily rider statistics (provided by ADFC)
* A slider at the bottom of the page allows the user to see the **daily** statistics for the **incidence rate of each borough** and the **amount of riders at each station**.
* A "Jump to COVID start" button to move the slider to the date that COVID statistics were first recorded.

## Notes
* The website works best when viewed from a desktop browser, as some functions (namely the slider) may not work when browsing from a phone.
* This website was tested mostly on Chrome, though it should work on most other browsers.
* The word "district" and "borough" are used interchangably, but they both refer to the boroughs of Berlin (e.g. Mitte).

## Folder structure
The webpage is self-contained, i.e. it does not rely on any external API calls.

This project relies mainly on the following files:
* `app.py`, the web server
* `pages/maps.html`, the main HTML file (also contains CSS/JS/JS packages)
* `static/jquery.csv.min.js`, [a module for parsing CSV files](https://github.com/evanplaice/jquery-csv)
* `static/berlin_big_table.json`, the **daily** amount of bikes detected at each bike station in Berlin ([source](https://daten.berlin.de/datensaetze/covid-19-berlin-fallzahlen-und-indikatoren-gesamtübersicht))
* `static/berlin_covid.json`, **daily** incidence rate of each borough and 7-day incidence rate over all boroughs
* `static/berlin_bezirke.geojson`, [the GeoJson files](https://github.com/funkeinteraktiv/Berlin-Geodaten/blob/master/berlin_bezirke.geojson) for drawing Berlin's boroughs 
* `static/fetched_eco_bike_data-overall_germany.csv`, the names and positions of each bike station in Berlin

## Methodology / Implementation
This section mainly explains how the Javascript part of `maps.html` works. The file itself also has detailed comments on how each section works.

### Loading data & creating the map
1. The data from `fetched_eco_bike_data-overall_germany.csv` is loaded.  
    1.1. As `fetched_eco_bike_data-overall_germany.csv` contains the positions and names of the bike stations, the map is created once this data is loaded and the bike stations are plotted. (To view the markers in JS, simply type `markers` into the browser's console.)
2. The coronavirus data for Berlin is loaded from `berlin_covid.json`. (To view this data in JS, type `berlin_covid` into the console.)
3. The bike rider information from `berlin_big_table.json` is loaded. (To view this data in JS, type `daily_riders` into the console.)
4. The polygon data for each of Berlin's boroughs are loaded from `berliner-bezirke.geojson`, and a tooltip (which will later display coronavirus information) is bound to each polygon.

Note that though each file is loaded asynchronously, the script will wait for all 4 files to finish loading before proceeding.

### The slider
JQuery UI's `slider` is used as a quick and easy slider. 

The slider itself can only take integers (to my knowledge), and thus it is necessary to convert dates (e.g. "2021-01-12") to integers. To this end, we define the slider values (0, 1, 2, ...) as **the number of days passed since 2016-01-01**, which is the first day of the bike ridership statistics.

Naturally, the minimum value of the slider is 0 (i.e. 0 days past 2016-01-01), and the maximum value is 2021-09-29, the final day of bike statistics. 

Note that the 2016-01-01 value was hardcoded due to the time limit of the datathlon, but it is recommended to find this programmatically. 

Now, whenever the slider is moved, we simply take its value (an integer) and translate it to its corresponding date. For example, since 2016-01-01 is defined as the starting date, a slider value of 5 would refer to 2016-01-06, i.e. 5 days after the earliest date.

We can then use this date to obtain the bike data (`daily_riders`) and covid data (`berlin_covid`) of each day.

After obtaining the bike and covid data of a specific day, we can obtain and display the respective information on the map.

## The `daily_riders` structure
The structure of `daily_riders` is:
```jsonc
{
    "YYYY-MM-DD" : { // day of bike statistics
        "Berlin_1": <int>, // id of bike station : number of riders at station that day
        "Berlin_2": <int>,
        ...,
        "Berlin_16": <int>,
    },
    ...
}
```

Example:
```jsonc
{
    "2016-01-01": {
        "Berlin_1": 420,
        "Berlin_2": 547,
        "Berlin_5": 303,
        "Berlin_8": 294,
        "Berlin_9": 165,
        "Berlin_12": 629,
        "Berlin_13": 91,
        "Berlin_14": 702,
        "Berlin_15": 172,
        "Berlin_16": 1620
    },
    ...
}
```

## The `berlin_covid` structure
The structure of `berlin_covid` is:
```jsonc
{
    "YYYY-MM-DD" : { // day of covid statistics
        "mitte": <int|null>,  // borough name : incidence rate (int or null)
        "friedrichshain_kreuzberg": <int|null>, // null means there was no information recorded
        "pankow": <int|null>, 
        "charlottenburg_wilmersdorf": <int|null>,
        "spandau": <int|null>,
        "steglitz_zehlendorf": <int|null>,
        "tempelhof_schoeneberg": <int|null>,
        "neukoelln": <int|null>,
        "treptow_koepenick": <int|null>,
        "marzahn_hellersdorf": <int|null>,
        "lichtenberg": <int|null>,
        "reinickendorf": <int|null>,
        "7_days_incidence": <int|null>, // 7 days incidence rate over ALL boroughs
    },
    ...
}
```

Example:
```jsonc
{
    "2020-03-16" : {
        "mitte": 4,
        "friedrichshain_kreuzberg": 6,
        "pankow": 14,
        "charlottenburg_wilmersdorf": 7,
        "spandau": null,
        "steglitz_zehlendorf": 6,
        "tempelhof_schoeneberg": 6,
        "neukoelln": 2,
        "treptow_koepenick": 4,
        "marzahn_hellersdorf": 1,
        "lichtenberg": 6,
        "reinickendorf": 7,
        "7_days_incidence": 7
    },
    ...
}
```

## Website link
Link to the website: https://datathlon-bikes.herokuapp.com/bike_stations 

With the code in this repository, it is also possible to self-host your own Flask server to view this website. 

## Possible extensions
As this project was completed in about 12 hours, it is not meant to be a final product. The following are suggestions on how to extend or improve this project.

* Double sliders, one for COVID data and one for bike data.
* More buttons (e.g. "show/hide COVID data", "show/hide bike data", FAQ button).
* Improve slider CSS / add more functionality.
* Reduce the amount of text, i.e. improve readability of map.
* Use external APIs to obtain more up-to-date information (though this will probably come at the cost of performance, as the user will have to wait for the data to arrive).
* Dedicated server to store bike/covid information (i.e. not JSON files). A cron job can be run to regularly update the database.