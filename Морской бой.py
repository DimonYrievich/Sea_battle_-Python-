
import random

# СОЗДАЕМ КЛАСС С ПОЛЬЗОВАТЕЛЬСКИМ ИСКЛЮЧЕНИЕМ ОТ РОДИТЕЛЬСКОГО ВСТРОЕННОГО КЛАССА Exception:

class BoardOutException(Exception):
    def __init__(self, message = "Вы выстрелили за пределы поля"):
        super().__init__(message)   # Используя встроенную функцию super(), передаем сообщение в базовый класс для
                                    # обработки исключения, чтобы сократить код и далее не использовать метод __str__(self)


# СОЗДАЕМ КЛАСС ТОЧЕК НА ИГРОВОМ ПОЛЕ:

class Dot:
    def __init__(self, x, y):
        self.x = x              # координата по оси x
        self.y = y              # координата по оси y

    def __str__(self):
        return f"Dot({self.x}, {self.y})"

    # Метод для проверки точек на равенство, и чтобы проверить, находится ли точка в списке.
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y    # ДЛЯ ПРИМЕРА!!!



# СОЗДАЕМ КЛАСС КОРАБЛЯ НА ИГРОВОМ ПОЛЕ:

class Ship:
    def __init__(self, length, bow_ship, direction, amount_life):
        self.length = length                # длина корабля
        self.bow_ship = bow_ship            # точка, где размещён нос корабля
        self.direction = direction          # направление корабля: 0 - горизонтальное, 1 - вертикальное
        self.amount_life = amount_life      # количеством жизней (сколько точек корабля ещё не подбито)

    def __str__(self):
        return f"Ship(length={self.length}, bow={self.bow_ship}, direction={self.direction}, lives={self.amount_life})"

    # Метод, который возвращает список всех точек корабля
    def dots(self):
        one_ship = []
        for i in range(self.length):
            if self.direction == 0:
                coordinate_x = self.bow_ship.x + i
                coordinate_y = self.bow_ship.y
                one_ship.append(Dot(coordinate_x, coordinate_y))
            if  self.direction == 1:
                coordinate_x = self.bow_ship.x
                coordinate_y = self.bow_ship.y + i
                one_ship.append(Dot(coordinate_x, coordinate_y))
        return one_ship



# СОЗДАЕМ КЛАСС ИГРОВОЙ ДОСКИ:

