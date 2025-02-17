import math
import random


def _interpolate(a: float, b: float, step: float) -> float:
    return a + (b - a) * step


def linear(a: float, b: float) -> float:
    """Linear distribution: Value has an equal chance of being anywhere between a and b."""
    return random.uniform(a, b)


def gaussian(a: float, b: float) -> float:
    """Gaussian distribution: Value is more likely to be near the mean and less likely to be near the extremes."""
    mu = _interpolate(a, b, 0.5)
    sigma = (b - a) / 6

    return random.gauss(mu, sigma)


def arcsine(a: float, b: float) -> float:
    """Arcsine distribution: Value is more likely to be near the extremes and less likely to be near the mean."""
    u = random.random()
    x = math.sin((math.pi / 2) * u) ** 2

    return _interpolate(a, b, x)
