# optimal_infrastructure

**В этом модуле производится реализация сетевой топологии свитч и набор машин для решения определенных задач:**

**Цель работы:** на вход программе дается граф задач (DAG), описание задач и ограничение в цене. Цель реализации - найти оптимальный набор машин для исполнения набора задач за наименьшее время с ограниченным бюджетом.

**Особенности:**
необходимо найти 2 набора машин для последовательных и для параллельных задач, каждый из наборов содержит свой сетевой коммутатор - свитч.
Машины для параллельных и для последовательных задач отличаются, потому что параллельные задачи уменьшают время исполнения за счет возможности параллельности (т.е. количества ядер и количества машин)
Машины для последовательных вычислений уменьшают время исполнения за счет частоты процессора


**Глобальные подзадачи:**
1. Построить инфраструктуру на вход которой подается набор машин и задача, и в результате программа выводит стоимость и время вычисления задач на данном наборе машин.
2. Найти оптимальный набор машин для решения этой задачи за ограниченную стоимость.
 - реализация жадного алгоритма;
 - реализация эволюционного алгоритма.

**Сделаны реализации второй глобальной подзадачи в двух вариациях:**
    - когда набор машин для решения задач стационарен (набор машин выбирается один раз в задания, и все задачи выполняются на них согласно расписанию). Данный метод подходит для стационарных машин. Реализация в папке parallel_task_scheduling
    - когда набор машин может подбираться для каждой задачи индивидуально. Данный метод подходит для облачных вычислений. Реализация в папке sequential modification.


**Данные о машинах:**
        - Данные о доступных конфигурациях и об их стоимости взяты с Amazon AWS
        - Оценочное время исполнения задачи на определенной машине вычислено путем экспериментального вычисления на одной машине с частотой ядра 3.7, что аналитически позволяет вычислить время исполнения на других машинах
        - Оценочное время передачи на несколько машин в зависимости от частоты свитча и от количества машин вычислено на кластере (на 4, 3, 2, 1 машинах), затем аппроксимировано и оценено время передачи на машины и обратно (скорость передачи зависит от количества машин ,и частоты свитча, и объема передаваемой памяти).


**Данные о задаче:**

**Начальные вводимые пользователем данные:**
- Граф задач (DAG)
- Датасет с информацией по каждой задачи (complexity of task, possibility for paralleling, incoming and outgoing memory)
- Ограничения в стоимости

**Результаты работы алгоритмов:**
- Необходимый набор машин для решения заданных задач
- Общее время выполнения этих задач на подобранных машинах
- Общая стоимость выполнения
- Таблица подробных результатов (на какой машине и сколько по времени выполняется данная задача, сколько затрачено денежных ресурсов на ее выполнения, время передачи данных и т.д.)






**Алгоритм для построения инфраструктуры на вход которой подается набор машин и задача, и в результате программа выводит стоимость и время вычисления задач на данном наборе машин:**

Инфраструктура состоит из набора машин для непараллельных задач, машин для параллельных задач, свитча (сетевого коммутатора). Далее задачи распределяются на машины:
1.  Задачи выполняются согласно заданному ориентированному графу. То есть следующая задача не может выполняться, пока не выполнилась предыдущая.
Для каждой задачи определяется ее приоритет (то есть первая задача, имеет 0 приоритет и должна выполнится самой первой). Приоритет рассчитывается как максимальное расстояние до текущей задачи до первой задачи). Задачи с одинаковым приоритетом могут рассчитываться параллельно.
2. Задачи одного приоритета сортируются по убыванию. И самая сложная задача таким образом попадает на лучшую машину.
3. Задачи с возможностью распараллеливания (параллелятся на машины и на количество ядер этих машин). На каждую машину направляется часть задания согласно ее конфигурации.
4. Затем так рассчитывается время и стоимость для реализации каждой задачи. Также рассчитывается время и стоимость передачи данных с машины на машину. Итого получаем время и стоимость реализации.


**Алгоритмы подбора оптимальной инфрастуктуры:**

Для первой вариации алгоритма (неменяющиеся машины)
Жадный алгоритм:
1. Для последовательных машин: максимальное количество = максимальное количество последовательных задач с одинаковым приоритетом. Сортируется набор доступных машин (с минимальным количеством ядер, потому что для задач без распараллеливания кол-во ядер не важно).
Далее пробуем добавит лучшую машину, если на ней стоимость расчетов превосходит ограничения в стоимость для последовательных машин, то пробуем добавить следующую машину. Когда удалось подобрать одну машину.
Сохраняем ее и пока количество машин не превосходит максимального повторяем этот процесс. (Полученное число машин будет находиться в интервале от 1 до "максимальное количество последовательных задач с одинаковым приоритетом".
2. Для параллельных задач.
Алгоритм тот же самый, что и для последовательных. Только список доступных машин расширяется (появляются машины с разным количеством ядер). И максимально возможное количество машин ограничивается свитчом (максимальным кол-вом подсоединяемых машин).


**Эволюционный алгоритм:**

1. Особь выглядит как список, где каждый элемент - это количество машин текущей конфигурации.
Например:
Список доступных машин:
[(4,2), (4,1), (2,2), (2,1)] первый элемент кол-во ядер, второй - частота.
Особь:
[0, 0, 3, 2] = берем 3 машины 3 -го типа, 2 машины 4-го типа и все.



Для второй вариации (облачной)
Отличия для поcледовательных задач:
Количество машин = количеству последовательных задач. Для каждой задачи своя машины.
Подбираем также жадным алгоритмом.
Задачи сортируются по убыванию сложности, и при распределении на самую сложную задачу идет самая лучшая машина.
