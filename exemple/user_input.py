def reverse(text): #переворачивает
    return text[::-1]

def is_palindrome(text): #проверяет
    return text.replace(' ', '').casefold() == reverse(text).replace(' ', '').casefold()

something = input('Введите текст: ')
if (is_palindrome(something)):
    print("Да, это палиндром")
else:
    print("Нет, это не палиндром")
