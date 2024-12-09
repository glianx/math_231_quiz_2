# %% [markdown]
# # 3
# 
# sources: 
# 
# my notes on likelihood, metro-hastings
# 
# codeium fast on \because symbol
# 
# https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
# 
# claude 3.5 sonnet:
# why conditional for (q,u) is greater than 1, appears miscount number of qs in emma.txt
# 
# the number of characters is off by much more than 1, chararray[q] should be 1296 not 375
# 
# ---
# 
# **1**
# How many possible codebooks are there given that each codebook is a permutation of the letters A to Z?
# 
# 
# There there are 26! (factorial) possible codebooks. nPr = 26 P 26 = 26!/(26-26)! = 26!/0! = 26!
# 
# 
# **2**
# Would it be feasible to calculate $\pi(B)$ directly for a code book $B$ applied to an encrypted text $C$? 
# 
# 
# Explain the different difficulties that might exist.
# 
# 
# 
# No, it would be infeasible to calculate $\pi(B)$ directly for a code book $B$ applied to an encrypted text $C$, because one must consider all of the many other potential code books which could have been applied and evaluate the probability that they were used. 
# 
# By Baye's,
# 
# $P(\lambda|D) = P(D|\lambda) * \frac{P(\lambda)}{P(D)}$
# 
# $P(B|C) = P(C|B) * \frac{P(B)}{P(C)}$
# 
# so
# 
# $\pi(B)=\frac{1}{Z} e^{l(A_B)} = \frac{1}{Z}P(A_B) = \frac{1}{Z}P(A|B) = \frac{P(B)}{P(A)}*P(A|B)$
# 
# $P(A|B) = P(B^{-1}(A))$ because the probability that the cipher appears for the code book is the chance that its plaintext appears in English.
# 
# **3**
# 
# Show that the sample “swap chain” on codebooks is a symmetric Markov Chain. That is to say, if 
# $T$ is the Markov transition matrix for the swap chain and $B$ and $B'$ are two possible codebooks then $T(B, B')=T(B', B)$. Don’t try to write down $T$ as it is huge. Just argue directly. What is the probability of proposing any particular “swap” given a codebook $B$?
# 
# Case 1: $B$ can reach $B'$ in exactly one swap. Let $a$, $b$ be the characters which must be swapped to reach from $B$ to $B'$, or from $B'$ to $B$. Note that the swapping is symmetric, and swapping twice results in the same codebook. Then the chance the the unordered pair $(a,b)$ is chosen is
# 
# $T(B,B') = \frac{1}{26 \choose 2} = \frac{1}{325}= T(B',B)$
# 
# Case 2: $B$ cannot reach $B'$ in exactly one swap. Either $B = B'$, or $B'$ is 'far' from $B$ in terms of swaps needed. Then
# 
# $T(B,B') = 0 = T(B',B)$
# 
# **4**
# 
# We will use a Metropolis-Hastings MCMC algorithm to sample from the $\pi$ defined above. What is the acceptance probability if we use a proposal of the simple swap chain? Please simplify your expression using that the proposal chain is symmetric. Explain.
# 
# $\alpha(B,B') = min(1,\frac{\pi(B')T(B',B)}{\pi(B)T(B,B')}) = min(1,\frac{\pi(B')}{\pi(B)}) = min(1,e^{l(A_{B'})-l(A_B)})$
# 
# $\because T(B',B) = T(B,B')$

# %%
import random as rnd
def randomCodebook(): 
    alpha = [chr(c) for c in range(ord('A'), ord('A')+26)]  # create list A-Z
    alpha2 = alpha.copy()  # Start with every letter mapping to itself
    rnd.shuffle(alpha2)  # shuffle letter around to create a random permutation
    codeBook = {a: code for a, code in zip(alpha, alpha2)}  # Make a dictionary
    return codeBook
codebook = randomCodebook()
print(codebook)

# %%
# make sure the character is in the range we expect. Just a double-check.
def okChar(c):  
    if ((('A' <= c) and (c <= 'Z')) or (c == ' ')):
        return True
    return False
def applyCodeBook(text, code_book):
    out = []
    for c in text:
        if c == ' ':  # just keep spaces as spaces
            out.append(' ')
        elif okChar(c):  # if not ok, we just skip it.
            out.append(code_book[c])
    s = ""
    return s.join(out)
    
text = "in the land of the blind, the one eyed person is king"
text = text.upper()  # make upper case

