# Ask Jane

Ask Jane is the garden planner for [Saved by the Plate](https://savedbytheplate.org), a food-justice education nonprofit. This repository is the planner on its own: a Python library, an interactive command-line interview, and a FastAPI service. It was developed separately from the organization's site.

A plan is plain text. You give a location and a growing profile. Ask Jane combines that profile with a short weather forecast and the catalogs in this repository, then writes crop ideas, a bed sketch, watering notes, companions, care, and learning links.

The service version string in `api.py` is 4.2.0.

## What you get

`generate_plan` in `agi_agent/gardening/planner.py` assembles one document:

- Resolved place, coordinates, and timezone
- An estimated USDA hardiness zone and a typical last-spring / first-fall frost window
- A 7-day temperature and precipitation summary
- Layout tips for the method, space, and light you chose
- Up to 20 crop suggestions, with planting months and days to harvest when the timing catalog has that crop
- Yield notes, companion notes, and an ASCII bed layout
- Variety notes for suggested crops that have variety records
- A planting calendar and a care schedule
- An irrigation note when a soil type is set, from a local water-balance calculation on that 7-day forecast (Hargreaves-style reference evapotranspiration, following the shape of the [Cornell Climate Smart Farming water-deficit calculator](https://climatesmartfarming.org/tools/csf-water-deficit-calculator/))
- Succession-planting and cover-crop windows
- A 4-year rotation sketch, plus soil, care, maintenance, fertilization, and pruning notes
- Troubleshooting notes, common mistakes, and tips for the current season
- Disease-prevention notes for the suggested crops
- Regional climate-hub links, static future-climate tables for US regions, and stored assessment blurbs for New York and California
- Learning links filtered toward the stated experience level

Two optional inputs change the text when they are present:

- A local image path, used by the CLI, is reduced to brightness, a green-pixel share, and an edge-density estimate (`agi_agent/gardening/vision.py`).
- Air quality, solar, pollen, elevation, and aerial fields are summarized when the caller sends them. This service does not request those feeds itself.

The interview asks for location (address or coordinates), method, space, sunlight, experience, soil, crop interests, preferences, notes, and an optional image path. Methods include raised beds, containers, in-ground, vertical, indoor, rooftop, and hydroponic.

## Catalogs checked into this repository

These are the sizes of the Python catalogs, counted from the modules. They are not live external databases.

| Catalog | What it holds |
| --- | --- |
| `GET /api/crops` | 334 entries on a local run: 100 with variety records, 234 further names from the family catalog |
| `CROP_FAMILIES` | 298 crop keys in 21 botanical families |
| `VARIETY_DATABASE` | 100 crops, 108 variety records |
| `CROP_TIMING_DATABASE` | 289 crops |
| `COMPANION_DATABASE` | 160 crops, 578 listed companions and 210 listed plants to separate |
| `DISEASE_DATABASE` | 50 records across 17 crops (31 distinct names) |
| `FAMILY_DISEASES` | 400 family-level disease strings (311 unique), used by symptom matching |
| `RESOURCES_DATABASE` | 58 learning resources |
| `PLANTS` | 13 hand-written profiles that the recommender filters first |

Further suggestions are built from the family catalog. `recommend_plants` returns at most 20 names.

## Stack

- Python. `runtime.txt` asks for 3.11. The checks below also ran on 3.12.
- FastAPI 0.104.1, Uvicorn 0.24.0, Pydantic 2.5.0
- `requests` and `python-dotenv`
- NumPy and Pillow, for the optional image estimate
- pandas is listed in `requirements.txt`. The planner modules do not import it.
- [Open-Meteo](https://open-meteo.com/) forecast and ERA5 archive, both key-free
- [OpenStreetMap Nominatim](https://nominatim.org/) for addresses when `GOOGLE_MAPS_API_KEY` is empty
- Google Maps Geocoding when that key is set

No model SDK is imported. `agi_agent/core/agent.py` defines `AGIAgent`, an in-memory placeholder with a canned reply. The CLI imports that class and does not call it. Planning stays in `generate_plan`.

## Architecture

```mermaid
flowchart TD
  CLI[CLI interview]
  API[FastAPI]
  GEO[geocode_location]
  WX[fetch_simple_forecast]
  PLAN[generate_plan]
  CAT[Local catalogs]
  CLI --> GEO
  API --> GEO
  GEO --> NOM[Nominatim when no Google key]
  GEO --> GMAP[Google Maps when a key is set]
  CLI --> WX
  API --> WX
  WX --> OM[Open-Meteo forecast and ERA5]
  CLI --> PLAN
  API --> PLAN
  WX --> PLAN
  PLAN --> CAT
```

`api.py` exposes:

| Method | Path | Role |
| --- | --- | --- |
| GET | `/` | Service name, version, and endpoint list |
| GET | `/health` | Health check |
| GET | `/api/enums` | Form choices |
| GET | `/api/crops` | Crop catalog |
| POST | `/api/plan` | Garden plan |
| POST | `/api/v1/garden-plan/generate` | Same plan handler |
| POST | `/api/v1/disease/identify` | Symptom and crop-family match |
| GET | `/docs` | Interactive API docs |

Disease matching compares the crop family and the words you send with a local keyword list. Image fields are accepted on the request and left unused.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Generate a New York plan with coordinates, so no geocoding key is required:

```bash
python generate_sample_plan.py
```

Interactive interview:

```bash
python -m agi_agent.cli
```

An editable install also adds a `agi-agent` command (`pip install -e .`).

API, with docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs):

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Copy `.env.example` to `.env` only if you want to set something. Both names are blank in the example.

| Name | Role |
| --- | --- |
| `GOOGLE_MAPS_API_KEY` | Optional. Empty uses Nominatim for addresses and reverse lookup. |
| `PORT` | Port used when you start the API with `python api.py`. Uvicorn's `--port` flag overrides this. |

`.env` is gitignored. A forecast for coordinates works with both variables empty. Address lookup then uses Nominatim, which expects a identifiable User-Agent and light traffic.

Example plan request:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/garden-plan/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "address": "New York, NY",
    "method": "Raised Beds",
    "size": "Medium (balcony, small patio)",
    "experience": "Beginner (never grown anything before)",
    "crop_interests": ["Tomatoes", "Herbs (basil, parsley, cilantro, mint)"],
    "preferences": ["Low Maintenance"],
    "soil_type": "Medium (Loam, mixed)"
  }'
```

## Local run

Interactive docs from this machine, with the API listening on port 8000:

![Ask Jane API docs on a local run](docs/screenshots/api-docs.png)

The opening of a plan for New York, produced by `python generate_sample_plan.py` with no API key:

![Sample Ask Jane plan for New York](docs/screenshots/sample-plan.png)

## Project layout

```
api.py                          FastAPI app
generate_sample_plan.py         One New York plan, no prompts
agi_agent/cli.py                Interactive interview
agi_agent/core/agent.py         Unused in-memory placeholder
agi_agent/gardening/planner.py  Plan assembly
agi_agent/gardening/climate.py  Geocoding, forecast, zone, frost window
agi_agent/gardening/knowledge.py
agi_agent/gardening/*.py        Catalogs and section writers
```

Scripts named `test_v3_*.py`, `test_v4_phase_2.py`, `test_layout_generator.py`, and `demo_water_management.py` print feature checks. They are not a pytest suite.

Older notes in the repository root (`CHANGELOG_v3*`, `V4_ROADMAP.md`, `CURRENT_STATUS.md`, and similar files) record development as it happened. Several of their counts and completion claims differ from the catalogs above. Use this README for what the code does today.

## Contributors

From the git history:

- **Shay Bouchles** ([shaythegay13](https://github.com/shaythegay13)) — author and primary developer
- **Sabih Sarowar** ([kleenkanteen](https://github.com/kleenkanteen)) — local development notes

## License

This repository does not include a `LICENSE` file.

## Limits of the current code

- Drought status is a fixed record: no drought, labeled as a placeholder. It does not read the US Drought Monitor.
- Coastal risk is a latitude/longitude box check. Flood zone is a fixed placeholder. Both modules say so in their docstrings.
- Future-climate figures are static tables in `future_climate.py`.
- The hardiness zone is the coldest daily low in about eight years of Open-Meteo ERA5 data, mapped to a whole USDA zone number. It is an estimate, separate from the [official Plant Hardiness Zone Map](https://planthardiness.ars.usda.gov/).
- `PlanRequest` accepts `growing_location`, `time_commitment`, and garden-image fields. Plan generation does not read them.
- CORS in `api.py` allows every origin and allows credentials.
