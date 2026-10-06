# Darsxona

O‘qituvchi uchun shaxsiy CRM: guruhlar, shogirdlar, dars mavzulari, o‘tilgan darslar va yo‘qlama.

## Ishga tushirish

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py bootstrap
python manage.py runserver
```

Brauzerda: http://127.0.0.1:8000/

Kirish:

- login: `ustoz`
- parol: `darsxona2026`

`bootstrap` buyrug‘i namuna guruh, shogird, mavzu va darslarni ham yaratadi.
