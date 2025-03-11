#!/usr/bin/env python3
# One-File Python Brainfuck Compiler by KTILTED

lang = None

while lang != "Russian" or "English":
	lang = input("Select language: Russian or English: ")
	if lang == "Russian":
		welcomeText = "Добро пожаловать в компилятор Brainfuck! Введите help для вывода справки."
		selectDirectory = "Введите директорию файла .bf. Не используйте кавычки!\nДиректория: "
		notFound = "Ошибка FileNotFoundError: указанный вами файл или директория неверны."
		inputCode = "Введите код для компиляции: "
		brainfuckHelp = '''Brainfuck — эзотерический язык программирования, который использует символы в качестве функций.

+ — увеличение значения ячейки на 1
- — уменьшение значения ячейки на 1
< — предыдущая ячейка
> — следующая ячейка
[ — начало цикла. Цикл длится пока значение в текущей ячейке не станет равно 0
] — конец цикла
. — вывод значения в текущей ячейке
, — запрос ввода значения для ячейки

Все значения являются символами в таблице ASCII.
Все символы, не являющиеся этими функциями считаются комментариями и не учитываются при компиляции.
Функция , принимает только один символ, в случае введения больше одного примет только первый, а остальные проигнорирует.'''
		helpText = '''run — использовать файл .bf для компиляции
input — ввести код в программе и скомпилировать его
bfhelp — справка по языку Brainfuck
help — вывести этот текст'''
		unknownCommand = "Неизвестная команда. Введите help для вывода справки."
		syntaxError = "Незакрытый цикл"
		typeSymbol = "Введите символ: "
		error = "Ошибка: "
		break
	elif lang == "English":
		welcomeText = "Welcome to the Brainfuck compiler! Use 'help' to see help."
		selectDirectory = "Type .bf file directory. Don't use quotes!\nDirectory: "
		notFound = "FileNotFoundError: directory or file are incorrect."
		inputCode = "Type the code for compilation: "
		brainfuckHelp = '''Brainfuck is an esoteric programming language which uses chars for functions.

+ — increase cell value for 1 point
- — decrease cell value for 1 point
< — move to previous cell
> — move to next cell
[ — cycle start. Cycle going while value in a selected cell won't be zero
] — cycle end
. — print value of the selected cell
, — request input for the selected cell

All the cell values are standing for the symbols in the ASCII table.
All the symbols which is not these functions compiler understands like a comments and ignores them.
, function takes only one symbol. In case of typing more than one it take only first and ignore others.'''
		helpText = '''run — run .bf file for compilation.
input — type the code in this app and compile it
bfhelp — learn how to code on Brainfuck
help — print this text'''
		unknownCommand = "Unknown command. Type 'help' to see help."
		syntaxError = "Unclosed cycle"
		typeSymbol = "Type symbol: "
		error = "Error: "
		break
	else:
		print("Language selection is incorrect! Try again.\n")

def bfcompile(code):
	cells = [0] * 256 # Создаём массив с ячейками
	cellIndex = 0 # Индекс ячейки
	codePointer = 0 # Указатель на текущую команду для работы с циклами

	bracketPairs = {} # Словарь для хранения пар скобок
	stack = [] # Стак для нахождения пар скобок

	for i in range(len(code)):
		if code[i] == "[":
			stack.append(i) # Находим открывающую скобку
		elif code[i] == "]":
			if not stack:
				raise SyntaxError(syntaxError)
			start = stack.pop() # Находим закрывающую скобку
			bracketPairs[start] = i
			bracketPairs[i] = start
	if stack:
		raise SyntaxError(syntaxError)

	# Основной цикл выполнения кода
	while codePointer < len(code):
		command = code[codePointer]

		if command == "+":
			cells[cellIndex] = (cells[cellIndex] + 1) % 256  # Увеличиваем значение ячейки (с учётом переполнения)
		elif command == "-":
			cells[cellIndex] = (cells[cellIndex] - 1) % 256  # Уменьшаем значение ячейки (с учётом переполнения)
		elif command == "<":
			cellIndex = (cellIndex - 1) % 256  # Перемещаемся влево (с учётом переполнения)
		elif command == ">":
			cellIndex = (cellIndex + 1) % 256  # Перемещаемся вправо (с учётом переполнения)
		elif command == "[":
			if cells[cellIndex] == 0:
				codePointer = bracketPairs[codePointer]  # Переходим к закрывающей скобке
		elif command == "]":
			if cells[cellIndex] != 0:
				codePointer = bracketPairs[codePointer]  # Возвращаемся к открывающей скобке
		elif command == ".":
			print(chr(cells[cellIndex]), end="")
		elif command == ",":
			symbolInput = input(typeSymbol)
			if symbolInput:
				cells[cellIndex] = ord(symbolInput[0])

		codePointer += 1  # Переходим к следующей команде

	return cells

print(welcomeText)

while True: # Реализация команд
	command = input("\nbfcompiler ~ > ")
	if command == "help":
		print(helpText)
	elif command == "run":
		codeFile = input(selectDirectory)
		try:
			with open(codeFile, "r") as file:
				content = file.read()
				bfcompile(content)
		except FileNotFoundError:
			print(notFound)
		except Exception as e:
			print(error + e)
	elif command == "input":
		print(brainfuckHelp)
		code = input(inputCode)
		bfcompile(code)
	elif command == "bfhelp":
		print(brainfuckHelp)
	else:
		print(unknownCommand)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)

    codeFile = sys.argv[1]
    try:
        with open(codeFile, "r") as file:
            code = file.read()
            bfcompile(code)
    except FileNotFoundError:
        print(f"Файл {codeFile} не найден!")
    except Exception as e:
        print(f"Ошибка: {e}")