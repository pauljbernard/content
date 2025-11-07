"""
Claude API Client - Handles all interactions with Anthropic's Claude API
"""
import os
import anthropic
from typing import Dict, Any, Optional, AsyncIterator
from core.config import settings


class ClaudeClient:
    """Wrapper for Anthropic's Claude API with streaming and non-streaming support."""

    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY or ""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        # Using Claude Sonnet 4 - verified working model
        self.default_model = "claude-sonnet-4-20250514"
        self.max_tokens = 8000

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


def get_claude_client() -> ClaudeClient:
    """Get or create the Claude client singleton."""
    global _claude_client
    if _claude_client is None:
        _claude_client = ClaudeClient()
    return _claude_client
