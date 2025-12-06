"""
Utility functions for agent communication, streaming, and thinking pane handling.
Each agent should use these functions to enable streaming responses and thinking visibility.
"""

import json
import queue
import time
import random
from typing import Callable, Optional, Generator


# Global queue for SSE streaming updates (used in app.py)
_update_queue: Optional[queue.Queue] = None


def set_update_queue(q: queue.Queue) -> None:
    """Set the global queue for streaming updates. Called by app.py on startup."""
    global _update_queue
    _update_queue = q


def stream_agent_message(
    agent_id: str,
    node_id: str,
    message_generator_or_callable,
    status_callback: Optional[Callable] = None,
    is_code: bool = False,
    max_retries: int = 3
) -> str:
    """
    Stream a message from an agent to the frontend in real-time, token by token.
    BLOCKS until the entire generator is consumed.
    Includes exponential backoff with jitter for rate limit errors.
    
    Can accept either:
    - A generator object (direct generator)
    - A callable that returns a generator (enables retries by recreating the generator)
    
    Args:
        agent_id: The ID of the agent (e.g., 'similarity-finder')
        node_id: The ID of the workflow node for the diagram
        message_generator_or_callable: Either a generator or callable that returns a generator
        status_callback: Optional callback for status updates (for backward compatibility)
        is_code: Whether the message is code (affects formatting)
        max_retries: Maximum number of retry attempts for rate limits
    
    Returns:
        The complete accumulated message (only after generator is fully consumed)
        
    Raises:
        Exception: If all retries are exhausted
    """
    global _update_queue
    
    complete_message = ""
    retry_count = 0
    base_delay = 2  # Start with 2 seconds
    
    print(f"[STREAM START] {agent_id} - Starting to stream", flush=True)
    
    while retry_count <= max_retries:
        try:
            complete_message = ""
            chunk_count = 0
            
            # Get the generator (either passed directly or via callable)
            # This allows us to get a FRESH generator on each retry
            if callable(message_generator_or_callable):
                print(f"[STREAM] {agent_id} - Creating fresh generator from callable", flush=True)
                message_generator = message_generator_or_callable()
            else:
                print(f"[STREAM] {agent_id} - Using provided generator directly", flush=True)
                message_generator = message_generator_or_callable
            
            # Stream the response content - THIS BLOCKS until generator is exhausted
            print(f"[STREAM] {agent_id} - Consuming generator chunks", flush=True)
            for chunk in message_generator:
                chunk_count += 1
                if chunk:
                    complete_message += chunk
                    
                    # Send streaming update
                    update = {
                        "agentId": agent_id,
                        "message": chunk,
                        "nodeId": node_id,
                        "isCode": is_code,
                        "isStreaming": True,
                    }
                    
                    if _update_queue:
                        _update_queue.put(json.dumps(update))
                    
                    # Also call status_callback if provided (for backward compatibility)
                    if status_callback:
                        status_callback(agent_id, chunk, node_id, is_code)
            
            print(f"[STREAM] {agent_id} - Finished consuming {chunk_count} chunks", flush=True)
            
            # Send completion signal
            complete_update = {
                "agentId": agent_id,
                "message": "",
                "nodeId": node_id,
                "isCode": is_code,
                "isStreaming": False,
                "streamComplete": True,
            }
            
            if _update_queue:
                _update_queue.put(json.dumps(complete_update))
            
            print(f"[STREAM END] {agent_id} - Successfully completed with {len(complete_message)} chars", flush=True)
            return complete_message
            
        except Exception as e:
            error_msg = str(e)
            print(f"[STREAM ERROR] {agent_id} - Exception: {error_msg}", flush=True)
            
            # Check if it's a rate limit error
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                retry_count += 1
                print(f"[STREAM RETRY] {agent_id} - Rate limit detected, retry {retry_count}/{max_retries}", flush=True)
                
                if retry_count <= max_retries:
                    # Calculate exponential backoff with jitter
                    # Formula: base_delay * (2 ^ (retry_count-1)) + random jitter
                    exponential_delay = base_delay * (2 ** (retry_count - 1))
                    jitter = random.uniform(0, exponential_delay * 0.1)  # Add up to 10% jitter
                    wait_time = exponential_delay + jitter
                    
                    # Send retry message to user
                    retry_msg = {
                        "agentId": agent_id,
                        "message": f"Rate limited. Retrying in {int(wait_time)}s... (Attempt {retry_count}/{max_retries})",
                        "nodeId": node_id,
                        "isCode": False,
                        "isStreaming": False,
                        "isRetry": True,
                    }
                    
                    if _update_queue:
                        _update_queue.put(json.dumps(retry_msg))
                    
                    # Wait before retrying (with exponential backoff and jitter)
                    print(f"[STREAM WAIT] {agent_id} - Waiting {wait_time}s before retry", flush=True)
                    time.sleep(wait_time)
                    
                    # Continue to next iteration to retry
                    # This time we'll create a fresh generator (if a callable was provided)
                    print(f"[STREAM RETRY] {agent_id} - Continuing to next retry iteration", flush=True)
                    continue
                else:
                    # Max retries exceeded
                    print(f"[STREAM FAILED] {agent_id} - Max retries exceeded", flush=True)
                    error_update = {
                        "agentId": agent_id,
                        "message": "⚠️ API rate limit exceeded. Please wait a few minutes and try again.",
                        "nodeId": node_id,
                        "isCode": False,
                        "isStreaming": False,
                        "isError": True,
                        "retryPrompt": True,
                    }
                    
                    if _update_queue:
                        _update_queue.put(json.dumps(error_update))
                    
                    # Re-raise the exception to halt the workflow
                    raise
            else:
                # Not a rate limit error, re-raise immediately
                print(f"[STREAM ERROR] {agent_id} - Non-rate-limit error, re-raising", flush=True)
                raise
    
    return complete_message


