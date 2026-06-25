def is_prime(num):
    """Check if a number is prime."""
    if num <= 1:
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


def generate_primes(n):
    """Generate the first n prime numbers."""
    primes = []
    num = 2  # Start checking for prime from the first prime number
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes


if __name__ == "__main__":
    first_20_primes = generate_primes(20)
    print("The first 20 prime numbers are:", first_20_primes)
