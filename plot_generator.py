"""
Генератор высококачественного графика временной сложности O(N^2).
Лабораторная работа № 6. Студент: Мусин Т. Б., БЦШ02-26-02.
Стилизовано в соответствии с High-Craft Dark UI.
"""

from random import Random
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
from algorithms import insertion_sort


def generate_complexity_chart():
    print("Запуск серии замеров для построения графика O(N^2)...")
    n_values = [100, 500, 1000, 1500, 2000, 3000, 4000, 5000, 7000, 10000]
    measured_times = []
    
    rng = Random(42)
    
    for n in n_values:
        repeats = 3
        times = []
        for _ in range(repeats):
            data = [rng.randint(-10**6, 10**6) for _ in range(n)]
            t0 = perf_counter()
            _ = insertion_sort(data)
            t1 = perf_counter()
            times.append((t1 - t0) * 1000.0)  # в миллисекундах
        avg_time = sum(times) / len(times)
        measured_times.append(avg_time)
        print(f"  N = {n:5d} -> {avg_time:8.2f} ms")
    
    # Теоретическая квадратичная кривая: c * N^2, калиброванная по последней точке N=10000
    c_coeff = measured_times[-1] / (n_values[-1] ** 2)
    n_dense = np.linspace(min(n_values), max(n_values), 200)
    theoretical_curve = c_coeff * (n_dense ** 2)
    
    # Настройка стилистики High-Craft Dark UI
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor('#09090B')
    ax.set_facecolor('#0E0E12')
    
    # Сетка
    ax.grid(True, linestyle='--', color='#FFFFFF', linewidth=0.7, alpha=0.08)
    
    # Линии графиков
    ax.plot(
        n_dense, theoretical_curve,
        label=f'Теоретическая сложность $O(N^2)$ ($c = {c_coeff:.2e}$)',
        color='#A855F7', linestyle='--', linewidth=2.0, alpha=0.9
    )
    ax.plot(
        n_values, measured_times,
        label='Экспериментальное время (Insertion Sort)',
        color='#38BDF8', marker='o', markersize=6, linewidth=2.4,
        markerfacecolor='#0284C7', markeredgecolor='#BAE6FD', markeredgewidth=1.2
    )
    
    # Оформление осей и заголовков
    ax.set_title(
        'Зависимость времени выполнения Insertion Sort от размера массива N\n(Экспериментальная проверка сложности $O(N^2)$)',
        fontsize=13, fontweight='bold', color='#FAFAFA', pad=15
    )
    ax.set_xlabel('Размер массива (N, элементов)', fontsize=11, fontweight='medium', color='#A1A1AA', labelpad=10)
    ax.set_ylabel('Время выполнения (миллисекунды, мс)', fontsize=11, fontweight='medium', color='#A1A1AA', labelpad=10)
    
    # Настройка границ и засечек
    for spine in ax.spines.values():
        spine.set_color('#FFFFFF')
        spine.set_alpha(0.15)
        spine.set_linewidth(1.0)
    
    ax.tick_params(colors='#A1A1AA', which='both', labelsize=9.5)
    
    # Легенда
    legend = ax.legend(
        facecolor='#18181B', edgecolor='#FFFFFF',
        fontsize=10, loc='upper left', framealpha=0.95
    )
    legend.get_frame().set_alpha(0.12)
    for text in legend.get_texts():
        text.set_color('#FAFAFA')
        
    # Добавляем плашку с параметрами окружения
    info_text = (
        "CPU: 12th Gen Intel Core i7-12650H\n"
        "OS: Arch Linux x86_64\n"
        "Python: 3.14 / Timer: time.perf_counter()"
    )
    ax.text(
        0.97, 0.05, info_text,
        transform=ax.transAxes,
        fontsize=8.5,
        color='#71717A',
        ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#121217', edgecolor='#FFFFFF', alpha=0.85)
    )
    
    plt.tight_layout()
    output_path = "plot_complexity.png"
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"График успешно сгенерирован и сохранён в: {output_path}")


if __name__ == '__main__':
    generate_complexity_chart()
