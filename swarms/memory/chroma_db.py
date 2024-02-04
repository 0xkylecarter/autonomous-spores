import numpy as np
import logging
import uuid
from typing import Optional, Callable, List

import chromadb
from dotenv import load_dotenv
from chromadb.utils.data_loaders import ImageLoader
from chromadb.utils.embedding_functions import (
    OpenCLIPEmbeddingFunction,
)


# Load environment variables
load_dotenv()


# Results storage using local ChromaDB
class ChromaDB:
    """

    ChromaDB database

    Args:
        metric (str): The similarity metric to use.
        output (str): The name of the collection to store the results in.
        limit_tokens (int, optional): The maximum number of tokens to use for the query. Defaults to 1000.
        n_results (int, optional): The number of results to retrieve. Defaults to 2.

    Methods:
        add: _description_
        query: _description_

    Examples:
        >>> chromadb = ChromaDB(
        >>>     metric="cosine",
        >>>     output="results",
        >>>     llm="gpt3",
        >>>     openai_api_key=OPENAI_API_KEY,
        >>> )
        >>> chromadb.add(task, result, result_id)
    """

    def __init__(
        self,
        metric: str,
        output_dir: str,
        limit_tokens: Optional[int] = 1000,
        n_results: int = 2,
        embedding_function: Callable = None,
        data_loader: Callable = None,
        multimodal: bool = False,
        *args,
        **kwargs,
    ):
        self.metric = metric
        self.output_dir = output_dir
        self.limit_tokens = limit_tokens
        self.n_results = n_results

        # Disable ChromaDB logging
        logging.getLogger("chromadb").setLevel(logging.INFO)

        # Create Chroma collection
        chroma_persist_dir = "chroma"
        chroma_client = chromadb.PersistentClient(
            settings=chromadb.config.Settings(
                persist_directory=chroma_persist_dir,
            ),
            *args,
            **kwargs,
        )

        # Data loader
        if data_loader:
            self.data_loader = data_loader
        else:
            self.data_loader = ImageLoader()

        # Embedding model
        if embedding_function:
            self.embedding_function = embedding_function
        else:
            self.embedding_function = None

        # If multimodal set the embedding model to OpenCLIP
        if multimodal:
            self.embedding_function = OpenCLIPEmbeddingFunction()

        # Create ChromaDB client
        self.client = chromadb.Client()

        # Create Chroma collection
        self.collection = chroma_client.get_or_create_collection(
            name=output_dir,
            metadata={"hnsw:space": metric},
            embedding_function=self.embedding_function,
            data_loader=self.data_loader,
            *args,
            **kwargs,
        )

    def add(
        self,
        document: str,
        images: List[np.ndarray] = None,
        img_urls: List[str] = None,
        *args,
        **kwargs,
    ):
        """
        Add a document to the ChromaDB collection.

        Args:
            document (str): The document to be added.
            condition (bool, optional): The condition to check before adding the document. Defaults to True.

        Returns:
            str: The ID of the added document.
        """
        try:
            doc_id = str(uuid.uuid4())
            self.collection.add(
                ids=[doc_id],
                documents=[document],
                images=images,
                uris=img_urls,
                *args,
                **kwargs,
            )
            return doc_id
        except Exception as e:
            raise Exception(f"Failed to add document: {str(e)}")

    def query(
        self,
        query_text: str,
        query_images: List[np.ndarray],
        *args,
        **kwargs,
    ):
        """
        Query documents from the ChromaDB collection.

        Args:
            query (str): The query string.
            n_docs (int, optional): The number of documents to retrieve. Defaults to 1.

        Returns:
            dict: The retrieved documents.
        """
        try:
            docs = self.collection.query(
                query_texts=[query_text],
                query_images=query_images,
                n_results=self.n_docs,
                *args,
                **kwargs,
            )["documents"]
            return docs[0]
        except Exception as e:
            raise Exception(f"Failed to query documents: {str(e)}")
