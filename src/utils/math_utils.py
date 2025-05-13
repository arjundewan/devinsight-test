import math
import statistics
from typing import List

def add(a: float, b: float) -> float:
    """Adds two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts second number from the first."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divides first number by the second. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base: float, exp: float) -> float:
    """Calculates the power of base to the exponent."""
    return math.pow(base, exp)

def factorial(n: int) -> int:
    """Calculates the factorial of a non-negative integer."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers")
    if n == 0:
        return 1
    else:
        res = 1
        for i in range(1, n + 1):
            res *= i
        return res

def calculate_mean(data: List[float]) -> float:
    """Calculates the arithmetic mean (average) of a list of numbers."""
    if not data:
        raise ValueError("Cannot calculate mean of an empty list")
    return statistics.mean(data)

def calculate_median(data: List[float]) -> float:
    """Calculates the median of a list of numbers."""
    if not data:
        raise ValueError("Cannot calculate median of an empty list")
    return statistics.median(data)

def calculate_std_dev(data: List[float]) -> float:
    """Calculates the sample standard deviation of a list of numbers."""
    if len(data) < 2:
        raise ValueError("Standard deviation requires at least two data points")
    return statistics.stdev(data)

def is_prime(num: int) -> bool:
    """Checks if a positive integer is a prime number."""
    if not isinstance(num, int) or num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

class Vector2D:
    """Represents a 2D vector with basic operations."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def magnitude(self) -> float:
        """Calculates the magnitude (length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """Normalizes the vector (makes its magnitude 1). Modifies in-place."""
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        self.x /= mag
        self.y /= mag
        return self # Return self for chaining if desired

    def dot_product(self, other: 'Vector2D') -> float:
        """Calculates the dot product with another Vector2D."""
        return self.x * other.x + self.y * other.y

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        return f"Vector2D(x={self.x}, y={self.y})" 