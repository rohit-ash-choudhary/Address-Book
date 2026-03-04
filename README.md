# Address Book API

Simple REST API for addresses. Create/read/update/delete, optional geocoding (street + city → lat/lon), and distance between two points.

## Run it

Python 3.10+ and pip.


Make Folder Address-Book
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


Open http://127.0.0.1:8000/docs for the interactive API docs.

## Optional: .env

If you need to change defaults, add a `.env` in the project root:

```
DATABASE_URL=sqlite:///./addresses.db
LOG_LEVEL=INFO


## Main endpoints

- `GET /addresses/` – list all
- `POST /addresses/` – create (name, street, city required; lat/lon optional, will geocode if missing)
- `GET /addresses/{id}` – get one
- `PUT /addresses/{id}` – update
- `DELETE /addresses/{id}` – delete
- `GET /addresses/distance?from_id=1&to_id=2` – distance in km (or use `to_lat` and `to_lon` instead of `to_id`)

## Quick test

curl -X POST "http://127.0.0.1:8000/addresses/" \
-H "Content-Type: application/json" \
-d "{\"name\":\"Delhi Home\",\"street\":\"Connaught Place\",\"city\":\"New Delhi\",\"latitude\":28.6315,\"longitude\":77.2167}"

