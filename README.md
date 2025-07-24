# Search Engine

A full-stack search engine built with modern technologies, featuring web crawling, intelligent indexing, and fast search capabilities.

## 🚀 Features

- **Web Crawling**: Automated crawling of websites with configurable depth and rate limiting
- **Intelligent Indexing**: TF-IDF based search indexing for relevant results
- **Fast Search**: Real-time search with AND/OR operations
- **Async Processing**: Background task processing with Celery
- **Modern UI**: Responsive Vue.js frontend with Tailwind CSS
- **Production Ready**: Docker containerization with PostgreSQL and Redis
- **Scalable Architecture**: Microservices design for easy scaling

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Backend   │    │   Celery    │
│   (Vue.js)  │◄──►│   (FastAPI) │◄──►│   Workers   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────────┐   ┌─────────┐
              │PostgreSQL│   │  Redis  │
              └─────────┘   └─────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **PostgreSQL**: Primary database for documents and indices
- **Redis**: Caching and Celery broker
- **Celery**: Asynchronous task processing
- **SQLAlchemy**: Database ORM
- **NLTK**: Natural language processing
- **BeautifulSoup**: HTML parsing

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and static file serving

## 📦 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd search-engine
```

### 2. Deploy with One Command
```bash
./deploy.sh
```

### 3. Access the Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Manual Setup

### 1. Environment Configuration
```bash
 backend/.env
```

### 2. Start Services
```bash
# Build and start all services
docker-compose up -d --build

# Check service status
docker-compose ps
```

### 3. Verify Deployment
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost
```

## 📚 Usage

### 1. Adding Content
1. Go to the **Crawler** page
2. Enter URLs to crawl (comma-separated)
3. Click "Crawl"
4. Monitor task progress

### 2. Searching
1. Use the search box on the homepage
2. Enter your search query
3. Results are ranked by relevance
4. Use AND/OR operations for advanced queries



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🎯 Roadmap

- [ ] Advanced search filters
- [ ] User authentication
- [ ] Search analytics
- [ ] Machine learning ranking
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Search suggestions
- [ ] Export functionality