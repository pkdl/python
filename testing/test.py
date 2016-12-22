import unittest
from io import StringIO
from unittest.mock import patch

from model import *

class TestScope(unittest.TestCase):
    def testStorage(self):
        s0 = Scope()
        s0["v1"] = 123
        s0["v2"] = "qwe"

        self.assertEqual(s0["v1"], 123)
        self.assertEqual(s0["v2"], "qwe")

    def testInheritance(self):
        s0 = Scope()
        s1 = Scope(s0)

        s0["v1"] = 123
        s1["v1"] = 456
        s0["v2"] = 789

        self.assertEqual(s1["v1"], 456)
        self.assertEqual(s1["v2"], 789)

        s2 = Scope(s1)
        self.assertEqual(s2["v2"], 789)

class TestNumber(unittest.TestCase):
    def testInit(self):
        s = Scope()
        s["v1"] = Number(5)
        s["v2"] = Number(-8)

        self.assertIsInstance(s["v1"], Number)
        self.assertIsInstance(s["v2"], Number)

    def testEvaluate(self):
        s = Scope()
        s["a"] = Number(5)
        self.assertIs(s["a"], s["a"].evaluate(s))

class TestFunction(unittest.TestCase):
    def testInit(self):
        s = Scope()
        s["func"] = Function([Number(5), Number(7)], [Number(9)])

        self.assertIsInstance(s["func"], Function)
        self.assertIsInstance(s["func"], Function)

    def testEvaluate(self):
        s = Scope()
        s["func"] = Function([Number(5), Number(7)], [Number(9)])

        self.assertIsInstance(s["func"].evaluate(s), Number)

class TestFunctionDefinition(unittest.TestCase):
    def test(self):
        s = Scope()
        f = Function(["args"], [Number(3), Number(5)])
        funcdef = FunctionDefinition("funcname", f)

        self.assertIsInstance(funcdef.evaluate(s), Function)
        self.assertIsInstance(s["funcname"], Function)
        self.assertIs(s["funcname"], f)

    def testEmptyBody(self):
        s = Scope()
        f = Function(["args"], [])
        funcdef = FunctionDefinition("funcname", f)
        
        self.assertIsInstance(funcdef.evaluate(s), Function)
        self.assertIsInstance(s["funcname"], Function)
        self.assertIs(s["funcname"], f)
    
class TestConditional(unittest.TestCase):
    def test(self):
        s = Scope()
        true = Number(17)
        false = Number(0)

        with patch('sys.stdout', new_callable = StringIO) as out:
            c1 = Conditional(true, [Number(1), Number(2)], [Number(3)])
            Print(c1.evaluate(s)).evaluate(s)
            self.assertEqual(int(out.getvalue()), 2)

        with patch('sys.stdout', new_callable = StringIO) as out:
            c2 = Conditional(false, [Number(1), Number(2)], [Number(3)])
            Print(c2.evaluate(s)).evaluate(s)
            self.assertEqual(int(out.getvalue()), 3)

        c3 = Conditional(true, [], [])
        c3.evaluate(s)

        c3 = Conditional(false, [], [])
        c3.evaluate(s)

        c4 = Conditional(true, None, None)
        c4.evaluate(s)

        c4 = Conditional(false, None, None)
        c4.evaluate(s)


class TestPrint(unittest.TestCase):
    def test(self):
        s = Scope()
        with patch('sys.stdout', new_callable = StringIO) as out:
            Print(Number(23)).evaluate(s)
            self.assertEqual(int(out.getvalue()), 23)

class TestRead(unittest.TestCase):
    def test(self):
        s = Scope()
        for i in range(-115, 115):
            with patch('sys.stdin', new = StringIO(str(i))), patch('sys.stdout', new_callable = StringIO) as out:

                a = Read("name").evaluate(s)
                self.assertIsInstance(a, Number)

                op = BinaryOperation(Number(3), "+", a)
                Print(op).evaluate(s)
                self.assertEqual(out.getvalue(), str(i + 3) + '\n')


