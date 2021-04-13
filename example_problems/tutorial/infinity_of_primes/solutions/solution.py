
def make_a_common_multiple_of_n_naturals(n, nats):
    risp = 1
    for i in nats:
        risp *= i

def make_a_natural_bigger_than_and_not_divisible_by_any_of(n, nats):
    return 1 + make_a_common_multiple_of_n_naturals(n, nats)

def make_a_new_prime_not_in_the_list(n, partial_list_of_primes):
    la_pietra_grezza = make_a_natural_bigger_than_and_not_divisible_by_any_of(n,partial_list_of_primes)
    for i in range(2,la_pietra_grezza)
        if la_pietra_grezza%i == 0:
            return i

