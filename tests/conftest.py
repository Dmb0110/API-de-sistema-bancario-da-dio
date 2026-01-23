"""
Configuração do pytest para testes assíncronos
"""
import pytest
import asyncio
from typing import Generator


def pytest_configure(config):
    """Configura markers personalizados do pytest"""
    config.addinivalue_line(
        "markers", "asyncio: marca testes que usam asyncio"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para os testes"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
