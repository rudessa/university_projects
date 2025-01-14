import pygame
import numpy as np
import sys
import random
import math

"""
Код реализует игру "Четыре в ряд" с использованием графического интерфейса на базе Pygame.
Основные элементы:
1. Игровое поле - матрица 6x7, которая заполняется фишками игроков.
2. Игровая логика - функции проверки победителя, оценка хода, реализация алгоритма Minimax с альфа-бета отсечением.
3. Графический интерфейс - отображение доски, фишек, ходов, а также взаимодействие игрока с программой.
4. Искусственный интеллект (AI), который принимает решения, используя алгоритм Minimax.
"""

# Константы, определяющие игроков, пустые ячейки и другие настройки
PLAYER = 0 #игрок 1
AI = 1 #AI
EMPTY = 0 #пустая ячейка на доске
PLAYER_PIECE = 1 #фишка на доске
AI_PIECE = 2  #фишка AI
WINDOW_LENGTH = 4 # длина последовательности для победы

# Цвета для графического интерфейса
DARK_GREY = (105, 105, 105)  # цвет доски
WHITE = (255, 255, 255)  # цвет фона
RED = (255, 0, 0)  # цвет фишек игрока
BLUE = (0, 0, 255)  # цвет фишек AI

# Размеры доски
ROW_COUNT = 6  # количество строк
COLUMN_COUNT = 7  # количество столбцов



# Создание пустой доски как массива 6x7
def create_board():
    """
    Создает пустую игровую доску в виде массива 6x7, заполненного нулями.
    Возвращает доску.
    """
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# Добавление фишки в указанное место на доске
def drop_piece(board, row, col, piece):
    """
    Устанавливает фишку (piece) в определенную строку (row) и столбец (col) на доске.
    """
    board[row][col] = piece


# Проверяет, можно ли сделать ход в указанный столбец
def is_valid_location(board, col):
    """
    Проверяет, свободен ли верхний ряд в данном столбце. Возвращает True, если ход возможен.
    """
    return board[ROW_COUNT - 1][col] == 0


