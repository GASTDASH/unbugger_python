import ast
import inspect
import unittest

def create_tests(code_file):
    with open(code_file, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = ast.parse(code)
    print(ast.dump(tree, indent = 4))

    # Поиск функций и классов в коде
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]

    # Создание тестовых методов для функций
    for func in functions:
        func_name = func.name
        exec(
f'''
class Test{func_name}(unittest.TestCase):
    def test_{func_name}(self):
        # обновить с реальными параметрами для тестирования
        self.assertIsNone({func_name}())
''', globals())

    # Создание тестовых классов для классов
    for cls in classes:
        cls_name = cls.name
        exec(
f'''
class {cls_name}(unittest.TestCase):
    def test_{cls_name}(self):
        # создать экземпляр класса и вызвать методы для тестирования
        pass
''', globals())

    # Запуск тестов
    unittest.main()

create_tests("./run.py")