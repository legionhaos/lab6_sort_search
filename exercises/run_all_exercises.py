"""
Модуль выполнения обязательных упражнений (Упражнения 1-7).
Лабораторная работа № 6. Студент: Мусин Т. Б., БЦШ02-26-02.
"""

import sys
import os
from pathlib import Path
from random import Random
from time import perf_counter

# Добавляем родительский каталог в PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algorithms import (
    insertion_sort,
    binary_search,
    binary_search_trace,
    lower_bound,
    upper_bound,
)


def exercise_1_manual_trace():
    print("=" * 60)
    print("Упражнение 1. Трассировка сортировки вставками для [7, 4, 6, 2, 5]")
    print("=" * 60)
    a = [7, 4, 6, 2, 5]
    print(f"Исходный массив: {a}")
    print("База: префикс [7] упорядочен.")
    
    # Пошаговая симуляция
    curr = a[:]
    for i in range(1, len(curr)):
        key = curr[i]
        j = i - 1
        shifts = []
        while j >= 0 and curr[j] > key:
            shifts.append(curr[j])
            curr[j + 1] = curr[j]
            j -= 1
        curr[j + 1] = key
        print(f"Итерация i={i}: key={key}. Сдвинуты элементы {shifts}. "
              f"Префикс A[0..{i}] = {curr[:i+1]}. Массив: {curr}")
    print(f"Итоговый результат: {curr}\n")


def exercise_2_invariant_proof():
    print("=" * 60)
    print("Упражнение 2. Проверка и доказательство инварианта цикла")
    print("=" * 60)
    explanation = """
Инвариант внешнего цикла:
Перед началом каждой итерации i подмассив A[0..i-1] состоит из элементов,
первоначально находившихся в позициях с 0 по i-1, но уже упорядоченных:
A[0] <= A[1] <= ... <= A[i-1].

Доказательство по индукции:
1. Инициализация (база): перед i = 1 подмассив A[0..0] состоит из одного
   элемента A[0], который тривиально отсортирован.
2. Сохранение (шаг): тело цикла извлекает key = A[i] и в цикле while
   сдвигает вправо все элементы A[j] > key (начиная с j = i-1 вниз до 0).
   Поскольку префикс A[0..i-1] уже был упорядочен, все элементы строго больше
   key сдвигаются на 1 позицию вправо без изменения их взаимного порядка.
   Элемент key помещается в освободившуюся ячейку A[j+1], где:
     - либо j = -1 (key меньше всех элементов, встаёт в начало A[0]);
     - либо A[j] <= key (слева элемент меньше или равен key).
   Справа же находится сдвинутый элемент >= key.
   Следовательно, новый префикс A[0..i] полностью упорядочен.
3. Завершение: цикл завершается при i = n. В силу инварианта подмассив
   A[0..n-1] упорядочен, что означает полную сортировку исходного массива.
"""
    print(explanation.strip())
    print("\n")


def exercise_3_binary_search_steps():
    print("=" * 60)
    print("Упражнение 3. Бинарный поиск на бумаге для [2, 5, 8, 11, 15, 19, 23, 31]")
    print("=" * 60)
    arr = [2, 5, 8, 11, 15, 19, 23, 31]
    
    print("--- Поиск target = 19 ---")
    idx_19, steps_19 = binary_search_trace(arr, 19, verbose=True)
    print(f"Результат поиска 19: индекс {idx_19}")
    
    print("\n--- Поиск target = 20 ---")
    idx_20, steps_20 = binary_search_trace(arr, 20, verbose=True)
    print(f"Результат поиска 20: индекс {idx_20} (элемент отсутствует)")
    print("\n")


def exercise_4_unsorted_input():
    print("=" * 60)
    print("Упражнение 4. Неверный вход (неотсортированный список)")
    print("=" * 60)
    unsorted_data = [15, 2, 8, 31, 5, 19, 11, 23]
    target = 5
    print(f"Неотсортированный массив: {unsorted_data}")
    print(f"Ищем число target = {target}, которое реально есть в массиве на индексе 4.")
    
    res_index, steps = binary_search_trace(unsorted_data, target, verbose=True)
    print(f"Результат binary_search: {res_index}")
    assert res_index == -1, "Ожидалось, что на неотсортированном массиве алгоритм промахнется"
    
    explanation = """
Причина ошибки:
Бинарный поиск основан на аксиоме транзитивности отношений порядка:
если target < a[middle], то target гарантированно НЕ может находиться
правее middle.
На первом шаге: middle = 3, a[3] = 31.
Так как target = 5 < 31, бинарный поиск отбрасывает правую половину массива
(индексы 4..7) и переносит right = middle - 1 = 2.
Однако физически число 5 находилось в отброшенной половине (на индексе 4)!
В результате отсечения правильной области алгоритм не находит элемент и возвращает -1.
"""
    print(explanation.strip())
    print("\n")


