import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Optional
import json
import re
from pathlib import Path
import logging

from app.domain.entities import Product, SearchResult
from app.domain.repositories import ProductRepository
from app.infrastructure.embeddings import EmbeddingService
from app.core.config import Settings

logger = logging.getLogger(__name__)


class ChromaProductRepository(ProductRepository):
    """ChromaDB implementation of ProductRepository"""

    def __init__(
            self,
            embedding_service: EmbeddingService,
            settings: Settings
    ):
        self.embedding_service = embedding_service
        self.settings = settings

        logger.info(f"Initializing ChromaDB at: {settings.chroma_persist_path}")

        # Initialize ChromaDB with settings from config
        self.client = chromadb.PersistentClient(
            path=str(settings.chroma_persist_path),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Get or create collection with name from config
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

        logger.info(
            f"✅ ChromaDB initialized. "
            f"Collection: {settings.COLLECTION_NAME}, "
            f"Documents: {self.collection.count()}"
        )

        self._products_cache: List[Product] = []

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and normalize whitespace"""
        clean = re.sub('<[^<]+?>', '', text)
        clean = re.sub(r'\s+', ' ', clean)
        return clean.strip()

    async def load_products(self) -> List[Product]:
        """Load products from JSON and index them"""

        products_path = self.settings.products_json_path
        logger.info(f"Loading products from: {products_path}")

        # Load JSON
        try:
            with open(products_path, 'r', encoding='utf-8') as f:
                products_data = json.load(f)
        except FileNotFoundError:
            logger.error(f"Products file not found: {products_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in products file: {e}")
            raise

        # Parse products
        products = []
        for item in products_data:
            try:
                product = Product(
                    id=item['id'],
                    name=item['name'],
                    slug=item['slug'],
                    permalink=item['permalink'],
                    description=item.get('description', ''),
                    date_created=item['date_created'],
                    status=item['status'],
                    price=item['price']
                )
                products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing product {item.get('id')}: {e}")
                continue

        self._products_cache = products
        logger.info(f"✅ Loaded {len(products)} products")

        # Index in ChromaDB if not already indexed
        if self.collection.count() == 0:
            logger.info("Collection is empty. Starting indexing...")
            await self._index_products(products)
        else:
            logger.info(
                f"Collection already has {self.collection.count()} documents. "
                "Skipping indexing."
            )

        return products

    async def _index_products(self, products: List[Product]):
        """Index products in vector database"""

        logger.info(f"Indexing {len(products)} products...")

        documents = []
        metadatas = []
        ids = []

        for product in products:
            # Create searchable text
            clean_desc = self._clean_html(product.description)
            searchable_text = f"{product.name}\n\n{clean_desc}"

            documents.append(searchable_text)
            metadatas.append({
                "product_id": product.id,
                "name": product.name,
                "slug": product.slug,
                "permalink": product.permalink
            })
            ids.append(str(product.id))

        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.embedding_service.embed_texts(documents)

        # Add to ChromaDB
        logger.info("Adding to ChromaDB...")
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        logger.info(
            f"✅ Successfully indexed {len(products)} products in ChromaDB"
        )

    async def search_products(
            self,
            query: str,
            top_k: int = 5
    ) -> List[SearchResult]:
        """Search products using semantic similarity"""

        logger.debug(f"Searching for: '{query}' with top_k={top_k}")

        # Generate query embedding
        query_embedding = self.embedding_service.embed_text(query)

        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        # Convert to SearchResult entities
        search_results = []

        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                product_id = int(results['ids'][0][i])
                distance = results['distances'][0][i]
                document = results['documents'][0][i]

                # Convert distance to similarity score (cosine distance -> similarity)
                relevance_score = max(0.0, 1.0 - distance)

                # Get full product from cache
                product = await self.get_product_by_id(product_id)

                if product:
                    search_results.append(SearchResult(
                        product=product,
                        relevance_score=relevance_score,
                        matched_content=document[:300]
                    ))

        logger.debug(f"Found {len(search_results)} results")
        return search_results

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID from cache"""
        for product in self._products_cache:
            if product.id == product_id:
                return product
        return None

    def reset_collection(self):
        """Reset the collection (useful for re-indexing)"""
        logger.warning(f"Resetting collection: {self.settings.COLLECTION_NAME}")
        self.client.delete_collection(self.settings.COLLECTION_NAME)
        self.collection = self.client.create_collection(
            name=self.settings.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("✅ Collection reset complete")