def stream_thinking_pane(
    agent_id: str,
    thinking_generator: Generator[str, None, None],
    status_callback: Optional[Callable] = None,
) -> str:
    """
    Stream the AI's thinking process to a collapsible thinking pane.
    
    Args:
        agent_id: The ID of the agent
        thinking_generator: A generator that yields thinking chunks
        status_callback: Optional callback for status updates
    
    Returns:
        The complete thinking text
    """
    global _update_queue
    
    complete_thinking = ""
    
    for chunk in thinking_generator:
        complete_thinking += chunk
        
        update = {
            "agentId": agent_id,
            "message": chunk,
            "nodeId": None,
            "type": "thinking",
            "isStreaming": True,
        }
        
        if _update_queue:
            _update_queue.put(json.dumps(update))
        
        if status_callback:
            status_callback(agent_id, chunk, None)
    
    complete_update = {
        "agentId": agent_id,
        "message": "",
        "nodeId": None,
        "type": "thinking",
        "isStreaming": False,
        "streamComplete": True,
    }
    
    if _update_queue:
        _update_queue.put(json.dumps(complete_update))
    
    return complete_thinking


def send_agent_update(
    agent_id: str,
    message: str,
    node_id: str,
    is_code: bool = False,
    status_callback: Optional[Callable] = None,
    message_id: Optional[str] = None,
) -> None:
    """
    Send a complete agent update (non-streaming).
    Use this for backward compatibility with existing agents.
    
    Args:
        agent_id: The ID of the agent
        message: The complete message to send
        node_id: The workflow node ID
        is_code: Whether the message is code
        status_callback: Optional callback for status updates
        message_id: Optional unique ID for the message (allows updating in-place)
    """
    global _update_queue
    
    update = {
        "agentId": agent_id,
        "message": message,
        "nodeId": node_id,
        "isCode": is_code,
        "messageId": message_id,
    }
    
    if _update_queue:
        _update_queue.put(json.dumps(update))
    
    if status_callback:
        status_callback(agent_id, message, node_id, is_code)
