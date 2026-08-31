import asyncio
import time


async def interroger_doc(nom: str, duree: float) -> str:
    """Simule un appel LLM/réseau lent sur un document."""
    print(f"  [{nom}] requête envoyée…")
    await asyncio.sleep(duree)  # ⏳ ICI : l'attente I/O simulée
    print(f"  [{nom}] réponse reçue ({duree}s)")
    return f"resultat::{nom}"


async def demo_tasks():
    t0 = time.perf_counter()

    # Les deux DÉMARRENT ici, en concurrence :
    tache_a = asyncio.create_task(interroger_doc("A", 1.0))
    tache_b = asyncio.create_task(interroger_doc("B", 2.0))

    print("juste après create_task -> done() :", tache_a.done())  # False
    # ... je pourrais faire autre chose ici pendant qu'elles tournent ...

    ra = await tache_a  # j'attends A (≈1s)
    rb = await tache_b  # B est peut-être déjà fini, sinon j'attends le reste
    print(f"create_task : {time.perf_counter() - t0:.2f}s -> {ra}, {rb}")
    print("done() final :", tache_a.done(), tache_b.done())


asyncio.run(demo_tasks())
