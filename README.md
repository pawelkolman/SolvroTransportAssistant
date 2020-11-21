<div align="center">
<h1>Solvro Transport Assistant</h1>
  <img src="./main/static/img/SolvroTransportAssistant_logo.png" height="200">
</div>


## Table of contents:
- [General info](#general)
- [Technologies](#technologies)
- [Live version](#live)
- [Features](#features)
- [API](#api)
- [Problem solution](#solution)


<a name="general"></a>
## General info
This is a simple application that searches for the shortest route between two stops in Solvro City, created for the purposes of recruitment to KN Solvro.


<a name="technologies"></a>
## Technologies
- Python, Django
- HTML, CSS, Bootstrap


<a name="live"></a>
## Live version
Live version of this app is available [here](https://SolvroTransportAssistant.pythonanywhere.com).


<a name="features"></a>
## Features
- Sign up
- Log in
- All available stops preview
- Stops list API
- Find the shortest route between two stops form and result preview
- Shortest route API
- Add and show favourites routes
- City map graph visualization


<a name="api"></a>
## API
### stops
Available at [api/stops](https://SolvroTransportAssistant.pythonanywhere.com/api/stops). Returns a JSON array with available stops names as in the example below:
```
[
  {
    "name": "Przystanek Zdenerwowany kabanos"
  },
  {
    "name": "Przystanek Dziki student PWr"
  }
]
```
### path
Available at [api/path](https://SolvroTransportAssistant.pythonanywhere.com/api/path?source=Przystanek%20Zdenerwowany%20programista&target=Przystanek%20Cudowny%20student%20PWr). Expects `source` and `target` as string GET parameters. Returns a JSON containing stops and total distance as in the example below:
```
{
  "stops": [
    {
      "name": "Przystanek Zasmucony muczaczo"
    },
    {
      "name": "Przystanek Zdenerwowany jamnik"
    },
    {
      "name": "Przystanek Cudowny programista"
    }
  ],
  "distance": 36
}
```


<a name="solution"></a>
## Solution
Crucial code is located in [solvro_city.py](./scripts/solvro_city.py). The city map is an undirected weighted graph, therefore the shortest path can be determined with the Dijkstra's algorithm.