import sys
import os
import scanner
import error
import parser_
import ast_printer
import interpreter
import resolver


def main():
    arg_len = len(sys.argv)
    if arg_len > 2:
        print("Usage: plox [script]")
        os._exit(0)
    elif arg_len == 2:
        runFile(sys.argv[1])
    else:
        runPrompt()


def runFile(path):
    source = open(path).read()
    run(source)
    if error.hadError:
        os._exit(0)


def runPrompt():
    while True:
        print("> ", end="")
        line = input()
        if line == "":
            break
        run(line)
        if error.hadError:
            error.hadError = False
            pass


def run(source):
    scanner_instance = scanner.Scanner(source)
    tokens = scanner_instance.scanTokens()
    if error.hadError:
        return

    parser_instance = parser_.Parser(tokens)
    statements = parser_instance.parse()
    if error.hadError:
        return

    interpreter_ = interpreter.Interpreter()
    resolver.Resolver(interpreter_).resolve(statements)
    if error.hadError:
        return

    interpreter_.interpret(statements)
    if error.hadRunTimeError:
        return
    # output = ast_printer.AstPrinter().print(ast)
    # print(output)


if __name__ == '__main__':
    main()
