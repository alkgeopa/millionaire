from colorama import Fore, Back, Style

def dPN(message: str='') -> str:
    print(message)
    return message

def dPW(message: str='') -> str:
    print(f'{Back.YELLOW}{Fore.BLACK}{message}{Style.RESET_ALL}')
    return message

def dPE(message: str='') -> str:
    print(f'{Back.RED}{Fore.WHITE}{message}{Style.RESET_ALL}')
    return message
