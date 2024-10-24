'''Calculator Operations'''
import logging

import logging

class Operations:
    def __init__(self):
        self.results = []  # storing the results

    def add(self, num1, num2):
        '''adding function'''
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise TypeError("Both arguments must be numbers.")
        result = num1 + num2
        self.results.append({"Operation": "addition", "result": result})  # stores addition result
        return result

    def subtract(self, num1, num2):
        '''subtracting function'''
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise TypeError("Both arguments must be numbers.")
        result = num1 - num2
        self.results.append({"Operation": "subtraction", "result": result})  # stores subtraction result
        return result

    def divide(self, num1, num2):
        '''dividing function'''
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise TypeError("Both arguments must be numbers.")
        if num2 == 0:
            raise ValueError("Division by zero is not allowed.")
        result = num1 / num2
        self.results.append({"Operation": "division", "result": result})  # stores division result
        return result

    def multiply(self, num1, num2):
        '''multiplying function'''
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise TypeError("Both arguments must be numbers.")
        result = num1 * num2
        self.results.append({"Operation": "multiplication", "result": result})  # stores multiplication result
        return result

    def retrieve_results(self):
        '''retrieves results'''
        return self.results