class TestCall(unittest.TestCase):
    def test(self):
        s = Scope()
        
        f = Function(["a", "b"], [Reference("a"), Reference("b")])
        funcdef = FunctionDefinition("funcname", f)
        call = FunctionCall(funcdef, [Number(17), Number(19)])
        self.assertIsInstance(call.evaluate(s), Number)
        with patch('sys.stdout', new_callable = StringIO) as out:
            Print(call.evaluate(s)).evaluate(s)
            self.assertEqual(int(out.getvalue()), 19)

    def testNoArgs(self):
        s = Scope()
        f = Function([], [Print(Number(13))])
        funcdef = FunctionDefinition("funcname", f)
        call = FunctionCall(funcdef, [])
        with patch('sys.stdout', new_callable = StringIO) as out:
            call.evaluate(s)
            self.assertEqual(int(out.getvalue()), 13)
        
    def testNoBody(self):
        s = Scope()
        f = Function(["a", "b"], [])
        funcdef = FunctionDefinition("funcname", f)
        call = FunctionCall(funcdef, [Number(17), Number(19)])
        call.evaluate(s)

class ReferenceTest(unittest.TestCase):
    def test(self):
        s = Scope()
        s["name"] = Number(42)
        ref = Reference("name")
        self.assertIs(ref.evaluate(s), s["name"])

class BinaryOperationTest(unittest.TestCase):

    def test(self):
        s = Scope()

        for op in ['+', '-', '*', '/', '%', '&&', '||', '==', '!=', '<', '>', '<=', '>=']:
            for l in range(-15, 15):
                for r in range(-15, 15):
                    if op in ['/', '%'] and r == 0:
                        continue

                    res = BinaryOperation(Number(l), op, Number(r)).evaluate(s)
                    self.assertIsInstance(res, Number)
                    with patch('sys.stdout', new_callable = StringIO) as out:
                        Print(res).evaluate(s)
                        if op == '+':
                            self.assertEqual(out.getvalue(), str(l + r) + '\n')
                        elif op == '-':
                            self.assertEqual(out.getvalue(), str(l - r) + '\n')
                        elif op == '*':
                            self.assertEqual(out.getvalue(), str(l * r) + '\n')
                        elif op == '/':
                            self.assertEqual(out.getvalue(), str(l // r) + '\n')
                        elif op == '%':
                            self.assertEqual(out.getvalue(), str(l % r) + '\n')
                        elif op == '&&':
                            self.assertEqual(bool(int(out.getvalue())), bool(l and r))
                        elif op == '||':
                            self.assertEqual(bool(int(out.getvalue())), bool(l or r))
                        elif op == '==':
                            self.assertEqual(bool(int(out.getvalue())), bool(l == r))
                        elif op == '!=':
                            self.assertEqual(bool(int(out.getvalue())), bool(l != r))
                        elif op == '<':
                            self.assertEqual(bool(int(out.getvalue())), bool(l < r))
                        elif op == '>':
                            self.assertEqual(bool(int(out.getvalue())), bool(l > r))
                        elif op == '<=':
                            self.assertEqual(bool(int(out.getvalue())), bool(l <= r))
                        elif op == '>=':
                            self.assertEqual(bool(int(out.getvalue())), bool(l >= r))            

class UnaryOperationTest(unittest.TestCase):

    def test(self):
        s = Scope()
        for op in ['-', '!']:
            for a in range(-15, 15):
                with patch('sys.stdout', new_callable = StringIO) as out:
                    Print(UnaryOperation(op, Number(a))).evaluate(s)
                    if op == '-':
                        self.assertEqual(out.getvalue(), str(-a) + '\n')
                    if op == '!':
                        self.assertEqual(bool(int(out.getvalue())), bool(not a))

if __name__ == '__main__':
    unittest.main()
