#!/usr/bin/python
"RED (random early drop) simple implementation"
import random


def request_ok(current, th_min, th_max):
    """return OK with a probability proportional to
       'low' current, between th_min and th_max"""
    return (current - th_min) / (th_max - th_min) < random.random()
