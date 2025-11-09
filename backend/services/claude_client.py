"""
Claude API Client - Handles all interactions with Anthropic's Claude API
"""
import os
import anthropic
from typing import Dict, Any, Optional, AsyncIterator
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Wrapper for Anthropic's Claude API with streaming and non-streaming support."""

    def __init__(self, db_session=None):
        """
        Initialize Claude client.

        Args:
            db_session: Optional database session to load configuration from database.
                       If not provided, uses .env configuration.
        """
        # Try to load configuration from database first
        api_key_from_db = None
        model_from_db = None

        if db_session:
            try:
                from models.llm_config import LLMProvider, LLMModel

                # Get default agent model from database
                default_model = db_session.query(LLMModel).filter(
                    LLMModel.is_default_for_agents == True,
                    LLMModel.is_active == True
                ).first()

                if default_model:
                    model_from_db = default_model.model_id
                    logger.info(f"Using model from database: {model_from_db}")

                    # Get the provider for this model
                    provider = db_session.query(LLMProvider).filter(
                        LLMProvider.id == default_model.provider_id,
                        LLMProvider.is_active == True
                    ).first()

                    if provider and provider.api_key:
                        api_key_from_db = provider.api_key
                        logger.info(f"Using API key from database provider: {provider.name}")
                else:
                    logger.warning("No default agent model found in database, falling back to .env config")
            except Exception as e:
                logger.warning(f"Failed to load LLM config from database: {e}. Falling back to .env config")

        # Use database config if available, otherwise fall back to .env
        self.api_key = api_key_from_db or settings.ANTHROPIC_API_KEY or ""
        if not self.api_key:
            raise ValueError("No API key available. Configure LLM provider in database or set ANTHROPIC_API_KEY in .env")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.default_model = model_from_db or "claude-sonnet-4-20250514"
        self.max_tokens = 8000

        logger.info(f"ClaudeClient initialized with model: {self.default_model}")

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a non-streaming response from Claude.

        Args:
            prompt: The user prompt/question
            system_prompt: Optional system prompt to set context
            model: Claude model to use (defaults to latest Sonnet)
            temperature: Randomness (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response
        """
        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": model or self.default_model,
                "messages": messages,
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature,
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.client.messages.create(**kwargs)

            # Extract text from response
            return response.content[0].text

        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    async def generate_streaming(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """
        Generate a streaming response from Claude.

        Args:
            prompt: The user prompt/question
            system_prompt: Optional system prompt to set context
            model: Claude model to use
            temperature: Randomness (0-1)
            max_tokens: Maximum tokens in response

        Yields:
            Text chunks as they arrive
        """
        import asyncio
        from concurrent.futures import ThreadPoolExecutor

        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": model or self.default_model,
                "messages": messages,
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature,
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            # Use a queue to communicate between threads
            import queue
            text_queue = queue.Queue()

            def stream_in_thread():
                """Run the blocking stream in a separate thread."""
                try:
                    with self.client.messages.stream(**kwargs) as stream:
                        for text in stream.text_stream:
                            text_queue.put(('chunk', text))
                    text_queue.put(('done', None))
                except Exception as e:
                    text_queue.put(('error', str(e)))

            # Start streaming in a background thread
            executor = ThreadPoolExecutor(max_workers=1)
            executor.submit(stream_in_thread)

            # Yield chunks as they arrive
            while True:
                try:
                    # Check queue without blocking too long
                    event_type, data = await asyncio.get_event_loop().run_in_executor(
                        None, text_queue.get, True, 0.1
                    )

                    if event_type == 'chunk':
                        yield data
                    elif event_type == 'done':
                        break
                    elif event_type == 'error':
                        raise Exception(f"Claude API streaming error: {data}")
                except queue.Empty:
                    # No data yet, yield control and continue
                    await asyncio.sleep(0.01)
                    continue

        except Exception as e:
            raise Exception(f"Claude API streaming error: {str(e)}")

    async def count_tokens(self, text: str) -> int:
        """
        Count tokens in text (approximate).
        Claude uses ~4 characters per token on average.
        """
        return len(text) // 4


# Singleton instance
_claude_client: Optional[ClaudeClient] = None


def get_claude_client(db_session=None) -> ClaudeClient:
    """
    Get or create the Claude client singleton.

    Args:
        db_session: Optional database session to load configuration.
                   If provided on first call, will load config from database.

    Returns:
        ClaudeClient instance
    """
    global _claude_client
    if _claude_client is None:
        # On first initialization, try to get database session if not provided
        if db_session is None:
            try:
                from database.session import SessionLocal
                db_session = SessionLocal()
                _claude_client = ClaudeClient(db_session=db_session)
                db_session.close()
            except Exception as e:
                logger.warning(f"Could not access database for LLM config: {e}. Using .env config.")
                _claude_client = ClaudeClient(db_session=None)
        else:
            _claude_client = ClaudeClient(db_session=db_session)

    return _claude_client
