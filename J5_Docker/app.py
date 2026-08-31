import cowsay


def somme_carres(n):
    return sum(i * i for i in range(1, n + 1))


if __name__ == "__main__":
    resultat = somme_carres(10)
    cowsay.cow(f"Somme des carres de 1 a 10 = {resultat}")
