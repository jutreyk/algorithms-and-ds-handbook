import time
import random
from typing import List, Callable
from rich.console import Console
from rich.table import Table
from src.sorting.sorts import quick_sort, merge_sort, heap_sort, radix_sort, tim_sort

console = Console()

def run_benchmarks(sizes: List[int] = [1000, 5000, 10000]):
    console.print("[bold cyan]Running Performance Benchmarks on Random Integer Datasets[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta", border_style="dim")
    table.add_column("Algorithm", style="cyan")
    for s in sizes:
        table.add_column(f"N = {s:,} (ms)", style="yellow", justify="right")
        
    algorithms: List[tuple[str, Callable[[list], list]]] = [
        ("QuickSort (3-Way)", quick_sort),
        ("MergeSort", merge_sort),
        ("HeapSort", heap_sort),
        ("RadixSort (LSD)", radix_sort),
        ("TimSort (Hybrid)", tim_sort),
        ("Python Timsort (Builtin)", sorted)
    ]
    
    for name, func in algorithms:
        row = [name]
        for size in sizes:
            data = [random.randint(0, 1_000_000) for _ in range(size)]
            
            # Measure time
            start = time.perf_counter()
            _ = func(data)
            duration_ms = (time.perf_counter() - start) * 1000.0
            row.append(f"{duration_ms:.2f}")
        table.add_row(*row)
        
    console.print(table)

if __name__ == "__main__":
    run_benchmarks()
