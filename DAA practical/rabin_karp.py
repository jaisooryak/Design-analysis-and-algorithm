import time
import random
import string
def naive_search(text, pattern):
 n, m = len(text), len(pattern)
 matches, comparisons = [], 0
 for i in range(n - m + 1):
  j = 0
 while j < m:
  comparisons += 1
 if text[i + j] != pattern[j]:
   break
 j += 1
 if j == m:
 matches.append(i)
 return matches, comparisons

def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0
    while i < n:
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons

def rabin_karp_search(text, pattern, prime=101):
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    if m > n:
        return matches, comparisons

    base = 256
    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * base) % prime

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        comparisons += 1
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                matches.append(i)

        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if text_hash < 0:
                text_hash += prime

    return matches, comparisons

text ='AABAACAADAABAABA'
pattern = 'AABA'
print(f'Text: {text}')
print(f'Pattern: {pattern}')
m1, c1 = naive_search(text, pattern)
m2, c2 = kmp_search(text, pattern)
m3, c3 = rabin_karp(text, pattern)
print(f'\nNaive -> Matches at: {m1}, Comparisons: {c1}')
print(f'KMP -> Matches at: {m2}, Comparisons: {c2}')
print(f'RK -> Matches at: {m3}, Comparisons: {c3}')
# Performance comparison
text_large = ''.join(random.choices('ABCD', k=10000))
patterns = ['AB', 'ABCD', 'ABCDAB', 'ABCDABCD']
print(f'\n{"Pattern":>12} {"Naive":>10} {"KMP":>10} {"RK":>10}')
print('-' * 50)
for p in patterns:
 _, c1 = naive_search(text_large, p)
 _, c2 = kmp_search(text_large, p)
 _, c3 = rabin_karp(text_large, p)
 print(f'{p:>12} {c1:>10} {c2:>10} {c3:>10}')
