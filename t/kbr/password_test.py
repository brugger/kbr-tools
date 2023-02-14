import unittest
import time


import kbr.password_utils as pw

hashed_pw = '3cea0344defa16d698502cdbb015f8246f97e56dfdf63618275e203b4e9800540182065f8d5d563f975e438835dc02c232a690995eecb89276e1c4507cf043c6:salty'

def test_hash_password_001():
    assert pw.hash_password('secret', 'salty') == hashed_pw

def test_check_password_001():
    assert pw.check_password(hashed_pw, 'secret') == True


def test_check_password_002():
    assert pw.check_password(hashed_pw, 'secretly') == False
