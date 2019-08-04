"""
Specialized encryption algorithm. It was invented by ancient Egyptians.

Very sophisticated and looks secure.

It encodes strings by replacing each letter with another

Example.

Input: abc
Output: zyx
"""

intab = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
trantab = ''.join(reversed(intab))


def encrypt(message, key):
    table = str.maketrans(intab, trantab)
    return (message + key).translate(table)


def decrypt(message, key):
    table = str.maketrans(trantab, intab)
    content = message.translate(table)
    text = content[:-8]
    key_ = content[-8:]
    if key_ == key:
        return text
    else:
        raise ValueError('Invalid Key!')
