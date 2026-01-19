# AI Social Market

A full-stack application that helps UK small businesses generate social media marketing content. Users input their business details and campaign goals, and the app generates British English social media copy and matching promotional images.

## Live Demo

- **Frontend**: https://aisocialmarket.vercel.app
- **Backend API**: https://aisocialmarket-production.up.railway.app
- **API Documentation**: https://aisocialmarket-production.up.railway.app/docs (development only)

## Testing the Application

This application requires API keys to generate content. You will need to provide your own keys.

### Getting API Keys

1. **Anthropic API Key** (for text generation)
   - Visit: https://console.anthropic.com/settings/keys
   - Create an account or sign in
   - Generate a new API key
   - Keys start with `sk-ant-`

2. **OpenAI API Key** (for image generation)
   - Visit: https://platform.openai.com/api-keys
   - Create an account or sign in
   - Generate a new API key
   - Keys start with `sk-`

### Using the Application

1. Visit the live demo URL
2. Enter your API keys when prompted
3. Keys are validated for correct format before submission
4. Keys are stored in your browser session only
5. Keys are cleared when you close the browser tab

### Estimated API Costs

| Service | Cost per Request |
|---------|------------------|
| Anthropic Claude | $0.01 - $0.03 |
| OpenAI DALL-E | $0.04 |

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite
- Axios
- Deployed on Vercel

### Backend
- FastAPI (Python 3.12)
- SQLAlchemy with asyncpg
- Pydantic
- Deployed on Railway

### Database
- PostgreSQL on Supabase

### AI Services
- Claude API (Anthropic) for copy generation
- DALL-E API (OpenAI) for image generation

## Features

- Multi-step campaign brief form
- British English copy generation for multiple platforms (Instagram, Facebook, LinkedIn, X, TikTok)
- AI-generated promotional images
- UK seasonal marketing suggestions
- Campaign history storage
- Rate limiting and error handling
- Responsive design
- Bring-your-own-API-keys authentication

## Security

### Authentication Model

This application uses a bring-your-own-keys (BYOK) model where users provide their own API keys. This approach:

- Protects the application owner from API costs
- Gives users control over their own API usage
- Eliminates the need for user account management

### Security Measures

| Measure | Description |
|---------|-------------|
| Key format validation | Keys are validated on both frontend and backend before use |
| Session-only storage | Keys are stored in sessionStorage, cleared on tab close |
| HTTPS only | All communication encrypted via TLS |
| No server-side storage | Keys are never persisted on the server |
| Log filtering | API keys are filtered from server access logs |
| Restricted CORS | Only allows specific origins, methods, and headers |
| Rate limiting | Prevents abuse of API endpoints |
| Production docs disabled | API documentation hidden in production |

### User Responsibilities

- Keep API keys confidential
- Monitor API usage on respective platforms
- Revoke keys if compromised

## Project Structure
```
aisocialmarket/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── campaign.py
│   │   │       ├── image.py
│   │   │       └── seasonal.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── dependencies.py
│   │   │   ├── error_handlers.py
│   │   │   ├── exceptions.py
│   │   │   └── rate_limit.py
│   │   ├── models/
│   │   │   └── campaign.py
│   │   ├── schemas/
│   │   │   ├── campaign.py
│   │   │   ├── image.py
│   │   │   └── seasonal.py
│   │   ├── services/
│   │   │   ├── campaign_service.py
│   │   │   ├── claude_service.py
│   │   │   ├── dalle_service.py
│   │   │   └── seasonal_service.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ApiKeyModal.tsx
│   │   │   ├── CampaignForm.tsx
│   │   │   └── CampaignResults.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   ├── auth.ts
│   │   │   └── campaign.ts
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vercel.json
│   └── .env.example
├── README.md
└── LICENSE
```

## Local Development

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL database (or Supabase account)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL

# Run development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Run development server
npm run dev
```

### Verify Setup

- Backend: http://localhost:8000
- Backend Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

## Environment Variables

### Backend

| Variable | Description | Required |
|----------|-------------|----------|
| `APP_NAME` | Application name | No |
| `APP_VERSION` | Application version | No |
| `DEBUG` | Enable debug mode | No |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `FRONTEND_URL` | Frontend URL for CORS | Yes |
| `RATE_LIMIT_REQUESTS` | Max requests per window | No |
| `RATE_LIMIT_WINDOW_SECONDS` | Rate limit window in seconds | No |

Example `backend/.env`:
```
APP_NAME="AI Social Market"
APP_VERSION="0.1.0"
DEBUG=true

DATABASE_URL=postgresql://user:password@host:5432/database

FRONTEND_URL=http://localhost:5173

RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
```

### Frontend

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | Yes |

Example `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

## API Endpoints

### Authentication

API keys are passed via HTTP headers:
- `X-Anthropic-Key`: Anthropic API key for text generation
- `X-OpenAI-Key`: OpenAI API key for image generation

Keys are validated for correct format:
- Anthropic keys must match: `sk-ant-[a-zA-Z0-9-_]{20,}`
- OpenAI keys must match: `sk-[a-zA-Z0-9-_]{20,}`

### Campaigns

| Method | Endpoint | Description | Required Headers |
|--------|----------|-------------|------------------|
| POST | `/api/v1/campaigns/generate-copy` | Generate social media copy | X-Anthropic-Key |
| POST | `/api/v1/campaigns/generate-full` | Generate copy and image | X-Anthropic-Key, X-OpenAI-Key |
| GET | `/api/v1/campaigns/` | List saved campaigns | None |
| GET | `/api/v1/campaigns/{id}` | Get campaign by ID | None |

### Images

| Method | Endpoint | Description | Required Headers |
|--------|----------|-------------|------------------|
| POST | `/api/v1/images/generate` | Generate promotional image | X-OpenAI-Key |

### Seasonal

| Method | Endpoint | Description | Required Headers |
|--------|----------|-------------|------------------|
| GET | `/api/v1/seasonal/suggestions` | Get UK seasonal suggestions | None |

### Health

| Method | Endpoint | Description | Required Headers |
|--------|----------|-------------|------------------|
| GET | `/health` | Health check | None |

## Deployment

### Backend (Railway)

1. Create account at https://railway.app
2. Create new project and connect GitHub repository
3. Configure service:
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - `DATABASE_URL`
   - `FRONTEND_URL`
   - `DEBUG=false`
5. Generate domain under Networking settings

### Frontend (Vercel)

1. Create account at https://vercel.com
2. Import GitHub repository
3. Configure project:
   - Framework Preset: Vite
   - Root Directory: `frontend`
4. Add environment variable:
   - `VITE_API_URL`: Your Railway backend URL
5. Deploy

### Post-Deployment

Update `FRONTEND_URL` in Railway with your Vercel URL to enable CORS.

## Database Setup

The application uses PostgreSQL hosted on Supabase.

1. Create account at https://supabase.com
2. Create new project
3. Go to Project Settings > Database
4. Copy Session pooler connection string (port 5432)
5. Tables are created automatically on application startup

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Generate copy | 5 per minute |
| Generate full campaign | 3 per minute |
| Generate image | 3 per minute |
| List/Get campaigns | 30 per minute |

## British English

All generated copy uses British English spelling and conventions:

- British spelling: colour, favourite, organise, centre, behaviour
- UK date format: DD/MM/YYYY
- UK cultural references
- UK seasonal hooks: Bank Holidays, Bonfire Night, Boxing Day, etc.

## Supported Platforms

| Platform | Character Limit |
|----------|-----------------|
| Instagram | 2,200 |
| Facebook | 500 |
| LinkedIn | 700 |
| X (Twitter) | 280 |
| TikTok | 300 |

## License

MIT License

Copyright (c) 2026 Vincent Ngobeh