class Board:
    def __init__(self, all_board: list[list[str]], all_ships: list[Ship], hid: bool, living_ships: int):
        self.all_board = all_board          # двумерный список, в котором хранятся состояния каждой из клеток: "o" — пустая клетка, "■" — часть корабля, "x" — подбитая часть корабля, " " — промах.
        self.all_ships = all_ships          # список кораблей доски
        self.hid = hid                      # информация типа bool о том, нужно ли скрывать корабли на доске (True - для вывода доски врага) или нет (False - для своей доски).
        self.living_ships = living_ships    # количество живых кораблей на доске

    def __str__(self):
        return f"Board({self.all_board}, {self.all_ships}, {self.hid}, {self.living_ships})"

    # Метод для точки (объекта класса Dot), который возвращает True, если точка выходит за пределы поля, и False, если не выходит
    def out(self, dot: Dot):
        # Проверяем, находится ли точка за пределами поля по оси X
        if dot.x < 0:                        # Если x меньше 0
            return True                      # Точка выходит за пределы поля
        if dot.x >= len(self.all_board):     # Если x больше или равен количеству строк в поле
            return True                      # Точка выходит за пределы поля

        # Проверяем, находится ли точка за пределами поля по оси Y
        if dot.y < 0:                        # Если y меньше 0
            return True                      # Точка выходит за пределы поля
        if dot.y >= len(self.all_board[0]):  # Если y больше или равен количеству столбцов в поле
            return True                      # Точка выходит за пределы поля

        return False                         # Если ни одно из условий не выполнено, точка находится внутри поля

    # Метод, который ставит корабль на доску (если ставить не получается, выбрасываем исключения)
    def add_ship(self, ship: Ship):
        # Проверка каждой точки корабля
        for dot in ship.dots():
            # Проверка, не выходит ли точка за пределы поля
            if self.out(dot):
                raise BoardOutException(f"Корабль {ship} выходит за пределы поля.")

            # Проверка, занята ли эта точка другим кораблем
            if self.all_board[dot.x][dot.y] != "o":
                raise Exception(f"Точка {dot} уже занята.")

        # Добавление корабля на доску
        for dot in ship.dots():
            self.all_board[dot.x][dot.y] = "■"      # "■" указывает на присутствие части корабля на доске

        # Добавление корабля в список кораблей доски
        self.all_ships.append(ship)

    # Метод, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке
    def contour(self, ship: Ship):
        # Список направлений для проверки соседних клеток (по вертикали, горизонтали и диагоналям)
        near = [
            (-1, 1), (0, 1), (1, 1),  # Верхние клетки вокруг точки
            (-1, 0),         (1, 0),  # Клетки слева и справа вокруг точки
            (-1,-1), (0,-1), (1,-1)   # Нижние клетки вокруг точки
        ]
        # Перебираем все точки корабля
        for dot in ship.dots():
            # Проверяем все соседние клетки
            for dx, dy in near:
                contour_dot = Dot(dot.x + dx, dot.y + dy)
                # Проверка, не выходит ли точка за пределы поля
                if not self.out(contour_dot):
                    # Проверяем, что клетки вокруг корабля не заняты
                    if self.all_board[contour_dot.x][contour_dot.y] != "o":
                        raise Exception("Соседняя клетка занята! Корабли должны стоять на расстоянии.")

    # Метод, который выводит доску в консоль в зависимости от параметра hid
    def visibility_of_ships(self, label=" "):
        # Заголовок для доски
        board_header = f"{label} | a | b | c | d | e | f |"
        print(board_header)

        # Печатаем доску построчно
        for i in range(len(self.all_board)):
            row = self.all_board[i]
            row_str = f" {i + 1} | "     # Делаем индексацию с 1 для строк
            # Обрабатываем каждую ячейку в строке
            for cell in row:
                # Проверяем, нужно ли скрыть корабль ("■") или оставить значение ячейки
                if self.hid and cell == "■":
                    row_str += "o"      # Заменяем корабль на "o", если hid = True
                else:
                    row_str += cell     # Иначе добавляем текущее значение ячейки
                row_str += " | "        # Добавляем разделитель между ячейками
            print(row_str)              # Печатаем итоговую строку для текущей строки доски

    # Метод, который делает выстрел по доске.
    def shot(self, dot: Dot):
        # Уменьшаем x и y на 1, чтобы привести к индексации с "0"
        dot.x -= 1
        dot.y -= 1

        # Проверка на выход за пределы доски
        if self.out(dot):
            raise BoardOutException("Вы выстрелили за пределы поля")

        # Проверка, был ли уже выстрел в эту точку
        if self.all_board[dot.x][dot.y] in ["x", " "]:              # "x" и " " - подбитый корабль и промах
            raise Exception("Вы уже стреляли в эту клетку")

        # Обработка попадания или промаха
        if self.all_board[dot.x][dot.y] == "■":
            self.all_board[dot.x][dot.y] = "x"      # Присваеваем попадание
            print("Попал!")
        else:
            self.all_board[dot.x][dot.y] = " "      # Помечаем промах
            print("Мимо!")



# СОЗДАЕМ КЛАСС ИГРОКА В ИГРУ (AI и USER). ЭТОТ КЛАСС БУДЕТ РОДИТЕЛЕМ ДЛЯ КЛАССОВ c AI и USER:

class Player:
    def __init__(self, user_board: Board, ai_board: Board):
        self.user_board = user_board
        self.ai_board = ai_board

    def __str__(self):
        return f"Player({self.user_board}, {self.ai_board})"

    # Метод ask, который «спрашивает» игрока, в какую клетку он делает выстрел.
    def ask(self):
        """Метод-заглушка для запроса клетки для выстрела.
                   В классе-наследнике будет переопределен для пользователя или ИИ."""
        raise NotImplementedError("Метод ask должен быть переопределен в подклассе.")

    # Метод move, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел по вражеской доске (метод Board.shot),
    # отлавливаем исключения, и если они есть, пытаемся повторить ход. Метод должен возвращать True, если этому игроку нужен повторный
    # ход (например, если он выстрелом подбил корабль).
    def move(self):
        while True:
            try:
                # Получаем точку для выстрела
                target_dot = self.ask()
                # Выполняем выстрел по вражеской доске
                shot_at_target = self.ai_board.shot(target_dot)
                return shot_at_target              # Возвращает True, если нужен повторный ход (например, при попадании)

            except BoardOutException as e:
                print(e)
                print("Попробуйте снова: нельзя стрелять за пределы поля.")

            except Exception as e:
                print(e)
                print("Попробуйте снова: что-то пошло не так.")

