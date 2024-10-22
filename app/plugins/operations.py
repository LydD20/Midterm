'''Calculator Operations'''
import logging

class Operations:
    def __init__(self):
        self.result= [] #storing the results

    def add(self, num1, num2):
        '''adding function'''
        result = num1 + num2
        self.results.append({"Operation": "addition", "result": result}) #stores addition result
        return result
    
    def subtract(self, num1, num2):
        '''subtracting function'''
        result = num1 - num2
        self.results.appemd({"Operation": "subtraction", "result": result}) #stores subtraction result
        return result
    
    def divide(self, num1, num2):
        '''dividing function'''
        try:
            if num2==0:
                raise ValueError("Division by zero is not allowed")
            result= num1/num2
            self.result.append({"Operation": "division", "result": result}) #stores division result
            return result
        except ValueError as e:
            logging.error(F"Error: {e}")

    
    def multiply(self, num1, num2):
        '''multiplying function'''
        result= num1 * num2
        self.result.append({"Operation": "multiplication", "result": result}) #stores multiplication result
        return result
    
    def retrieve_results(self):
        '''retrieves results'''
        return self.resutlts
    
