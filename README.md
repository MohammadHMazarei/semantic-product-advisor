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

### Health Check
#### GET ```/api/v1/products/health```: Check system health and configuration
- Response:
```json
{
  "status": "healthy",
  "message": "The search system is ready",
  "config": {
    "embedding_model": "paraphrase-multilingual-mpnet-base-v2",
    "collection_name": "products_collection",
    "default_top_k": 5,
    "max_top_k": 20,
    "min_relevance_score": 0.3
  }
}
```

### Statistics
#### GET ```/api/v1/products/stats```: Get indexing statistics
- Response:
```json
{
  "total_products": 150,
  "indexed_documents": 150,
  "status": "synced"
}
```


## 🔧 Configuration

Key configuration options in ```.env```:

Variable | Description | Default
--- | --- | ---
`API_PORT` | API server port | 8000
`EMBEDDING_MODEL_NAME` | Sentence Transformer model | paraphrase-multilingual-mpnet-base-v2
`COLLECTION_NAME` | ChromaDB collection name | products_collection
`DEFAULT_SEARCH_TOP_K` | Default search results | 5
`MAX_SEARCH_TOP_K` | Maximum search results | 20
`MIN_RELEVANCE_SCORE` | Minimum similarity threshold | 0.3
`OLLAMA_MODEL` | LLM model for consultation | qwen2.5:latest
`REDIS_HOST` | Logging level | INFO


## 📊 Data Format

Products should be in JSON format (```data/products.json```):
```json
[
  {
    "id": 9177,
    "name": "مدیریت پیج اینستاگرام (اقتصادی)",
    "slug": "instagram-page-management-economic",
    "permalink": "https://example.com/product/...",
    "description": "<p>توضیحات محصول...</p>",
    "price": "1500000",
    "date_created": "2024-01-01T00:00:00",
    "status": "publish"
  }
]
```

## 🐳 Docker Services

The application uses three Docker services:
1. **chatbot-api**: Main FastAPI application
2. **ollama**: Local LLM server for consultation features
3. **redis**: Session and cache storage



## 📝 API Documentation

Once running, access interactive documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🧪 Testing


```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```


## 🔍 Logging

Logs are stored in the ```logs/``` directory with configurable levels:

- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages


## 🤝 Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (```git checkout -b feature/AmazingFeature```)
3. Commit your changes (```git commit -m 'Add some AmazingFeature'```)
4. Push to the branch (```git push origin feature/AmazingFeature```)
5. Open a Pull Request


## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments


- **Sentence Transformers** for multilingual embeddings
- **ChromaDB** for vector storage
- **FastAPI** for the excellent web framework
- **LangChain** for LLM orchestration


## 📧 Contact
For questions or support, please open an issue on GitHub.

**Made with ❤️**
