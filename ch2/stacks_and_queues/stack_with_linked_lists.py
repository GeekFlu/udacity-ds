from datastructures.StackLL import Stack
import math

"""
Reverse Polish Notation

Reverse Polish notation, also referred to as Polish postfix notation is a way of laying out operators and operands.

When making mathematical expressions, we typically put arithmetic operators (like +, -, *, and /) between operands. For example: 5 + 7 - 3 * 8

However, in Reverse Polish Notation, the operators come after the operands. For example: 3 1 + 4 *

The above expression would be evaluated as (3 + 1) * 4 = 16

The goal of this exercise is to create a function that does the following:

    Given a postfix expression as input, evaluate and return the correct final answer.

Note: In Python 3, the division operator / is used to perform float division. So for this problem, you should use int() after every division to convert the answer to an integer.

"""


def evaluate_post_fix(input_list):
    """
    Evaluate the postfix expression to find the answer

    PAY ATTENTION to the order of the popped elements, the first popped element is the second number in the operation

    Args:
       input_list(list): List containing the postfix expression
    Returns:
       int: Postfix expression solution
    """
    s = Stack()
    if input_list is None:
        return None
    if len(input_list) <= 0:
        return None
    for num_operand in input_list:
        if num_operand == '*':
            second = s.pop()
            first = s.pop()
            output = first * second
            s.push(output)
        elif num_operand == '/':
            second = s.pop()
            first = s.pop()
            output = int(first / second)
            s.push(output)
        elif num_operand == '+':
            second = s.pop()
            first = s.pop()
            output = first + second
            s.push(output)
        elif num_operand == '-':
            second = s.pop()
            first = s.pop()
            output = first - second
            s.push(output)
        else:
            s.push(int(num_operand))
    return s.pop()


def equation_checker(equation):
    """
    Check equation for balanced parentheses

    Args:
       equation(string): String form of equation
    Returns:
       bool: Return if parentheses are balanced or not
    """
    s = Stack()
    if equation is None:
        return False
    if len(equation) <= 0:
        return False

    for letter in equation:
        if letter == '(':
            s.push(letter)
        elif letter == ')':
            if s.pop() is None:
                return False

    if s.size() == 0:
        return True
    else:
        return False


def reverse_stack(stack):
    """
    Reverse a given input stack, if the stack was implemented using a linked list only by reversing the linked list
    would be enough, but if the stack is implemented using an array this inversion method does not work.

    Args:
       stack(stack): Input stack to be reversed
    Returns:
       stack: Reversed Stack
    """
    r_stack = Stack()
    if stack is None:
        return None
    if stack.is_empty():
        return None

    while not stack.is_empty():
        r_stack.push(stack.pop())

    return r_stack


"""
Problem Statement

Given an input string consisting of only { and }, figure out the minimum number of reversals required to make the brackets balanced.

For example:

    For input_string = "}}}}, the number of reversals required is 2.

    For input_string = "}{}}, the number of reversals required is 1.

If the brackets cannot be balanced, return -1 to indicate that it is not possible to balance them.

An Efficient Solution can solve this problem in O(n) time. The idea is to first remove all balanced part of expression. 
For example, convert “}{{}}{{{” to “}{{{” by removing highlighted part. If we take a closer look, we can notice that, 
after removing balanced part, we always end up with an expression of the form }}…}{{…{, 
an expression that contains 0 or more number of closing brackets followed by 0 or more numbers of opening brackets.

How many minimum reversals are required for an expression of the form “}}..}{{..{” ?. 
Let m be the total number of closing brackets and n be the number of opening brackets. We need ⌈m/2⌉ + ⌈n/2⌉ reversals. 
For example }}}}{{ requires 2+1 reversals. 
"""


def minimum_bracket_reversals(input_string):
    """
    Calculate the number of reversals to fix the brackets

    Args:
       input_string(string): Strings to be used for bracket reversal calculation
    Returns:
       int: Number of bracket reversals needed
    """
    if input_string is None:
        return None
    if len(input_string) % 2 != 0:
        return -1
    stack_brackets = Stack()
    for letter in input_string:
        if letter == '}':
            if stack_brackets.top() == '{':
                stack_brackets.pop()
            else:
                stack_brackets.push(letter)
        else:
            stack_brackets.push(letter)

    open_b_c = 0
    close_b_c = 0
    while not stack_brackets.is_empty():
        if stack_brackets.top() == '{':
            stack_brackets.pop()
            open_b_c += 1
        elif stack_brackets.top() == '}':
            stack_brackets.pop()
            close_b_c += 1
    return math.ceil(open_b_c / 2) + math.ceil(close_b_c / 2)


if __name__ == "__main__":
    s_ = Stack()
    s_.push(1)
    s_.push(2)
    s_.push(3)
    print(s_.pop())
    print(s_.pop())
    print(s_.pop())
    print(s_.pop())

    for i in range(1000):
        s_.push(i)

    for i in range(999):
        s_.pop()

    assert s_.size() == 1
    print(s_.pop())

    print("Pass" if (equation_checker('((3^2 + 8)*(5/2))/(2+6)')) else "Fail")
    print("Pass" if not (equation_checker('((3^2 + 8)*(5/2))/(2+6))')) else "Fail")

    assert evaluate_post_fix(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    assert evaluate_post_fix(["4", "13", "5", "/", "+"]) == 6
    assert evaluate_post_fix(["3", "1", "+", "4", "*"]) == 16

    orig_stack = Stack()
    orig_stack.push(1)
    orig_stack.push(2)
    orig_stack.push(3)
    rev_stack = reverse_stack(orig_stack)
    for _ in range(rev_stack.size()):
        print(rev_stack.pop())

    assert minimum_bracket_reversals("}}{{") == 2
    assert minimum_bracket_reversals("}}}}") == 2
    assert minimum_bracket_reversals("{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}") == 13
    assert minimum_bracket_reversals("}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{") == 2
    assert minimum_bracket_reversals("}}{}{}{}{}{}{}{}{}{}{}{}{}{}{}") == 1
