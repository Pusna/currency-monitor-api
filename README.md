# Currency Monitor API (Monobank API) 🏦

A backend service for tracking UAH exchange rates, integrated with Monobank API, featuring automated updates and CSV export.

---

## 🛠 Tech Stack
* **Python** / **Django 5.0** / **DRF**
* **PostgreSQL** / **Redis**
* **Docker** & **Docker Compose**
* **Celery** / **Celery Beat**

---

## 📡 API Endpoints

- GET /api/currencies/tracked/ - Get currently tracked exchange rates.
- GET /api/currencies/available/ - List currencies available for tracking.
- PATCH /api/currencies/{id}/toggle_tracking/ - Enable or disable monitoring for a currency.
- GET /api/currencies/{id}/history/?start=&end= - Get rate history for a specific period.
- GET /api/currencies/export_csv/ - Download all currency data in CSV format

---

## 📁 Project Structure
```text
apps/
│   ├── currencies/          # Main application logic
│   │   ├── management/      # Custom CLI: python manage.py export_currencies_csv
│   │   ├── tasks.py         # Celery tasks (Monobank API integration)
│   │   ├── tests.py         # Automated API & Logic tests
│   │   ├── models.py        # Database schema (Currency, RateHistory)
│   │   ├── serializers.py   # Data transformation logic
│   │   └── views.py         # API Endpoints & Business logic
├── core/                    # Project settings & Celery config
├── .env.example             # Environment variables template
├── Dockerfile               # Container definition
├── docker-compose.yml       # Infrastructure orchestration
└── requirements.txt         # Project dependencies
```

---

## 🚀 How to Run
### 1. Prepare Environment
Copy the example environment file to create your active `.env`:
```bash
cp .env.example .env
```

### 2. Launch Application
Build and start the containers:

```bash
docker-compose up --build
```

### 3. Create Admin Account
To access the Admin Panel, create your superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```
---

## 📖 API & Monitoring
Swagger UI: http://localhost:8000/api/docs/ - Full interactive API documentation.

Admin Panel: http://localhost:8000/admin/ - Manage currency list and monitor Celery tasks.

CSV Export : http://localhost:8000/api/currencies/export_csv/ - Direct file download.

---
## ⚙️ Key Requirements Met
Automation: Celery Beat syncs latest rates from Monobank every 5 minutes.

History: All exchange rate changes are stored in a dedicated history table.

Filtering: API supports historical data retrieval with start and end date filters.

Tracking: Currencies can be enabled or disabled for monitoring via PATCH request.

Export: CSV generation is available via both CLI command and API endpoint.

API Access: CSRF is disabled for API endpoints to ensure seamless testing in Swagger.

---
## 🧪 Run Tests
To verify the application integrity:
```bash
docker-compose exec web python manage.py test apps.currencies.tests
```
