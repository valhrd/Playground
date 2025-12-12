import json

with open('w1.json', 'r') as f:
    ciphertexts = json.load(f)

def hex_to_dec(s):
    assert len(s) == 2
    h = {str(i): i for i in range(10)}
    h |= {chr(ord('a') + i): 10 + i for i in range(6)}
    return h[s[0]] * 16 + h[s[1]]

def hex_to_declist(s):
    return [hex_to_dec(s[i:i+2]) for i in range(0, len(s), 2)]

def xor(lst1, lst2):
    if len(lst1) > len(lst2):
        return [(a ^ b) for a, b in zip(lst1[:len(lst2)], lst2)]
    return [(a ^ b) for a, b in zip(lst1, lst2[:len(lst1)])]

def to_ascii(lst):
    return [chr(v) for v in lst]

def xor_sample(val):
    chars = 'qwertyuiopasdfghjklzxcvbnm'
    charlist = sorted(list(chars + chars.upper()))
    print(f"ASCII equiv: {chr(val)}")
    for c in charlist:
        xor_val = val ^ ord(c)
        print(f"Character: {c}, XOR val with space: {xor_val}, ASCII equiv: {chr(xor_val)}")

def notable_indices(lst):
    return [ord(' ') if ord('a') <= ord(c) <= ord('z') or ord('A') <= ord(c) <= ord('Z') else 0 for i, c in enumerate(lst)]

lst = hex_to_declist(ciphertexts['7'])
key = xor(lst, [ord(c) for c in list("There are two types of cyptography: one that allows the Government to use brute force to break the code, and one that requires the Government to use brute force to break your codes")])
for c in [str(i) for i in range(1, 11)]:
    lst = hex_to_declist(ciphertexts[c])
    print(f'Ciphertext #{c}: Missing {max(0, len(lst) - len(key))} chars')
    print(''.join(to_ascii(xor(lst, key))))
print(key)
target = hex_to_declist(ciphertexts['target'])
print(len(target), len(key))
print(''.join(to_ascii(xor(target, key))))

# main = '2'
# lst1 = hex_to_declist(ciphertexts[main])
# for c in [str(i) for i in range(1, 11)]:
#     if main == c:
#         continue
#     lst2 = hex_to_declist(ciphertexts[c])
#     xored_lsts = xor(lst1, lst2)
#     ascii_lst = to_ascii(xored_lsts)
#     print('-' * 100)
#     print(xored_lsts)
#     print(ascii_lst)
# xor_sample(82)