class AI(Player):
    def ask(self):
        # Генерируем случайные координаты для выстрела
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        print(f"AI стреляет в точку ({x + 1}, {y + 1})")  # Для наглядности выводим координаты в формате 1-6
        return Dot(x, y)

class User(Player):
    def ask(self):
        while True:
            try:
                # Запрашиваем координаты у пользователя
                coords = input("Введите координаты для выстрела (например 'a1', 'd5'): ").lower()

                # Проверяем, что пользователь ввёл две координаты
                if len(coords) != 2:
                    raise ValueError("Неверный формат. Введите координаты как 'a1', 'b2' и т.п.")

                # Преобразуем координаты в числа и проверяем их корректность
                column, row = coords[0], coords[1]
                # Преобразуем столбец 'a'..'f' в индексы
                if column not in 'abcdef' or not row.isdigit() or not (1 <= int(row) <= 6):
                    raise BoardOutException("Координаты вне пределов игрового поля.")
                # Преобразуем в индексы
                x = ord(column) - ord('a')          # Преобразуем букву в индекс столбца
                y = int(row) - 1                    # Преобразуем строку в индекс

                return Dot(x, y)

            except ValueError as e:
                print(f"Ошибка: {e}. Пожалуйста, попробуйте снова.")
            except BoardOutException as e:
                print(f"Ошибка: {e}. Пожалуйста, попробуйте снова.")



# СОЗДАЕМ ГЛАВНЫЙ КЛАСС ВСЕЙ ИГРЫ:

class Game:
    def __init__(self):
        # Генерация случайных досок для пользователя и компьютера
        self.user_board = self.random_board()               # Используем self.user_board для сохранения
        self.ai_board = self.random_board(hid=True)         # Указываем hid=True, чтобы скрыть корабли компьютера
        # Инициализация игроков
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    # Метод для случайной генерации доски
    def random_board(self, hid=False):
        while True:
            board = Board(all_board=[['o']*6 for _ in range(6)], all_ships=[], hid=hid, living_ships=0)
            attempts = 0  # Счетчик попыток для проверки неудачных расстановок

            # Проходимся от длинных кораблей к коротким
            for length in [3, 2, 2, 1, 1, 1, 1]:
                while True:
                    attempts += 1
                    # Генерация случайной точки и направления
                    bow_ship = Dot(random.randint(0, 5), random.randint(0, 5))
                    direction = random.randint(0, 1)
                    amount_life = length    # Жизни корабля по умолчанию равны его длине
                    ship = Ship(length, bow_ship, direction, amount_life)

                    # Пытаемся добавить корабль на доску
                    try:
                        board.add_ship(ship)
                        break
                    except Exception:
                        if attempts > 2000:  # Прерывание при большом числе неудачных попыток
                            break

            if len(board.all_ships) == 7:
                return board

    # Метод для вывода приветствия
    def greet(self):
        print('Добро пожаловать в игру "Морской бой"!')
        print("Формат ввода координат для выстрела: 'Буква столбца' и 'Номер строки' без пробелов (например, a1, d5)")
        print("Удачи!")

    # Основной игровой цикл
    def loop(self):
        while True:
            # Отображение досок
            print()
            print("Доска пользователя:")
            self.user_board.visibility_of_ships(label="ME")
            print()
            print("Доска компьютера:")
            self.ai_board.visibility_of_ships(label="AI")

            # Ход пользователя
            repeat_user = self.user.move()
            if self.ai_board.living_ships == 0:
                print("Поздравляем, вы победили!")
                break

            # Если нужно повторить ход, пропускаем ход AI
            if repeat_user:
                continue

            # Ход AI
            repeat_ai = self.ai.move()
            if self.user_board.living_ships == 0:
                print("К сожалению, вы проиграли!")
                break

            # Если ход AI был успешен, ход повторяется
            if repeat_ai:
                continue

    # Метод для начала игры
    def start(self):
        self.greet()
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.start()
























