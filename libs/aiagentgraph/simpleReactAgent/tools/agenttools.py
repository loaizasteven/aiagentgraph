from langchain.tools import tool

@tool
def calculate(expression:str) -> str:
    "Runs a calculation and returns the number. Uses Python syntax."
    return eval(expression)

@tool
def average_dog_weight(breed:str) -> str:
    """Returns average weight of a dog when given the breed. Dog breed name is case sensitive
    Example
    average_dog_weight(Collie)
    """
    print('this is the input', breed, breed == "Toy Poodle")
    if breed in "Scottish Terrier": 
        return("Scottish Terriers average 20 lbs")
    elif breed in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif breed in "Toy Poodle":
        return("a toy poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")