encrypted_text = applyCodeBook(text, codebook)
print(f"Original Text: {text}")
print(f"Encrypted Text: {encrypted_text}")

# %%
def invert_code_book(codeBook):
    # Switch the order to make inverse mapping
    inverted_book = {i[1]: i[0] for i in codeBook.items()}  
    return inverted_book


inverted_codebook = invert_code_book(codebook)
decoded_text = applyCodeBook(encrypted_text, inverted_codebook)
print(f"decoded Text: {decoded_text}")

# %%
def randSwapInCodeBook(codeBook):
    codebook_2 = codeBook.clone()
    o = rnd.sample([k for k in codeBook], k=2)
    tmp = codeBook[o[0]]
    codeBook[o[0]] = codeBook[o[1]]
    codeBook[o[1]] = tmp

# %%
num_swaps = 2
for k in range(num_swaps):
    randSwapInCodeBook(inverted_codebook)
decoded_text = applyCodeBook(encrypted_text, inverted_codebook)
print(f"decoded Text with corrupted codebook: \n{decoded_text}")

# %%
def cleanText(text):
    text = text.upper()
    makeSpacesChar = [',', '!', '?', ';', '.', ':']  # characters to spaces
    for i in range(10):
        makeSpacesChar.append(str(i))  # add all of the numbers to the list
    for c in makeSpacesChar:
        text = text.replace(c, ' ')  # Replace each characters with a space
    text = ' '.join(text.split())  # Remove extra spaces 
    # Remove all characters who are not A-Z or Space:
    onlyGoodChar = [c for c in text if ((c <= 'Z') and (c >= 'A')) 
                    or (c == ' ')] 
    text = ''.join(onlyGoodChar)
    return text

# %%
def getCharCountsArray(text):
    char_counts_array = [0 for _ in range(256)]
    for i in range(len(text)-1):
        char_code = ord(text[i])
        char_counts_array[char_code] += 1
    return char_counts_array

def addPairCounts(pair_dict, text): 
    for i in range(len(text)-1):
        c1 = text[i]
        c2 = text[i+1]
        if (okChar(c1) and okChar(c2)):
            key = (c1, c2)
            if key in pair_dict:  # if key=(c1,c2) is already there
                pair_dict[key] += 1  # if it is add 
            else:
                pair_dict[key] = 1

def convertToConditional(pair_dict, text):
    char_counts_array = getCharCountsArray(text);
    for key in pair_dict.keys():
        if key == ('Q', 'U'): 
            print('hi');
        c1 = key[0]
        c1_code = ord(c1)
        pair_dict[key] = pair_dict[key] / char_counts_array[c1_code]

# %%
def get_pair_dict_and_text(directory, fileNames):
    pair_dict = {}  # initialize empty pair dictionary
    all_text = ""
    for fileName in fileNames:  # cycle over the file names
        with open(directory+fileName, 'r') as file:
            text = file.read().replace('\n', '')
        text = cleanText(text)
        all_text += text
        addPairCounts(pair_dict, text)  # add the counts for the current file
    return (pair_dict, all_text)


# %%
import math

def prob_of_text(text, pair_dict):
    pi = 1
    for i in range(0, text.length-2):
        pi *= max(pair_dict.get((text[i],text[i+1])), 2.718**-16)

def log_likelihood(text, pair_dict):
    return math.log(prob_of_text(text, pair_dict))

def pi_ratio(text, codebook_b1, codebook_b2):
    decodebook_b1 = invert_code_book(codebook_b1)
    decodebook_b2 = invert_code_book(codebook_b2)

    decoded_text_b1 = applyCodeBook(text, decodebook_b1)
    decoded_text_b1 = applyCodeBook(text, decodebook_b2)
    return math.e ** (log_likelihood(decoded_text_b1, decoded_text_b1))


# %%
fileNames = ["emma.txt", "journey.txt"]
directory = "text/"
pair_dict, text = get_pair_dict_and_text(directory, fileNames)


print(sorted(pair_dict.items(), key=lambda item:item[1], reverse=True))

convertToConditional(pair_dict, text)
print(sorted(pair_dict.items(), key=lambda item:item[1], reverse=True))

file_tag = open("encoded.txt", "r")  # read in encoded message
encoded_text = file_tag.read()

print(log_likelihood(text, pair_dict, ))
file_tag.close()




# %% [markdown]
# $p(\beta|\alpha) = \frac{p(\alpha \cap \beta)}{p(\beta)}$


