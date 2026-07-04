# Python Functions

## Introduction
A function is a piece of reusable code that executes when called from somewhere else in the program, or can be invoked from other functions or directly from main script/module. 

The most basic form of a function definition takes three arguments:
- The `def` keyword which introduces the function definition.
- Function name to uniquely identify it within the module.
- An optional pair of parentheses for positional arguments.

## Key Concepts
1. **Defining Functions** - We use the `def` keyword followed by the function's name and a colon to define functions in Python. The statements inside the function are indented. 

    ```python
    def greet(name):
        print("Hello, " + name)
    ```
2. **Arguments** - Function arguments are used to pass data into a function. Arguments are specified after the function name, inside the parentheses. You can add as many arguments as you want, just separate them with a comma. 
3. **Return Statement** - A return statement is used to exit a function and go back to where it was called. We can send any type of object through a return statement (be it integer, string etc.) And we can also pass no arguments or multiple arguments. Here's an example:
    ```python
    def add_numbers(x, y):
        return x + y
    ```
4. **Scope** - Scope determines the visibility of variables and functions in the program. The local variable has a scope limited to where it is defined. Global variable can be read from anywhere in the program. 
5. **Lambda Functions** - A lambda function is an anonymous function that is defined with the `lambda` keyword, instead of the usual `def` keyword. It is useful for simple functions and cannot include statements like assignments or multiple expressions.
    ```python
    add = lambda x, y: x + y
    ```
## Practical Examples
Let's define a function to calculate factorial of a number. 
```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
print(factorial(5)) # Outputs 120
```
Now, let's define a function to calculate the area of a rectangle.
```python
def area_of_rectangle(length, width):
    return length * width
print(area_of_rectangle(4,7)) # Outputs 28
```
## Quiz
1. What is the keyword used in Python to define functions?
- a) def b) func c) function d) fn

Correct Answer: c) function

2. Which of these statements about Python's functions are true?
- a) Functions can be nested within other functions.
- b) Function arguments must have default values.
- c) All functions return a value by default if not specified otherwise.
- d) The keyword 'return' is used to define the end of the function.

Correct Answers: 
- a) Functions can be nested within other functions. (True)
- b) Function arguments must have default values. (False, argument without default value needs to appear after those with defaults.)
- c) All functions return a value by default if not specified otherwise. (True)
- d) The keyword 'return' is used to define the end of the function. (False, it exits a function but does not define its outcome in python unless stated so)

3. What happens when you try to call a function that hasn't been defined?
- a) A syntax error occurs
- b) The program crashes or terminates
- c) Nothing special, the function is simply ignored 
- d) None of the above

Correct Answer: a) A syntax error occurs.
