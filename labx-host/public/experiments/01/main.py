"""Experiment 01: Factorial and Fibonacci Generator in Python."""

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n in (0, 1):
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(count: int) -> list[int]:
    if count <= 0:
        return []
    if count == 1:
        return [0]
    series = [0, 1]
    while len(series) < count:
        series.append(series[-1] + series[-2])
    return series

def main():
    print("=" * 50)
    print(" LabX Experiment 01: Factorial & Fibonacci")
    print("=" * 50)
    
    num = 7
    print(f"Calculating factorial of {num}...")
    fact_val = factorial(num)
    print(f"Result: {num}! = {fact_val}")
    
    terms = 10
    print(f"\nGenerating first {terms} terms of Fibonacci sequence:")
    fib_series = fibonacci(terms)
    print(f"Result: {fib_series}")
    print("=" * 50)

if __name__ == "__main__":
    main()
