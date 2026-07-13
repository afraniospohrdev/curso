from tasks import fatorial, somar
from celery_app import celery_app

def test_somar():
    resultado = somar.apply(args=(5,3)).get()   
    assert resultado == 8

def test_fatorial():
    resultado = fatorial.apply(args=(5,)).get()
    assert resultado == 120