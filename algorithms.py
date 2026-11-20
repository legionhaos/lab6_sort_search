"""
Модуль реализации алгоритмов сортировки и поиска.
Лабораторная работа № 6.
"""

from typing import Any, List, Tuple


def insertion_sort(values: List[Any]) -> List[Any]:
    """
    Сортировка вставками (Insertion Sort).
    Возвращает новый отсортированный список, не изменяя исходный.
    
    Сложность:
      - Лучший случай: O(N) (массив уже отсортирован, ровно N-1 сравнений)
      - Средний случай: O(N^2) (примерно N^2 / 4 сравнений и сдвигов)
      - Худший случай: O(N^2) (массив отсортирован в обратном порядке, N^2 / 2 сдвигов)
    Память: O(N) для безопасной копии результата.
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
    Итеративный бинарный поиск (Binary Search).
    Возвращает индекс первого попавшегося совпадающего элемента или -1.
    
    Предусловие: sorted_values отсортирован по возрастанию.
    Сложность: O(1) лучший, O(log N) средний и худший.
    Память: O(1).
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


def binary_search_trace(a: List[Any], target: Any, verbose: bool = True) -> Tuple[int, List[dict]]:
    """
    Бинарный поиск с подробной трассировкой шагов (left, middle, right, value).
    Используется в Варианте Б (раздел 7.1) и Упражнении 3.
    """
    left = 0
    right = len(a) - 1
    steps = []
    while left <= right:
        middle = (left + right) // 2
        val = a[middle]
        step_info = {
            "left": left,
            "middle": middle,
            "right": right,
            "value": val
        }
        steps.append(step_info)
        if verbose:
            print(f"left={left}, middle={middle}, right={right}, value={val}")
        if val == target:
            return middle, steps
        if val < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1, steps


def linear_search(values: List[Any], target: Any) -> int:
    """
    Линейный поиск (Linear Search) для сравнительного анализа (раздел 7.2).
    Возвращает индекс первого вхождения target или -1.
    Сложность: O(1) лучший, O(N) средний и худший.
    """
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


def lower_bound(a: List[Any], target: Any) -> int:
    """
    Возвращает индекс первого элемента, не меньшего target (a[i] >= target).
    Если все элементы меньше target, возвращает len(a).
    Сложность: O(log N).
    """
    left, right = 0, len(a)
    while left < right:
        middle = (left + right) // 2
        if a[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


def upper_bound(a: List[Any], target: Any) -> int:
    """
    Возвращает индекс первого элемента, строго большего target (a[i] > target).
    Если таких элементов нет, возвращает len(a).
    Сложность: O(log N).
    """
    left, right = 0, len(a)
    while left < right:
        middle = (left + right) // 2
        if a[middle] <= target:
            left = middle + 1
        else:
            right = middle
    return left