def exercise_5_duplicate_bounds():
    print("=" * 60)
    print("Упражнение 5. Повторы (lower_bound и upper_bound)")
    print("=" * 60)
    arr = [1, 2, 2, 2, 5, 8]
    target = 2
    
    lb = lower_bound(arr, target)
    ub = upper_bound(arr, target)
    count = ub - lb
    
    print(f"Массив: {arr}, target = {target}")
    print(f"lower_bound({target}) = {lb} (первый элемент >= {target}: arr[{lb}] = {arr[lb]})")
    print(f"upper_bound({target}) = {ub} (первый элемент > {target}: arr[{ub}] = {arr[ub]})")
    print(f"Полуинтервал всех вхождений: [{lb}, {ub}), количество = {count}")
    
    assert lb == 1, f"lb mismatch: {lb} != 1"
    assert ub == 4, f"ub mismatch: {ub} != 4"
    assert count == 3, f"count mismatch: {count} != 3"
    
    # Проверки из методички
    test_arr = [1, 2, 2, 2, 5]
    assert lower_bound(test_arr, 2) == 1
    assert lower_bound(test_arr, 3) == 4
    assert lower_bound(test_arr, 9) == 5
    print("Все контрольные проверки lower_bound/upper_bound пройдены успешно!")
    print("\n")


def exercise_6_plot():
    print("=" * 60)
    print("Упражнение 6. Эксперимент со сложностью и генерация графика O(N^2)")
    print("=" * 60)
    # Запустим через uv отдельным шагом для генерации PNG
    print("Генерация графика вынесена в plot_generator.py (сохранение в plot_complexity.png)")
    print("\n")


def exercise_7_assert_verification():
    print("=" * 60)
    print("Упражнение 7. Контрольная проверка insertion_sort против sorted() (20 тестов)")
    print("=" * 60)
    rng = Random(42)
    lengths = [0, 1, 2, 3, 5, 10, 15, 20, 30, 50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    
    print(f"{'Тест №':<8} | {'Длина N':<8} | {'Диапазон чисел':<20} | {'Статус':<10}")
    print("-" * 52)
    for i, n in enumerate(lengths, 1):
        # Различные сценарии генерации
        if i % 4 == 0:
            # С большим количеством дубликатов
            data = [rng.randint(-5, 5) for _ in range(n)]
            mode = "[-5..5] (дубликаты)"
        elif i % 4 == 1:
            # Случайные большие числа
            data = [rng.randint(-10**6, 10**6) for _ in range(n)]
            mode = "[-10^6..10^6]"
        elif i % 4 == 2:
            # Уже отсортированные с небольшими возмущениями
            data = sorted([rng.randint(0, 1000) for _ in range(n)])
            mode = "Уже упорядоченные"
        else:
            # Обратно отсортированные
            data = sorted([rng.randint(0, 1000) for _ in range(n)], reverse=True)
            mode = "Обратный порядок"
        
        orig_copy = data[:]
        sorted_actual = insertion_sort(data)
        sorted_expected = sorted(data)
        
        assert sorted_actual == sorted_expected, f"Сбой на тесте {i} (N={n})"
        assert data == orig_copy, f"Исходный список был мутирован на тесте {i}"
        print(f"#{i:<7} | N = {n:<5} | {mode:<20} | PASS (OK)")
    
    print("\nВсе 20 рандомизированных тестов успешно подтвердили 100% эквивалентность!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    exercise_1_manual_trace()
    exercise_2_invariant_proof()
    exercise_3_binary_search_steps()
    exercise_4_unsorted_input()
    exercise_5_duplicate_bounds()
    exercise_6_plot()
    exercise_7_assert_verification()