# Возвращает первую доступную строку в указанном столбце
def get_next_open_row(board, col):
    """
    Возвращает индекс первой свободной строки в данном столбце.
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# Печатает игровую доску в консоль (для отладки)
def print_board(board):
    """
    Отображает игровую доску в консоли. Переворачивает доску для корректного отображения.
    """
    print(np.flip(board, 0))


#Отображает доску
def print_board(board):
	print(np.flip(board, 0))


# Проверяет, есть ли победная последовательность для текущего игрока
def winning_move(board, piece):
    """
    Проверяет, есть ли у игрока с указанной фишкой (piece) 4 последовательных фишки
    по горизонтали, вертикали или диагонали.
    Возвращает True, если игрок выиграл.
    """
    # Проверка по горизонтали
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Проверка по вертикали
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Проверка положительных наклонных диагоналей
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Проверка отрицательных наклонных диагоналей
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


	
# Оценивает конкретное окно (группу из 4 ячеек) для текущего игрока
    """
    Оценивает значение группы из 4 ячеек (window) на доске для заданного игрока.
    Возвращает числовую оценку.
    """
def evaluate_window(window, piece):
      
	score = 0
	opp_piece = PLAYER_PIECE

	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE
	# Счет за фишки игрока
	if window.count(piece) == 4:# Полная линия из 4
		score += 10000
	elif window.count(piece) == 3 and window.count(EMPTY) == 1: # 3 фишки + 1 пустая
		score += 100
	elif window.count(piece) == 2 and window.count(EMPTY) == 2: # 2 фишки + 2 пустые
		score += 10
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:  # Если противнику остался один ход до победы
		score -= 100
	if window.count(opp_piece) == 2 and window.count(EMPTY) == 2:  # Если противнику остался два ход до победы
		score -= 10
	if window.count(opp_piece) == 4:# Полная линия из 4
		score -= 10000
	return score


# Общая оценка текущей позиции на доске для игрока
def score_position(board, piece):
    """
    Вычисляет общую оценку текущей позиции на доске для заданного игрока.
    Суммирует очки за центр, горизонтали, вертикали и диагонали.
    """
    score = 0

    # Оценка центра доски
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

	 # Оценка вертикалей
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

     # Оценка горизонталей
    for c in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[c,:])]
        for r in range(COLUMN_COUNT-3):
            window = row_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
            
	# Оценка диагоналей с положительным наклоном
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

	# Оценка диагоналей с отрицательным наклоном
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


# Проверяет, завершена ли игра (победа или ничья)
def is_terminal_node(board):
    """
    Проверяет, завершена ли игра. Возвращает True, если кто-то выиграл или нет доступных ходов.
    """
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# Реализация алгоритма Minimax с альфа-бета отсечением
def minimax(board, depth, alpha, beta, maximizingPlayer):
    """
    Алгоритм Minimax для поиска лучшего хода с альфа-бета отсечением.
    Возвращает наилучший столбец и оценку доски.
    """

    # Получаем все допустимые столбцы для хода
    valid_locations = get_valid_locations(board)
    # Проверяем, является ли текущий узел конечным (выигрыш, ничья или конец игры)
    is_terminal = is_terminal_node(board)

    # Базовый случай: если глубина рекурсии 0 или достигнут конечный узел
    if depth == 0 or is_terminal:
        # Если это конечный узел, то возвращаем большую оценку для выигрыша AI, отрицательную для выигрыша игрока
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000000000)  # Победа AI
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)  # Победа игрока
            else: 
                return (None, 0)  # Ничья
        else: 
            # Если не конечный узел, оцениваем текущую позицию
            return (None, score_position(board, AI_PIECE))

    # Ход AI (maximizingPlayer=True): AI пытается максимизировать свою оценку
    if maximizingPlayer:
        value = -math.inf  # Начальная минимальная оценка для максимизирующего игрока
        column = random.choice(valid_locations)  # Случайный столбец как начальный выбор

        # Перебираем все допустимые столбцы
        for col in valid_locations:
            # Находим первую пустую строку в выбранном столбце
            row = get_next_open_row(board, col)
            b_copy = board.copy()  # Копируем доску, чтобы не изменять оригинальную
            drop_piece(b_copy, row, col, AI_PIECE)  # Совершаем ход AI
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]  # Рекурсивно вызываем Minimax для следующего хода

            # Обновляем наилучшую оценку для AI
            if new_score > value:
                value = new_score
                column = col

            # Альфа-отсечение: если найдено решение лучше, чем текущее, то отсеиваем остальные ветви
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Прерываем цикл, так как остальная ветвь уже не может улучшить результат
        return column, value  # Возвращаем наилучший столбец и его оценку

    # Ход игрока (maximizingPlayer=False): игрок пытается минимизировать оценку AI
    else: 
        value = math.inf  # Начальная максимальная оценка для минимизирующего игрока
        column = random.choice(valid_locations)  # Случайный столбец как начальный выбор

        # Перебираем все допустимые столбцы
        for col in valid_locations:
            # Находим первую пустую строку в выбранном столбце
            row = get_next_open_row(board, col)
            b_copy = board.copy()  # Копируем доску, чтобы не изменять оригинальную
            drop_piece(b_copy, row, col, PLAYER_PIECE)  # Совершаем ход игрока
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]  # Рекурсивно вызываем Minimax для следующего хода

            # Обновляем наилучшую оценку для игрока
            if new_score < value:
                value = new_score
                column = col

            # Бета-отсечение: если найдено решение хуже, чем текущее, то отсеиваем остальные ветви
            beta = min(beta, value)
            if alpha >= beta:
                break  # Прерываем цикл, так как остальная ветвь уже не может улучшить результат
        return column, value  # Возвращаем наилучший столбец и его оценку



#Возвращает список доступных для хода столбцов
def get_valid_locations(board):
	"""
    Возвращает список столбцов, куда можно сделать ход.
    """
	valid_locations = []

	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)

	return valid_locations


def draw_board(board):
    # Отрисовка игрового поля
    for c in range(COLUMN_COUNT):  # Перебираем все столбцы
        for r in range(ROW_COUNT):  # Перебираем все строки
            # Рисуем темно-серые клетки игрового поля
            pygame.draw.rect(screen, DARK_GREY, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # Рисуем белые окружности в качестве пустых клеток
            pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    # Отрисовка фишек (игрока и AI) на игровом поле
    for c in range(COLUMN_COUNT):  # Перебираем все столбцы
        for r in range(ROW_COUNT):  # Перебираем все строки
            if board[r][c] == PLAYER_PIECE:  # Если клетка занята фишкой игрока
                pygame.draw.circle(
                    screen, RED,  # Красный цвет для фишек игрока
                    (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS
                )
            elif board[r][c] == AI_PIECE:  # Если клетка занята фишкой AI
                pygame.draw.circle(
                    screen, BLUE,  # Синий цвет для фишек AI
                    (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS
                )

    pygame.display.update()  # Обновляем экран, чтобы изменения стали видны


# Создаем игровую доску
board = create_board()

# Печатаем игровую доску в консоль для отладки
print_board(board)

# Переменная для отслеживания состояния игры (закончена или нет)
game_over = False

# Инициализация Pygame (настройка графической библиотеки)
pygame.init()

# Устанавливаем размер одной клетки игрового поля в пикселях
SQUARESIZE = 100

# Вычисляем ширину и высоту игрового окна
width = COLUMN_COUNT * SQUARESIZE  # Ширина равна количеству колонок, умноженному на размер клетки
height = (ROW_COUNT+1) * SQUARESIZE  # Высота включает одну дополнительную строку для интерфейса

# Размеры игрового окна
size = (width, height)

# Радиус кружков, отображающих фишки (чуть меньше половины клетки)
RADIUS = int(SQUARESIZE / 2 - 5)

# Создаем окно с заданными размерами
screen = pygame.display.set_mode(size)

# Отрисовываем начальное состояние доски
draw_board(board)

# Обновляем экран после отрисовки
pygame.display.update()

# Задаем шрифт для отображения текста (например, сообщений о победе)
myfont = pygame.font.SysFont("monospace", 75)

# Устанавливаем начальный ход (в данном случае начинает AI)
# turn = random.randint(PLAYER, AI) # Если хотите случайный выбор первого игрока
turn = AI  # Здесь установлено, что первым ходит AI



# Если ход первым совершает AI
if turn == AI:
    # AI использует алгоритм minimax для выбора лучшего хода
    col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

    # Проверяем, допустимо ли выбранное AI место
    if is_valid_location(board, col):
        # Получаем доступную строку для фишки в выбранной колонке
        row = get_next_open_row(board, col)
        # Опускаем фишку AI на доску
        drop_piece(board, row, col, AI_PIECE)

        # Проверяем, привел ли ход AI к победе
        if winning_move(board, AI_PIECE):
            label = myfont.render("AI is win!!", 1, BLUE)  # Отображаем сообщение о победе AI
            screen.blit(label, (40, 10))  # Выводим текст на экран
            game_over = True  # Завершаем игру

        # Печатаем обновленную доску в консоль и отображаем её на экране
        print_board(board)
        draw_board(board)
        # Передаем ход игроку
        turn += 1
        turn = turn % 2

# Основной игровой цикл
while not game_over:
    # Обрабатываем события Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если пользователь закрыл окно
            sys.exit()

        if event.type == pygame.MOUSEMOTION:  # Отслеживаем движение мыши
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))  # Очищаем верхнюю часть экрана
            posx = event.pos[0]  # Координата X курсора
            if turn == PLAYER:  # Если ходит игрок
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)  # Отображаем фишку на экране
        pygame.display.update()  # Обновляем экран

        if event.type == pygame.MOUSEBUTTONDOWN:  # Отслеживаем нажатие кнопки мыши
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))  # Очищаем верхнюю часть экрана
            # Обработка хода игрока
            if turn == PLAYER:
                posx = event.pos[0]  # Получаем координату X клика мыши
                col = int(math.floor(posx / SQUARESIZE))  # Определяем колонку на основе позиции клика
                if is_valid_location(board, col):  # Проверяем, допустима ли колонка
                    row = get_next_open_row(board, col)  # Получаем доступную строку для фишки
                    drop_piece(board, row, col, PLAYER_PIECE)  # Опускаем фишку игрока на доску
                    if winning_move(board, PLAYER_PIECE):  # Проверяем, победил ли игрок
                        label = myfont.render("Player is win!!", 1, RED)  # Отображаем сообщение о победе игрока
                        screen.blit(label, (40, 10))  # Выводим текст на экран
                        game_over = True  # Завершаем игру

                    # Передаем ход AI
                    turn += 1
                    turn = turn % 2
                    # Обновляем доску в консоли и на экране
                    print_board(board)
                    draw_board(board)

    # Ход AI
    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)  # AI использует minimax
        if is_valid_location(board, col):  # Проверяем корректность хода
            row = get_next_open_row(board, col)  # Определяем доступную строку
            drop_piece(board, row, col, AI_PIECE)  # Опускаем фишку AI
            if winning_move(board, AI_PIECE):  # Проверяем, победил ли AI
                label = myfont.render("AI is win!!", 1, BLUE)  # Отображаем сообщение о победе AI
                screen.blit(label, (40, 10))  # Выводим текст на экран
                game_over = True  # Завершаем игру

            # Обновляем доску в консоли и на экране
            print_board(board)
            draw_board(board)
            # Передаем ход игроку
            turn += 1
            turn = turn % 2

    # Завершение игры
    if game_over:
        pygame.time.wait(10000)  # Ждем 10 секунд перед закрытием окна