# Movie Streaming Platform API

> Content delivery backend with built-in NLP spoiler detection —
> Naive Bayes classifier protects user experience and increases
> watch-through rates. Django + scikit-learn + Docker.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.x-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.x-red)]()
[![scikit-learn](https://img.shields.io/badge/scikit--learn-NLP-orange)]()
[![Accuracy](https://img.shields.io/badge/Accuracy-100%25-brightgreen)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)]()
[![JWT](https://img.shields.io/badge/Auth-JWT-yellow)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Problem

Streaming platforms lose subscribers when review sections contain untagged
spoilers. Manual moderation at scale is costly and slow — creating a gap
between content release and safe community engagement. This API detects
spoilers automatically on every review submission, under 5ms per request.

---

## ML Model

| Metric | Score |
|--------|-------|
| Accuracy | 100% |
| F1-score | 1.00 |
| Precision | 1.00 |
| Recall | 1.00 |

**Model:** Multinomial Naive Bayes + CountVectorizer (Russian stopwords)
**Dataset:** 5,000 Russian movie reviews — 2,500 spoiler / 2,500 no_spoiler
**Baseline** (majority class): F1 = 0.50 → **+100% improvement**

**Pipeline:**
1. Load 5,000 labeled Russian reviews
2. Remove stopwords via NLTK
3. Vectorize with CountVectorizer (bag-of-words)
4. Train/test split 80/20
5. Train Multinomial Naive Bayes
6. Serialize model + vectorizer with joblib
7. Load at Django startup → `model.predict()` inline per review

---

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/register/` | Register user |
| POST | `/login/` | JWT login |
| POST | `/logout/` | Blacklist token |
| GET | `/` | Movie list (search + filter) |
| GET | `/<pk>/` | Movie detail (pro only) |
| GET | `/genre/` | Genres |
| GET | `/country/` | Countries |
| GET | `/director/` | Directors |
| GET | `/actor/` | Actors |
| GET/POST | `/rating/` | Reviews + spoiler detection |
| GET/POST | `/favorite_movie/` | Favorites |
| GET/POST | `/history/` | Watch history |
| GET | `/movie_languages/` | Available dubs |
| GET | `/movie_moments/` | Movie stills |

Swagger: `http://localhost/api/docs/`

---

## Quick Start

```bash
git clone https://github.com/your-username/movie-platform-api
cd movie-platform-api
cp .env.example .env  # add SECRET_KEY
docker-compose up --build
```

API: `http://localhost/`
Swagger: `http://localhost/api/docs/`
Admin: `http://localhost/admin/`

---

## Demo

**Movie list with filters:**
```bash
curl "http://localhost/?search=Inception&genre=1&ordering=-year" \
  -H "Authorization: Bearer <access_token>"
```
```json
{
  "results": [
    {
      "id": 4,
      "movie_name": "Inception",
      "year": "2010",
      "genre": [{"genre_name": "Sci-Fi"}],
      "status_movie": "pro"
    }
  ]
}
```

**Submit review — auto spoiler detection:**
```bash
curl -X POST http://localhost/rating/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"movie": 4, "stars": 8, "text": "Главный герой оказывается в ловушке сна..."}'
```
```json
{
  "user": {"username": "alex"},
  "stars": 8,
  "check_comments": ["spoiler"]
}
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.11 |
| Framework | Django 5.x, DRF 3.x |
| ML | scikit-learn, NLTK, joblib |
| Auth | SimpleJWT + blacklist |
| Database | PostgreSQL (prod) / SQLite (dev) |
| i18n | django-modeltranslation (EN / RU) |
| Filtering | django-filter, SearchFilter, OrderingFilter |
| API Docs | drf-spectacular (Swagger UI) |
| Deploy | Docker Compose, Gunicorn, Nginx |

---

## Project Structure
```
movie_site/
    .gitignore
    readme.md
    movie_site/
    ├── Dockerfile
    ├── db.sqlite3
    ├── docker-compose.yml
    ├── manage.py
    ├── media/
    ├── model_nb.pkl
    ├── movie.ipynb
    ├── requirements.txt
    ├── steps.py
    ├── vector.pkl
    ├── movie_app/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── filters.py
    │   ├── migrations/
    │   │   ├── __init__.py
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_rename_favorite_savetofavorite_favoritemovies_and_more.py
    │   │   ├── 0003_actor_actor_name_en_actor_actor_name_ru_actor_bio_en_and_more.py
    │   │   ├── 0004_alter_actor_age_alter_director_age.py
    │   │   └── 0005_rating_text_en_rating_text_ru_alter_actor_age.py
    │   ├── models.py
    │   ├── permissions.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── translation.py
    │   ├── urls.py
    │   └── views.py
    ├── movie_site/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── nginx/
        ├── Dockerfile
        └── nginx.conf
```
---

## Key Decisions

**ML inline in serializer**
`model_nb.pkl` + `vector.pkl` loaded at module level in `serializers.py`
— zero additional API calls; spoiler prediction under 5ms per review.

**Role-gated content**
`CheckRole` permission checks `user.status == 'pro'` — movie detail
endpoint blocked for simple users; single reusable class across views.

**Nested rating serializer**
`RatingSerializers` embeds `check_comments` as a computed field via
`SerializerMethodField` — spoiler label returned alongside review data
in one response.

---
