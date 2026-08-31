"""
unstable_pipeline.py — exercice intégrateur J4-PM
Pipeline : stream d'utilisateurs depuis une "API instable" → log dans un fichier.
"""

import functools
import random
import time
from contextlib import contextmanager


# --- Décorateurs ---
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            ms = (time.perf_counter() - start) * 1000
            print(f"[timer] {func.__name__}: {ms:.2f} ms")

    return wrapper


def retry(max_attempts=3, backoff=0.3, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        print(f"[retry] {func.__name__} ÉCHEC définitif: {exc}")
                        raise
                    wait = backoff * (2 ** (attempt - 1))
                    print(
                        f"[retry] {func.__name__} essai {attempt} KO ({exc}), wait {wait}s"
                    )  # noqa: E501
                    time.sleep(wait)

        return wrapper

    return decorator


# --- Context manager ---
@contextmanager
def open_logfile(path):
    print(f"[CM] open {path}")
    f = open(path, "a")
    try:
        yield f
    finally:
        print(f"[CM] close {path}")
        f.close()


# --- Fonction "API" instable, retryée ---
@retry(max_attempts=4, backoff=0.2, exceptions=(ConnectionError,))
def fetch_page(page_num):
    """Simule un appel API qui échoue 60% du temps."""
    if random.random() < 0.6:
        raise ConnectionError(f"page {page_num} timeout")
    return [
        {"id": page_num * 10 + i, "email": f"u{page_num * 10 + i}@x.com"}
        for i in range(10)
    ]


# --- Générateur : stream paresseux des utilisateurs ---
def stream_users(n_pages):
    """Yield les users page par page, sans charger les pages d'avance."""
    for p in range(n_pages):
        page = fetch_page(p)
        for user in page:
            yield user


# --- Pipeline principal, instrumenté avec @timer ---
@timer
def run_pipeline(n_pages, output_path):
    written = 0
    with open_logfile(output_path) as f:
        for user in stream_users(n_pages):
            f.write(f"{user['id']},{user['email']}\n")
            written += 1
    return written


if __name__ == "__main__":
    print("\n=== Exercice 7 : pipeline cas heureux ===")
    n = run_pipeline(n_pages=3, output_path="/tmp/pipeline.log")
    print(f"Total écrit : {n} utilisateurs")
    print("\n=== Exercice 8 : pipeline avec exception forcée (vérif CM) ===")

    @timer
    def run_pipeline_breaking(output_path):
        with open_logfile(output_path) as f:
            f.write("ligne avant crash\n")
            raise RuntimeError("erreur métier simulée")

    try:
        run_pipeline_breaking("/tmp/pipeline_crash.log")
    except RuntimeError as e:
        print(f"Exception bien propagée: {e}")

    # Vérifier que le fichier a été fermé proprement et contient la ligne
    with open("/tmp/pipeline_crash.log") as f:
        print(f"Contenu du fichier crash : {f.read().strip()!r}")
