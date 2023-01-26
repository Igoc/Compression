import os
import time

DATA_PATH = './Data/String/data_0.txt'

def LZW(string, verbose=1):
    dictionarySize = 256
    dictionary     = dict((chr(character), character) for character in range(dictionarySize))
    longestString  = ''
    output         = list()
    
    for character in string:
        combinedLongestString = longestString + character
        
        if combinedLongestString in dictionary:
            longestString = combinedLongestString
        else:
            output.append(dictionary[longestString])
            dictionary[combinedLongestString]  = dictionarySize
            dictionarySize                    += 1
            longestString                      = character
    
    if longestString:
        output.append(dictionary[longestString])
    
    if verbose == 1:
        preCompressionSize  = len(string) * 8
        postCompressionSize = 0
        
        for value in output:
            postCompressionSize += value.bit_length() if value != 0 else 1
        
        print('[INFO] Pre-Compression Size = {} bits'.format(preCompressionSize))
        print('[INFO] Post-Compression Size = {} bits'.format(postCompressionSize))
        print('[INFO] Space Saving = {}%'.format(100 - postCompressionSize / preCompressionSize * 100))
    
    return output

if __name__ == '__main__':
    string = ''
    
    if os.path.isfile(DATA_PATH) == False:
        print('[ERROR] Data file dosen\'t exist')
        exit()
    
    with open(DATA_PATH, 'r') as file:
        string = file.read()
    
    startTime = time.process_time()
    output    = LZW(string)
    endTime   = time.process_time()
    
    print('[INFO] Elapsed Time = {} seconds'.format(endTime - startTime))