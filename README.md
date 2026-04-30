# MediFind

A FastAPI + vanilla frontend medicine finder and price comparison demo.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open:

- `http://127.0.0.1:8000/`

## What is included

- Medicine search by brand, generic, and symptom
- City and availability filters
- Price comparison across pharmacies
- Favorite medicines stored in SQLite
- Community reporting for suspicious pricing
- Usage guidance and generic alternatives

