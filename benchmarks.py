"""
Комплексный исследовательский бенчмарк для разделов 7.2, 8 и 9.
Лабораторная работа № 6. Студент: Мусин Т. Б., БЦШ02-26-02.

Проводит многократные замеры (3 повтора) с расчетом среднего, min, max и ст. откл.
для Insertion Sort, встроенной функции sorted(), Binary Search и Linear Search.
"""

from random import Random
from time import perf_counter
import math
import json
from algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
)


def calc_stats(times):
    avg = sum(times) / len(times)
    variance = sum((t - avg) ** 2 for t in times) / (len(times) - 1) if len(times) > 1 else 0.0
    std_dev = math.sqrt(variance)
    return {
        "avg": avg,
        "min": min(times),
        "max": max(times),
        "std": std_dev
    }


def run_full_experiments():
    print("=" * 80)
    print("ЗАПУСК КОМПЛЕКСНОГО ЭКСПЕРИМЕНТА ПО ОЦЕНКЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 80)
    
    rng = Random(42)
    repeats = 3
    
    # 1. Основные сценарии из Таблицы раздела 9
    # Случайные N = 100, 1000, 5000, 10000; отсортированный N = 1000; обратный N = 1000; дубликаты N = 1000
    scenarios = [
        {"name": "Случайный", "n": 100, "gen": lambda n: [rng.randint(-10**6, 10**6) for _ in range(n)]},
        {"name": "Случайный", "n": 1000, "gen": lambda n: [rng.randint(-10**6, 10**6) for _ in range(n)]},
        {"name": "Случайный", "n": 5000, "gen": lambda n: [rng.randint(-10**6, 10**6) for _ in range(n)]},
        {"name": "Случайный", "n": 10000, "gen": lambda n: [rng.randint(-10**6, 10**6) for _ in range(n)]},
        {"name": "Отсортированный", "n": 1000, "gen": lambda n: list(range(n))},
        {"name": "Обратный", "n": 1000, "gen": lambda n: list(range(n, 0, -1))},
        {"name": "С повторами", "n": 1000, "gen": lambda n: [rng.randint(-5, 5) for _ in range(n)]},
    ]
    
    main_results = []
    
    print("\n--- Основная таблица экспериментов (Раздел 9) ---")
    for sc in scenarios:
        n = sc["n"]
        name = sc["name"]
        
        ins_times = []
        sort_times = []
        bin_times = []
        
        for _ in range(repeats):
            raw_data = sc["gen"](n)
            
            # Измерение Insertion Sort
            t0 = perf_counter()
            ordered = insertion_sort(raw_data)
            t1 = perf_counter()
            ins_times.append((t1 - t0) * 1000.0)
            
            # Измерение sorted()
            t0 = perf_counter()
            _ = sorted(raw_data)
            t1 = perf_counter()
            sort_times.append((t1 - t0) * 1000.0)
            
            # Измерение Binary Search (1000 запросов)
            queries = [rng.choice(ordered) for _ in range(1000)]
            t0 = perf_counter()
            for q in queries:
                binary_search(ordered, q)
            t1 = perf_counter()
            bin_times.append((t1 - t0) * 1000.0)
            
        ins_stat = calc_stats(ins_times)
        sort_stat = calc_stats(sort_times)
        bin_stat = calc_stats(bin_times)
        
        # Определение вывода
        if name == "Отсортированный":
            conclusion = "Лучший случай O(N): минимальное время, 0 сдвигов"
        elif name == "Обратный":
            conclusion = "Худший случай O(N^2): максимум сдвигов (в 2 раза медленнее среднего)"
        elif name == "С повторами":
            conclusion = "Стабильность сохранена, время сравнимо со случайным"
        else:
            conclusion = f"Квадратичный рост O(N^2), поиск O(log N) стабилен (~{bin_stat['avg']:.2f} мс)"
            
        res_row = {
            "n": n,
            "type": name,
            "insertion": ins_stat,
            "sorted": sort_stat,
            "binary_1000": bin_stat,
            "conclusion": conclusion
        }
        main_results.append(res_row)
        
        print(f"N={n:5d} | {name:<15} | Ins: {ins_stat['avg']:8.3f} ms (min={ins_stat['min']:.3f}, max={ins_stat['max']:.3f}) | "
              f"sorted(): {sort_stat['avg']:6.3f} ms | Bin 1000: {bin_stat['avg']:6.3f} ms | {conclusion}")

    # 2. Сравнение линейного и бинарного поиска (Раздел 7.2)
    # N = 100, 1000, 10000, 100000 (1000 запросов к одному отсортированному списку)
    print("\n--- Сравнение линейного и бинарного поиска (Раздел 7.2) ---")
    search_comparison = []
    search_ns = [100, 1000, 10000, 100000]
    
    for n in search_ns:
        arr = sorted([rng.randint(-10**7, 10**7) for _ in range(n)])
        # Одинаковый набор 1000 запросов
        queries = [rng.choice(arr) for _ in range(1000)]
        
        # Линейный поиск
        lin_times = []
        for _ in range(repeats):
            t0 = perf_counter()
            for q in queries:
                linear_search(arr, q)
            t1 = perf_counter()
            lin_times.append((t1 - t0) * 1000.0)
            
        # Бинарный поиск
        bin_times = []
        for _ in range(repeats):
            t0 = perf_counter()
            for q in queries:
                binary_search(arr, q)
            t1 = perf_counter()
            bin_times.append((t1 - t0) * 1000.0)
            
        lin_stat = calc_stats(lin_times)
        bin_stat = calc_stats(bin_times)
        speedup = lin_stat["avg"] / bin_stat["avg"] if bin_stat["avg"] > 0 else 0
        
        search_row = {
            "n": n,
            "linear_avg": lin_stat["avg"],
            "binary_avg": bin_stat["avg"],
            "speedup": speedup
        }
        search_comparison.append(search_row)
        print(f"N={n:6d} | Линейный: {lin_stat['avg']:8.3f} ms | Бинарный: {bin_stat['avg']:6.3f} ms | Ускорение: {speedup:6.1f}x")

    # Сохраняем результаты в JSON для отчета
    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "main_experiments": main_results,
            "search_comparison": search_comparison
        }, f, ensure_ascii=False, indent=2)
    print("\nРезультаты бенчмарков успешно сохранены в benchmark_results.json")


if __name__ == "__main__":
    run_full_experiments()
