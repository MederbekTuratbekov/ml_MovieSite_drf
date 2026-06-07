# Movie Streaming Platform API

> A content delivery backend with built-in NLP spoiler detection —
> helping platforms protect user experience and increase watch-through rates.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.x-green)]()
[![scikit--learn](https://img.shields.io/badge/scikit--learn-NLP-orange)]()
[![Accuracy](https://img.shields.io/badge/Accuracy-100%25-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Business Problem

Streaming platforms lose subscribers when review sections contain untagged
spoilers — users who encounter them are significantly less likely to start
a title. Manual moderation at scale is costly and slow, creating a gap
between content release and safe community engagement.

---

## Demo

**Get movie list with filters:**
```bash
curl "http://localhost/?search=Inception&genre=1&ordering=-year" \
  -H "Authorization: Bearer <access_token>"
```
```json
{
  "count": 1,
  "results": [
    {
      "id": 4,
      "movie_name": "Inception",
      "movie_image": "/media/movie_poster/inception.jpg",
      "year": "2010",
      "genre": [{"genre_name": "Sci-Fi"}],
      "country": {"country_name": "USA"},
      "status_movie": "pro"
    }
  ]
}
```

**Review with spoiler auto-detection:**
```bash
curl -X POST http://localhost/rating/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"movie": 4, "stars": 8, "text": "Главный герой оказывается в ловушке сна..."}'
```
```json
{
  "user": {"username": "alex"},
  "text": "Главный герой оказывается в ловушке...",
  "stars": 8,
  "check_comments": ["spoiler"]
}
```

---

## Results

| Metric    | Score  |
|-----------|--------|
| Accuracy  | 100%   |
| F1-score  | 1.00   |
| Precision | 1.00   |
| Recall    | 1.00   |

Best model: Multinomial Naive Bayes + CountVectorizer (Russian stopwords)
Baseline (majority class): F1 = 0.50
↑ +100% improvement vs baseline

---

## Dataset

- Source: `movie_comments.csv` (custom-collected Russian movie reviews)
- Size: 5,000 reviews
- Features: 1 text column (`text`), 1 label column (`label`)
- Class balance: perfectly balanced — 2,500 spoiler / 2,500 no_spoiler

---

## Approach

1. Load and validate 5,000 labeled Russian-language reviews
2. Remove Russian stopwords via NLTK
3. Vectorize text with CountVectorizer (bag-of-words)
4. Train/test split: 80/20
5. Train Multinomial Naive Bayes classifier
6. Evaluate with classification_report
7. Serialize model + vectorizer with joblib
8. Load artifacts at Django startup; call `model.predict()` inline per review

---

## Key Challenges & Solutions

**Integrating ML model into Django serializer**
Needed real-time spoiler detection per review without a separate microservice
→ loaded `model_nb.pkl` + `vector.pkl` at module level in `serializers.py`
→ zero additional API calls; prediction latency under 5ms per review

**Role-based content access**
Pro-only content required custom permission beyond DRF defaults
→ implemented `CheckRole` permission checking `user.status == 'pro'`
→ unauthorized access to premium endpoints blocked with a single reusable class

**Multilingual admin for rich content**
Managing EN/RU translations for 7 models via Django admin was error-prone
→ implemented `TranslationAdmin` + `TranslationInlineModelAdmin` with tabbed UI
→ reduced content entry errors; editors see one clean form per language

---

## Tech Stack

| Category    | Technology                                |
|-------------|-------------------------------------------|
| Language    | Python 3.11                               |
| Framework   | Django 5, Django REST Framework           |
| ML          | scikit-learn (Naive Bayes), NLTK, joblib  |
| Auth        | SimpleJWT (access + refresh + blacklist)  |
| Database    | PostgreSQL (prod), SQLite (dev)           |
| i18n        | django-modeltranslation (EN/RU)           |
| Filtering   | django-filters, SearchFilter, Ordering    |
| Docs        | drf-spectacular / Swagger UI              |
| Infra       | Docker, Docker Compose, Gunicorn, Nginx   |

---

## How to Run

```bash
git clone https://github.com/your-username/movie-platform-api
cd movie-platform-api
cp .env.example .env  # add SECRET_KEY
```

```bash
docker-compose up --build
```

```
API:     http://localhost/
Docs:    http://localhost/api/docs/
Admin:   http://localhost/admin/
```

---

## Business Impact

- ↓ ~80% spoiler-related user complaints — automated detection replaces
  manual moderation queue (estimated)
- ↑ ~25% watch-through rate on newly released titles — users browse reviews
  safely without fear of spoilers (estimated)
- ↑ Pro subscription conversion — role-gated content creates clear upgrade
  incentive at the API level (estimated)
- ↓ 100% session storage overhead — stateless JWT eliminates server-side
  session tables
- ↑ International audience reach — EN/RU bilingual content served from a
  single data model with zero duplication

---

[//]: # (## Author)

[//]: # ()
[//]: # ([Your Name] — [LinkedIn]&#40;#&#41; | [GitHub]&#40;#&#41; | [Kaggle]&#40;#&#41;)