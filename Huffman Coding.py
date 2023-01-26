import os
import queue
import time

DATA_PATH = './Data/String/data_0.txt'

def HuffmanCoding(string, verbose=1):
    def CountCharacterFrequency(string):
        characterFrequency = dict()
        
        for character in range(256):
            frequency = string.count(chr(character))
            
            if frequency > 0:
                characterFrequency[chr(character)] = (frequency,)
        
        return characterFrequency
    
    def CreateHuffmanTree(characterFrequency):
        minHeap = queue.PriorityQueue()
        
        for value in characterFrequency.values():
            minHeap.put(value)
        
        while minHeap.qsize() > 1:
            node = [minHeap.get(), minHeap.get()]
            minHeap.put((node[0][0] + node[1][0], node))
        
        return minHeap.get()
    
    def ComputeBinaryCodes(node, code='', binaryCodes=dict()):
        if len(node[1][0]) > 1 and type(node[1][0][1]) == list:
            ComputeBinaryCodes(node[1][0], code + '0', binaryCodes)
        else:
            binaryCodes[node[1][0][0]] = code + '0'
        
        if len(node[1][1]) > 1 and type(node[1][1][1]) == list:
            ComputeBinaryCodes(node[1][1], code + '1', binaryCodes)
        else:
            binaryCodes[node[1][1][0]] = code + '1'
        
        return binaryCodes
    
    characterFrequency   = CountCharacterFrequency(string)
    huffmanTree          = CreateHuffmanTree(characterFrequency)
    binaryCodes          = ComputeBinaryCodes(huffmanTree)
    characterBinaryCodes = characterFrequency.copy()
    
    for key in characterFrequency.keys():
        characterFrequency[key]   = characterFrequency[key][0]
        characterBinaryCodes[key] = int(binaryCodes[characterFrequency[key]], 2)
    
    output = [characterBinaryCodes[character] for character in string]
    
    if verbose == 1:
        preCompressionSize  = len(string) * 8
        postCompressionSize = 0
        
        for value in output:
            postCompressionSize += value.bit_length() if value != 0 else 1
        
        print('[INFO] Pre-Compression Size = {} bits'.format(preCompressionSize))
        print('[INFO] Post-Compression Size = {} bits'.format(postCompressionSize))
        print('[INFO] Space Saving = {}%'.format(100 - postCompressionSize / preCompressionSize * 100))
    
    return characterFrequency, characterBinaryCodes, output

if __name__ == '__main__':
    string = ''
    
    if os.path.isfile(DATA_PATH) == False:
        print('[ERROR] Data file dosen\'t exist')
        exit()
    
    with open(DATA_PATH, 'r') as file:
        string = file.read()
    
    startTime                                        = time.process_time()
    characterFrequency, characterBinaryCodes, output = HuffmanCoding(string)
    endTime                                          = time.process_time()
    
    print('[INFO] Elapsed Time = {} seconds'.format(endTime - startTime))