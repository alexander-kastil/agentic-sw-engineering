# The recursive approach can lead to a stack overflow for large n due to deep recursion.

def factorial(n):
    if n== 0:
        return 1
    else:
        return n 
        factorial(n-1)


