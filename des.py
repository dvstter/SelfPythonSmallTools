#!/bin/python

#
#	File Created By:p1usj4de
#	File Date:2015.4.12
#	All rights reserved.
#

########################################################
#  Constants for cipher engineer
#######################################################

S_TABLE = [[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7], [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
	 [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0], [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],

	[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10], [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
	 [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15], [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],

	[[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8], [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
	[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7], [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],

	[[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15], [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
	[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4], [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],

	[[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9], [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
	[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14], [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],

	[[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11], [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
	[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6], [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],

	[[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1], [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
	[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2], [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],

	[[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7], [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
	[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8], [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]
# 0 table is IP_TABLE and 1 table is the reversed
IP_TABLE = [[57,49,41,33,25,17,9,1,
	 59,51,43,35,27,19,11,3,
	 61,53,45,37,29,21,13,5,
	 63,55,47,39,31,23,15,7,
	 56,48,40,32,24,16,8,0,
	 58,50,42,34,26,18,10,2,
	 60,52,44,36,28,20,12,4,
	 62,54,46,38,30,22,14,6]
	,[39,7,47,15,55,23,63,31,
	   38,6,46,14,54,22,62,30,
	   37,5,45,13,53,21,61,29,
	   36,4,44,12,52,20,60,28,
	   35,3,43,11,51,19,59,27,
	   34,2,42,10,50,18,58,26,
	   33,1,41,9,49,17,57,25,
	   32,0,40,8,48,16,56,24]]

KEY_ROTATION = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

PC_1 =  [56,48,40,32,24,16,8,
     0,57,49,41,33,25,17,
     9,1,58,50,42,34,26,
     18,10,2,59,51,43,35,
     62,54,46,38,30,22,14,
     6,61,53,45,37,29,21,
     13,5,60,52,44,36,28,
     20,12,4,27,19,11,3]
PC_2 = [13,16,10,23,0,4,
	1,27,14,5,20,9,
	22,18,11,3,25,7,
	15,6,26,19,12,1,
	40,51,30,36,46,54,
	29,39,50,44,32,47,
	43,48,38,55,33,52,
	45,41,49,35,28,31]

PERMUTATION_TABLE = [15,6,19,20,28,11,27,16,
		0,14,22,25,4,17,30,9,
		1,7,23,13,31,26,2,8,
		18,12,29,5,21,10,3,24]

######################################################
#  Auxilary Funcions
#####################################################

# delete one character from string
def delete(string, pos):
	return string[:pos] + string[pos+1:]
# circle rotate a string
def rotate(string, length):
	return string[length:] + string[:length]
# xor function
def xor(string1, string2):
	result = ''
	if len(string1) != len(string2):
		raise TypeError('xor need two string which has same length.')
	for x in range(len(string1)):
		if string1[x] != string2[x]:
			result += '1'
		else:
			result += '0'
	return result
#####################################################
#  Cipher Main Class
####################################################

class AES:
	def __init__(self, cipherKey):
		# get 56 bit cipherKey
		self.cipherKey = cipherKey
		if len(cipherKey)!=64:
			raise TypeError('You must input a 64-bit binary string as cipher key.')
		temp = ''
		for x in PC_1:
			temp += cipherKey[x]
		self.cKey  = temp[:28]
		self.dKey = temp[28:]
		self.circle = 0 # decide the circle number

	def Reset(self):
		# reset the circle number ready for decipher
		self.__init__(self.cipherKey)

	def GetKey(self):
		self.cKey = rotate(self.cKey, KEY_ROTATION[self.circle])
		self.dKey = rotate(self.dKey, KEY_ROTATION[self.circle])
		self.circle += 1
		tempResult = self.cKey + self.dKey
		resultKey = ''
		for x in PC_2:
			resultKey += tempResult[x]
		return resultKey

	def IPDisplace(self, bitStr64, reversed=0):
		result = ""
		for index in IP_TABLE[reversed]:
			result += bitStr64[index]
		return result

	def ExpansionTable(self, bitStr32):
		result = bitStr32[31] + bitStr32[0:5]
		for index in range(1, 7):
			result += bitStr32[index*4-1:index*4+5]
		result += bitStr32[27:] + bitStr32[0]
		return result

	def SubstitutionBox(self, bitStr48):
		result = ""
		for index in range(8):
			row = int(bitStr48[index*6] + bitStr48[index*6+5], 2)
			column = int(bitStr48[index*6+1:index*6+5], 2)
			res = bin(S_TABLE[index][row][column])[2:]
			result += '0'*(4-len(res)) + res
		return result
	def PermutationBox(self, bitStr32):
		result = ""
		for eachPosition in PERMUTATION_TABLE:
			result += bitStr32[eachPosition]
		return result

	# we will do this 16 times
	def CircleFunction(self, beforeThisCircleData, subKey):
		# get left and right data
		left = beforeThisCircleData[:32]
		right = beforeThisCircleData[32:]
		# E table 4->6
		right = self.ExpansionTable(right)
		# execute xor operation
		right = xor(right, subKey)
		# S box 6->4
		right = self.SubstitutionBox(right)
		# Permutation
		right = self.PermutationBox(right)
		# another xor operation and reset left and right string
		right = xor(left, right)
		left = beforeThisCircleData[:32] # left == right
		return left + right

	def Decipher(self, cipherText):
		self.Reset()
		# IP Transformation
		if len(cipherText) != 8:
			raise TypeError('You must feed me 8 bytes to decipher.')
		# change text into 'bit string' which length is 64
		cipherTextBitStr64 = self._trans(cipherText)
		# IP Displace
		circleData = self.IPDisplace(cipherTextBitStr64)
		# restore all the subkey, get ready for the circle function
		# get all the subkey
		cipherKeyList = []
		for x in range(16):
			cipherKeyList.append(self.GetKey())
		# 16 times circle function
		for x in reversed(range(16)):
			circleData = self.CircleFunction(circleData, cipherKeyList[x])
		# reversed IP Displace to get plainText
		plainText = self.IPDisplace(circleData, 1)
		return self._retrans(plainText)

	def Cipher(self, plainText):
		self.Reset()
		if len(plainText) != 8: # will process 8bytes (64bit) character each time
			raise TypeError('You must feed me 8 bytes data to cipher.')
		# change text into 'bit string' which length is 64
		plainTextBitStr64 = self._trans(plainText)
		# IP Displace
		circleData = self.IPDisplace(plainTextBitStr64)
		# 16 times circle function
		for x in range(16):
			circleData = self.CircleFunction(circleData, self.GetKey())
		# exchange left and right 32 bits
		afterExchangeData = circleData[32:] + circleData[:32]
		# reversed IP Displace to get cipherText
		cipherText = self.IPDisplace(afterExchangeData, 1)
		return self._retrans(cipherText)

	# private functions should only called by the main function
	def _trans(self, text):
		result = ''
		for each in text:
			x = bin(ord(each))[2:]
			x = '0' * (8-len(x)) + x
			result += x
		return result
	def _retrans(self, bitText):
		resultStr = ''
		for index in range(8):
			resultStr += chr(int(bitText[index*8:index*8+8],2))
		return resultStr
			
if __name__ == '__main__':
	a = AES('0100101000100100010010100010001000100010111001101001000111110101')
	text = a.Cipher('this is ')
	print text
	print a.Decipher(text)
