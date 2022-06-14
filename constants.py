from typedef import AmountType

"""
Collection of various constants and reference lists
"""

# View
MAINMENU = 'mainmenu'
HALLOFFAME = 'halloffame'
GAME = 'game'
USERINPUT = 'userinput'
VICTORY = 'victory'
DEFEAT = 'defeat'

# view list
VIEWS = [
    'mainmenu',
    'halloffame',
    'game',
    'userinput',
    'victory',
    'defeat'
]

# Stage
EASY = 'ε'
MEDIUM = 'μ'
HARD = 'δ'

# Lifelines
LIFELINES = [
    '50-50',
    'computer',
    'skip'
]

# Answer Dimensions
ANSWERWIDTH = 116
ANSWERHEIGHT = 86

# Amounts
AMOUNTS: list[AmountType] = [
    {
        "string": "100 €",
        "numeric": 100,
    },
    {
        "string": "200 €",
        "numeric": 200,
    },
    {
        "string": "300 €",
        "numeric": 300,
    },
    {
        "string": "500 €",
        "numeric": 500,
    },
    {
        "string": "1.000 €",
        "numeric": 1000,
    },
    {
        "string": "1.500 €",
        "numeric": 1500,
    },
    {
        "string": "2.000 €",
        "numeric": 2000,
    },
    {
        "string": "3.500 €",
        "numeric": 3500,
    },
    {
        "string": "5.000 €",
        "numeric": 5000,
    },
    {
        "string": "7.500 €",
        "numeric": 7500,
    },
    {
        "string": "10.000 €",
        "numeric": 10000,
    },
    {
        "string": "20.000 €",
        "numeric": 20000,
    },
    {
        "string": "50.000 €",
        "numeric": 50000,
    },
    {
        "string": "100.000 €",
        "numeric": 100000,
    },
    {
        "string": "250.000 €",
        "numeric": 250000,
    },
]
