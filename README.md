# Match Master - The Tournament Scheduler

**Version 2.0 - Full-Stack Web Application**

## Overview

MatchMaster has been transformed from a Streamlit application to a comprehensive full-stack web application for tournament management. The platform preserves the existing Pair Table Algorithm and tournament logic while adding modern web architecture, user authentication, persistent data storage, and a sleek dark-mode interface.

## Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **JWT Authentication** - Secure token-based authentication
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - Lightweight state management
- **React Hook Form** - Performant forms with easy validation
- **Lucide React** - Beautiful & consistent icons

## Scheduling Algorithm

The project uses a custom match scheduling algorithm named **PAIR TABLE ALGORITHM**. This algorithm was inspired by older versions of standard match making which is favorable for "between tournament country travels". This algorithm is optimal for:
- Fair rest days for all teams
- Strategic home ground plays
- Reduced inter-country travel
- Balanced tournament scheduling

## Features

### Core Features
- **User Authentication** - Secure registration and login system
- **Tournament Management** - Create and manage tournaments with comprehensive settings
- **Team Organization** - Add teams with home ground assignments and detailed profiles
- **Smart Scheduling** - Automated match scheduling using the Pair Table Algorithm
- **Real-time Points Table** - Live updates using existing PointsTable.py logic
- **Match Management** - Input results and track match progress
- **Analytics Dashboard** - Performance metrics and tournament insights

### User Roles
- **Super Admin** - Full system access and user management
- **Tournament Admin** - Create/manage tournaments and teams
- **Team Manager** - Manage assigned teams and view results
- **Viewer** - Read-only access to public tournaments

## Architecture Highlights

### Preserved Tournament Logic
All existing Python classes and algorithms have been integrated without modification:
- `Structures/Dequeue.py` - Queue management for tournament operations
- `Structures/Graph.py` - Fully connected undirected graphs for match relationships
- `Structures/PointsTable.py` - Points calculation and ranking system
- `Structures/Scheduler.py` - Match scheduling implementation with Pair Table Algorithm
- `Structures/Stack.py` - Stack operations for tournament data

### Modern Web Architecture
- **RESTful API** - Clean API design with FastAPI
- **Database Persistence** - PostgreSQL with proper relationships
- **Authentication & Authorization** - JWT-based security
- **Responsive Design** - Mobile-first dark theme interface
- **State Management** - Efficient client-side state handling

## Project Structure

```plaintext
MatchMaster/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── auth.py                 # Authentication logic
│   ├── services/
│   │   └── tournament_service.py # Tournament business logic
│   └── requirements.txt
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx           # Landing page
│   │   ├── login/             # Authentication pages
│   │   ├── register/
│   │   ├── dashboard/         # Main dashboard
│   │   └── tournaments/       # Tournament management
│   ├── components/            # Reusable UI components
│   │   ├── ui/               # Base UI components
│   │   ├── layout/           # Layout components
│   │   └── tournaments/      # Tournament-specific components
│   └── lib/                  # Utilities and configuration
│       ├── api.ts           # API client
│       ├── store.ts         # State management
│       └── utils.ts         # Helper functions
├── Structures/               # Original tournament logic (preserved)
│   ├── Dequeue.py
│   ├── Graph.py
│   ├── PointsTable.py
│   ├── Scheduler.py
│   └── Stack.py
└── CLI Version/              # Original CLI implementation
```

## Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- PostgreSQL 12+

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Set up PostgreSQL database:**
   ```sql
   CREATE DATABASE matchmaster;
   CREATE USER matchmaster_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE matchmaster TO matchmaster_user;
   ```

4. **Run the backend server:**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your API URL
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

### Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## API Documentation

The FastAPI backend automatically generates interactive API documentation available at `/docs` endpoint. Key endpoints include:

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - Get user profile

### Tournaments
- `GET /tournaments` - List all tournaments
- `POST /tournaments` - Create new tournament
- `GET /tournaments/{id}` - Get tournament details
- `POST /tournaments/{id}/schedule` - Schedule matches using Pair Table Algorithm

### Teams & Matches
- `POST /tournaments/{id}/teams` - Add team to tournament
- `GET /tournaments/{id}/matches` - Get tournament matches
- `PUT /matches/{id}` - Update match results
- `GET /tournaments/{id}/points-table` - Get live points table

## Key Features in Detail

### Pair Table Algorithm Integration
The original scheduling algorithm has been seamlessly integrated into the web application:
- Preserves all original logic and data structures
- Maintains optimal scheduling for fair rest days
- Supports home ground advantage distribution
- Minimizes travel requirements between matches

### Real-time Points Table
- Uses original `PointsTable.py` with quicksort implementation
- Live updates when match results are entered
- Maintains last 5 matches history using Stack data structure
- Supports multiple sorting and filtering options

### Modern User Interface
- Dark theme optimized for extended use
- Responsive design for all device sizes
- Intuitive navigation and user experience
- Real-time updates and notifications

## Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - bcrypt with salt rounds
- **Role-based Access Control** - Granular permissions
- **Input Validation** - Comprehensive data validation
- **SQL Injection Prevention** - Parameterized queries
- **CORS Protection** - Configured for secure cross-origin requests

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
npm test
```

### Database Migrations
The application uses SQLAlchemy for database management. Models are automatically created on startup.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Migration from Streamlit

The application has been completely rewritten while preserving all core tournament logic:

### What's Preserved
- All original Python classes and algorithms
- Pair Table Algorithm implementation
- Tournament scheduling logic
- Points calculation system
- Data structures (Stack, Deque, Graph)

### What's New
- Modern web architecture with FastAPI + Next.js
- User authentication and authorization
- Persistent database storage
- RESTful API design
- Responsive dark theme interface
- Real-time updates and notifications

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on GitHub or contact the development team.

---

**MatchMaster v2.0** - Tournament management reimagined with modern web technology while preserving the proven Pair Table Algorithm.
