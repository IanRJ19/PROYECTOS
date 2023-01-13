from difflib import SequenceMatcher as SM

s1 = 'Hola Mundo'
s2 = 'Hola Mundo cruel'
print(SM(None, s1, s2).ratio())

s1 = 'Hola Mundo'
s2 = 'Hola Mundo!'
print(SM(None, s1, s2).ratio())
