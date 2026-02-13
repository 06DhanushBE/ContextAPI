import os
from abc import ABC, abstractmethod
from typing import Iterator
import requests
from groq import Groq
import json


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a non-streaming response"""
        pass
    
    @abstractmethod
    def generate_stream(self, prompt: str) -> Iterator[str]:
        """Generate a streaming response"""
        pass


class GroqProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content
    
    def generate_stream(self, prompt: str) -> Iterator[str]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class OpenAIProvider(LLMProvider):
    def __init__(self):
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in environment")
            self.client = OpenAI(api_key=api_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content
    
    def generate_stream(self, prompt: str) -> Iterator[str]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


def get_llm_provider(provider_name: str = None) -> LLMProvider:
    """Factory function to get the configured LLM provider"""
    if provider_name is None:
        provider_name = os.getenv("LLM_PROVIDER", "groq").lower()
    else:
        provider_name = provider_name.lower()
    
    providers = {
        "groq": GroqProvider,
        "openai": OpenAIProvider
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unknown LLM provider: {provider_name}. Choose from: {list(providers.keys())}")
    
    return providers[provider_name]()
