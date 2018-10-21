#!/usr/bin/env python3

# This is a proof of concept code computing the mingzhi or the main stack for
# any valid Tibetan syllable. It uses the data and algorithm described
# in this repository.
#
# The main limitation is the completely unknown behavior (including crashes) fo
# a non-valid Tibetan syllable.
#
# Copyright (C) 2017 Elie Roux <elie.roux@telecom-bretagne.eu>
# Provided under the Creative Commons CC0 license
# http://creativecommons.org/publicdomain/zero/1.0/legalcode



import re

subjoined_to_letter = {
	'\u0F90': 'ཀ',
	'\u0F92': 'ག',
	'\u0F94': 'ང',
	'\u0F97': 'ཇ',
	'\u0F99': 'ཉ',
	'\u0F9F': 'ཏ',
	'\u0FA1': 'ད',
	'\u0FA3': 'ན',
	'\u0FA6': 'བ',
	'\u0FA8': 'མ',
	'\u0FA9': 'ཙ',
	'\u0FAB': 'ཛ',
	'\u0F95': 'ཅ',
	'\u0FA4': 'པ',
	'\u0FB7': 'ཧ'
}

def get_mingzhi(syl):
	mainstack = get_main_stack(syl)
	if len(mainstack) < 2:
		return mainstack
	if mainstack[1] == '\u0FAD' or mainstack[1] == '\u0FB1' or mainstack[1] == '\u0FB2' or mainstack[1] == '\u0FB3':
		return mainstack[0]
	if mainstack[0] == 'ར' or mainstack[0] == 'ས' or mainstack[0] == 'ལ':
		return subjoined_to_letter[mainstack[1]]
	return mainstack[0]



def can_be_prefix_of_naked(prefix, main):
	if prefix == 'ད':
		return main in ['ཀ', 'ག', 'ང', 'པ', 'བ', 'མ']
	if prefix == 'བ':
		return main in ['ཀ', 'ག', 'ཅ', 'ཏ', 'ད', 'ཙ', 'ཞ', 'ཟ', 'ཤ', 'ས']
	if prefix == 'མ':
		return main in ['ཁ', 'ག', 'ང', 'ཆ', 'ཇ', 'ཉ', 'ཐ', 'ད', 'ན', 'ཚ', 'ཛ']
	if prefix == 'འ':
		return main in ['ཁ', 'ག', 'ཆ', 'ཇ', 'ཐ', 'ད', 'ཕ', 'བ', 'ཚ', 'ཛ']
	if prefix == 'ག':
		return main in ['ཅ', 'ཉ', 'ཏ', 'ད', 'ན', 'ཙ', 'ཞ', 'ཟ', 'ཡ', 'ཤ', 'ས']
	return False

ambiguous_to_main = {
	'མངས': 'མ',
	'འབས': 'བ',
	'མགས': 'མ',
	'བགས': 'བ',
	'འགས': 'ག',
	'དབས': 'བ',
	'དགས': 'ག',
	'དངས': 'ད',
	'དམས': 'མ'
}

def get_main_stack(syl):
	# rule 1: if the syllable contains a subscript, superscript or wasur then the main stack is what contains it
	m = re.search("[\u0F40-\u0F6C][\u0F90-\u0FBC]+", syl)
	if (m is not None):
		return m.group(0)
	# rule 2: if a letter other than འ carries a vowel then it is the main stack
	m = re.search("([\u0F40-\u0F5F\u0F61-\u0F6C])[\u0F71-\u0F81]", syl)
	if (m is not None):
		return m.group(1)
	# rule 3: if a vowel is carried by འ and འ is the first letter then འ is the main stack
	m = re.search("\u0F60[\u0F71-\u0F81]", syl)
	if (m is not None and m.span()[0] == 0):
		return "\u0F60"
	# rule 4: if a vowel accent is carried by an འ which is not the first letter, the main stack is before the first འ with a vowel
	elif (m is not None):
		return syl[m.span()[0]-1]
	# rule 5: if the syllable has three or four letters and ends with འང or འམ, then the main stack is right before འང or འམ
	syllen = len(syl)
	if syllen > 2 and (syl.endswith('འང') or syl.endswith('འམ')):
		return syl[-3]
	# rule 6: if the syllable is composed of only one letter this letter is the main stack
	if syllen == 1:
		return syl
	# rule 7: if the syllable contains two letters, then the first is the main stack
	if syllen == 2:
		return syl[0]
	# rule 8: if the syllable contains four letters, the main stack is the second letter
	if syllen == 4:
		return syl[1]
	# rule 9: if the final letter is not ས, then the main stack is the second letter
	if not syl[2] == 'ས':
		return syl[1]
	# rule 10: if the first letter cannot be a prefix to the second letter when it has no superscribed nor subscribedy, then the main stack is the first letter
	if not can_be_prefix_of_naked(syl[0], syl[1]):
		return syl[0]
	# rule 11:  if ས cannot be second suffix after the second letter if it was a first suffix (meaning the second letter is not ག, ང, བ nor མ), then the main stack is the second letter
	if not syl[1] in ['ག', 'ང', 'བ', 'མ']:
		return syl[1]
	else:
		return ambiguous_to_main[syl]

print(get_main_stack('དབྱངས') == 'བྱ')
print(get_main_stack('གཞི') == 'ཞ')
print(get_main_stack('འོད') == 'འ')
print(get_main_stack('མའིའོ') == 'མ')
print(get_main_stack('མའིའམ') == 'མ')
print(get_main_stack('བའམ') == 'བ')
print(get_main_stack('བ') == 'བ')
print(get_main_stack('བར') == 'བ')
print(get_main_stack('བཟབས') == 'ཟ')
print(get_main_stack('བཟའ') == 'ཟ')
print(get_main_stack('ཐགས') == 'ཐ')
print(get_main_stack('གནས') == 'ན')
print(get_main_stack('མགས') == 'མ')
print(get_mingzhi('རླ') == 'ར')
print(get_mingzhi('སྦྱ') == 'བ')
print(get_mingzhi('རྙ') == 'ཉ')
print(get_mingzhi('ལྔ') == 'ང')
print(get_mingzhi('སྲ') == 'ས')
print(get_mingzhi('གླ') == 'ག')
print(get_mingzhi('རྒྱ') == 'ག')
print(get_mingzhi('ར\u0FAD') == 'ར')
