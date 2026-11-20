"""
Лабораторная работа № 6
Тема: «Алгоритмы сортировки и бинарного поиска: программная реализация базовой
сортировки списка, поиск элемента в отсортированном массиве и оценка скорости
выполнения алгоритмов на разных объёмах данных»

Студент: Мусин Тимур Булатович, гр. БЦШ02-26-02 (N = 17)
"""

from random import Random
from time import perf_counter
from typing import Any, List


def insertion_sort(values: List[Any]) -> List[Any]:
    """
    Возвращает новый список, отсортированный по возрастанию.
    Исходный список не модифицируется (сохраняется безопасная копия).
    
    Временная сложность:
      - Лучший случай (уже отсортирован): O(N)
      - Средний случай (случайные данные): O(N^2)
      - Худший случай (обратно отсортирован): O(N^2)
    Пространственная сложность: O(N) для создания независимой копии.
    """
    result = values[:]
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def binary_search(sorted_values: List[Any], target: Any) -> int:
    """
    Итеративный алгоритм бинарного поиска элемента в отсортированном массиве.
    Возвращает индекс найденного target или -1, если target отсутствует.
    
    Предусловие: sorted_values должен быть отсортирован по неубыванию.
    
    Временная сложность:
      - Лучший случай (элемент в середине): O(1)
      - Средний и худший случаи: O(log N)
    Пространственная сложность: O(1) (итеративная реализация).
    """
    left = 0
    right = len(sorted_values) - 1
    while left <= right:
        middle = (left + right) // 2
        value = sorted_values[middle]
        if value == target:
            return middle
        if value < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


def check_algorithms() -> None:
    """
    Набор контрольных тестов для валидации корректности алгоритмов
    на граничных и стандартных случаях.
    """
    tests = [
        [],
        [7],
        [3, 1, 2],
        [1, 2, 3],
        [3, 2, 1],
        [5, 1, 5, 2, 5],
        [-2, 0, -1, 4]
    ]
    for data in tests:
        expected = sorted(data)
        actual = insertion_sort(data)
        assert actual == expected, f"Ошибка сортировки для {data}: {actual} != {expected}"
        assert data == data[:], "Нарушено условие сохранения исходного списка"
    
    data = [-10, -3, 0, 4, 4, 9, 20]
    assert binary_search(data, -10) != -1, "Элемент -10 должен быть найден"
    assert binary_search(data, 4) != -1, "Элемент 4 должен быть найден"
    assert binary_search(data, 100) == -1, "Элемент 100 отсутствует в массиве"
    print("Контрольные тесты пройдены")


def benchmark() -> None:
    """
    Базовый бенчмарк по методическим указаниям для N = (100, 1000, 5000, 10000).
    Использует фиксированный seed Random(42) для строгой воспроизводимости.
    """
    rng = Random(42)
    print("N; insertion_sort_ms; sorted_ms; binary_1000_ms")
    for n in (100, 1000, 5000, 10000):
        data = [rng.randint(-10**6, 10**6) for _ in range(n)]
        
        start = perf_counter()
        ordered = insertion_sort(data)
        insertion_ms = (perf_counter() - start) * 1000
        
        start = perf_counter()
        sorted(data)
        builtin_ms = (perf_counter() - start) * 1000
        
        queries = [rng.choice(ordered) for _ in range(1000)]
        start = perf_counter()
        for target in queries:
            binary_search(ordered, target)
        search_ms = (perf_counter() - start) * 1000
        
        print(f"{n}; {insertion_ms:.3f}; {builtin_ms:.3f}; {search_ms:.3f}")


if __name__ == '__main__':
    check_algorithms()
    benchmark()
