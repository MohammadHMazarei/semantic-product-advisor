# Digital Marketing Chatbot API

A sophisticated AI-powered chatbot system for digital marketing consultation and product search, built with FastAPI, LangChain, and semantic search capabilities.

## 🎯 Project Overview

This project provides an intelligent chatbot API that offers:
1. **Semantic Product Search**: Advanced search functionality over digital marketing products using vector embeddings
2. **Business Consultation** *(Coming Soon)*: Interactive consultation workflow to analyze business needs and recommend appropriate marketing solutions

## 🏗️ Architecture

The project follows **Clean Architecture** principles with clear separation of concerns:
```bash
chatbot-project/
├── app/
│   ├── api/                    # API Layer
│   │   └── routes.py           # FastAPI endpoints
│   ├── application/            # Application Layer
│   │   ├── dtos.py             # Data Transfer Objects
│   │   └── services.py         # Business logic services
│   ├── core/                   # Core Layer
│   │   ├── config.py           # Configuration management
│   │   └── dependencies.py     # Dependency injection
│   ├── domain/                 # Domain Layer
│   │   ├── entities.py         # Domain entities
│   │   └── repositories.py     # Repository interfaces
│   ├── infrastructure/         # Infrastructure Layer
│   │   ├── embeddings.py       # Embedding service
│   │   └── vector_store.py     # ChromaDB implementation
│   └── main.py                 # Application entry point
├── data/
│   └── products.json           # Product data
├── logs/                       # Application logs
├── tests/                      # Test files
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── .gitignore
```

### Architecture Layers

#### 1. **API Layer** (`app/api/`)
- **Purpose**: HTTP request handling and routing
- **Components**:
  - `routes.py`: Defines FastAPI endpoints for product search, health checks, and statistics
- **Responsibilities**: Request validation, response formatting, error handling

#### 2. **Application Layer** (`app/application/`)
- **Purpose**: Business logic orchestration
- **Components**:
  - `dtos.py`: Pydantic models for request/response validation
  - `services.py`: Service classes implementing business workflows
- **Responsibilities**: Coordinate between domain and infrastructure, implement use cases

#### 3. **Core Layer** (`app/core/`)
- **Purpose**: Cross-cutting concerns and configuration
- **Components**:
  - `config.py`: Centralized configuration using Pydantic Settings
  - `dependencies.py`: Dependency injection with singleton pattern
- **Responsibilities**: Configuration management, service lifecycle

#### 4. **Domain Layer** (`app/domain/`)
- **Purpose**: Business entities and contracts
- **Components**:
  - `entities.py`: Core business entities (Product, SearchResult)
  - `repositories.py`: Abstract repository interfaces
- **Responsibilities**: Define business rules and contracts (framework-agnostic)

#### 5. **Infrastructure Layer** (`app/infrastructure/`)
- **Purpose**: External service implementations
- **Components**:
  - `embeddings.py`: Sentence Transformers integration
  - `vector_store.py`: ChromaDB repository implementation
- **Responsibilities**: Database access, external API integration

## ✨ Features

### Phase 1: Product Search (✅ Implemented)

- **Semantic Search**: Persian language support using multilingual embeddings
- **Vector Database**: ChromaDB for efficient similarity search
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Health Monitoring**: System health checks and statistics endpoints
- **Configurable Search**: Adjustable result count and relevance thresholds

### Phase 2: Business Consultation (🚧 Coming Soon)

An interactive consultation workflow that:

1. **Information Gathering**: Collects four key business parameters through conversation:
   - Business Type
   - Customer Type (B2B/B2C)
   - Geographic Location
   - Existing Digital Sales Tools (website/social media pages)

2. **Analysis & Recommendations**: 
   - Provides initial analysis using LLM knowledge
   - Suggests relevant products and sales-boosting packages
   - Offers personalized marketing strategies

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.109.0
- **Language Model**: Ollama (Qwen 2.5)
- **Embeddings**: Sentence Transformers (paraphrase-multilingual-mpnet-base-v2)
- **Vector Database**: ChromaDB 0.4.22
- **Cache/Session**: Redis 7
- **LLM Framework**: LangChain 0.1.6
- **Validation**: Pydantic 2.5.3
- **Containerization**: Docker & Docker Compose

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- 4GB+ RAM (for embedding models)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/digital-marketing-chatbot-api.git
cd digital-marketing-chatbot-api
```
2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```
3. **Prepare product data**
```bash
# Place your products.json file in the data/ directory
mkdir -p data
cp /path/to/your/products.json data/
```
4. **Start services with Docker Compose**
```bash
docker-compose up -d
```
***The API will be available at http://localhost:8000***

### Local Development Setup
1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Run the application**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### Product Search
#### POST ```/api/v1/products/search```: Search products using semantic similarity
- Request Body:
```json
{
  "query": "مدیریت اینستاگرام",
  "top_k": 5
}
```
- Response:
```json
{
  "query": "مدیریت اینستاگرام",
  "results": [
    {
      "product": {
        "id": 9177,
        "name": "مدیریت پیج اینستاگرام (اقتصادی)",
        "slug": "instagram-page-management-economic",
        "permalink": "https://example.com/product/...",
        "description_preview": "...",
        "price_display": "1,500,000 تومان"
      },
      "relevance_score": 0.892
    }
  ],
  "total_found": 5,
  "min_relevance_score": 0.3
}
```
