import random
import time
from rich.console import Console
from rich.table import Table
from handbook import quick_sort, merge_sort, heap_sort, radix_sort, tim_sort

console = Console()

def run():
    sizes = [1000, 5000, 10000]
    table = Table(title="Бенчмарк алгоритмов сортировки", show_header=True, header_style="bold magenta")
    table.add_column("Алгоритм", style="cyan")
    for s in sizes:
        table.add_column(f"N = {s:,} (мс)", justify="right")

    algorithms = [
        ("QuickSort (3-Way)", quick_sort),
        ("MergeSort", merge_sort),
        ("HeapSort", heap_sort),
        ("RadixSort", radix_sort),
        ("TimSort", tim_sort),
        ("Python sorted()", sorted)
    ]

    for name, func in algorithms:
        row = [name]
        for size in sizes:
            data = [random.randint(0, 1_000_000) for _ in range(size)]
            start = time.perf_counter()
            _ = func(data)
            duration_ms = (time.perf_counter() - start) * 1000.0
            row.append(f"{duration_ms:.2f}")
        table.add_row(*row)

    console.print(table)

if __name__ == "__main__":
    run()
