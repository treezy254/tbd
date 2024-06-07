
from functools import wraps

import time
import random
import logging
import functools
from typing import Union, Type, Tuple, Optional
import google.generativeai as genai



def extract_retry_time(error_message: str) -> Optional[float]:
    """Extract retry time from Google API error messages."""
    import re
    match = re.search(r'Try again in (\d+(?:\.\d+)?) seconds', error_message)
    return float(match.group(1)) if match else None


def retry_gemini_api(
    max_retries: int = 3,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (genai.types.google.api_core.exceptions.ResourceExhausted,
                        genai.types.google.api_core.exceptions.ServiceUnavailable,
                        genai.types.google.api_core.exceptions.DeadlineExceeded) as e:
                    if i == max_retries - 1:
                        
                        raise
                    
                    error_message = str(e)
                    delay_from_error = extract_retry_time(error_message)
                    
                    if delay_from_error:
                        delay = delay_from_error
                    else:
                        delay *= exponential_base * (1 + jitter * (random.random() - 0.5))
                    
                    
                    time.sleep(delay)
                except Exception as e:
                    
                    raise
        return wrapper
    return decorator