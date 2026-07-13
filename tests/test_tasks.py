import pytest
import sys, os
# adiciona a raiz do projeto (D:\MOD32) ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tasks import somar, fatorial
from celery_app import celery_app

# força o Celery a rodar em modo eager (sem Redis)
celery_app.conf.task_always_eager = True
celery_app.conf.task_eager_propagates = True


def test_soma_task():
    resultado = somar.delay(3, 5).get(timeout=5)
    assert resultado == 8

    resultado = somar.delay(-2, 7).get(timeout=5)
    assert resultado == 5

def test_fatorial_task():
    resultado = fatorial.delay(5).get(timeout=5)
    assert resultado == 120

    resultado = fatorial.delay(0).get(timeout=5)
    assert resultado == 1

    resultado = fatorial.delay(1).get(timeout=5)
    assert resultado == 1

    # Teste de erro para número negativo
    with pytest.raises(ValueError):
        fatorial.delay(-3).get(timeout=5)
