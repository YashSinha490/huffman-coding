# we are given a text file and we have to convert the text into binary and then change it into integer so that we can convert it into bytes and store it in a bytes file 
# the letter with the maximum frequency is assigned a lower binary value and the letter with less frequency is assigned a higher bianry value
# the binary codes formed with this process are prefix code, i.e, there are no two codes which will have the same prefix,(no code will be formed by using any other code fully)

# steps:- (COMPRESSION)
#     1. read the contents of the '.txt' file
#     2. we first find the frequency of each letter using hash maps
#     3. using this frequency, we build a min heap, which will contain the element with the least frequency on the top
#     4. using this heap, we will pop out two min nodes and form a tree(sum up their frequencies and make a new node with the frequency as the sum of the two child)
#     5. make that node as the parent of the two child node that were previously made and now push the same node into the heap
#     6. we can include the new node while popping the next time,
#     7. we will keep doing this until only one node is left in the heap that has no name, it will become the root of the tree, and by now, our tree is fully made
#     8. after this, we traverse through the tree and store the binary code for each charecter in a dictionary, now we have a dictionary which has bianry codes for all the charecters
#     9. now after we have the dictionary, we convert our string conataining text into binary form by converting each text into its binary form
#     10. to convert into bytes, the number of binary digits should be multiple of 8, hence we do padding for the generated binary text
#     11. for padding, we find how many digits are left in the binary text for it to become a multple of 8, we fill those spots by adding zeros, becasue as of now, we have the binary in string form
#     12. we keep into account the number of zeros we added to the last, we then add the binary form of the same number (add zeros to the beginning of that binary number so that its length becomes 8) to the beginning of the binary string
#     13. after the padding is done, we split the binary digits into group of 8 and convert then into integer form  and store them in an array so that we can convert them into bytes
#     14. after we have our array ready containing integers, we can directly convert them into bytes by using bytes function
#     15. store these bytes into a new '.bin' file

# steps:-  (DECOMPRESSION)
#     1. open the '.bin' file, take one byte from it at a time
#     2. convert that byte into integer value and then to its binary form, do this until all the bytes are finished
#     3. now remove the padding from the binary string
#     4. now using the reverse_dictionary, convert the binary codes into their respective charecters
#     5. write this to a new file


import heapq
import os
class BTnode(object):
    def __init__(self, val, freq):
        self.val = val
        self.freq = freq
        self.left = None
        self.right = None
     
    # while building heap, it is internally using '<' and '>' operator, so we use this incase we want to compare two nodes based on their frequencies  
    def __lt__(self, other): #custom overloaded operator, it will be invoked when we use '<' operator with the object(node) we make of this class
        if self.freq < other.freq: #self is the current node, other is the node from which we are comparing
            return True                              # curr_node < other_node (if this ever used, the two nodes will be compared based on their frequencies)
        return False
        
    def __ge__(self, other): #custom overloaded operator, it will be invoked when we use '>=' operator with the object(node) we make of this class
        if self.freq >= other.freq:
            return True
        return False
        
class HuffmanCoding(object):
    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__Binarycode_dic = dict()
        self.__reverseBinarycode_dic = dict()
        
    def __get_frequency(self, text): #get the frequency of all the charecters present
        freq_dic = dict()
        for char in text:
            freq_dic[char] = freq_dic.get(char, 0) + 1
        return freq_dic
    
    def __BuildHeap(self, freq_dic): #build a min heap using the dictionary we made previously
        for key in freq_dic:
            nn = BTnode(key, freq_dic[key]) # make newnode of value and frequency
            heapq.heappush(self.__heap, nn) # push it in the heap and the node with the lowest frequency will be on the top, because it is internally using <, > operator and we have made custom overloaded operators to compare two nodes based on their frequencies
        return
        
    def __BuildTree(self): #getting two min nodes at a time from the min heap, we build a tree from the bottom, so that the char which is less used will have more bits, as we go down the tree
        while len(self.__heap) > 1: # do this until we have only one node left and we cannot pop out two min nodes now
            min_node_1 = heapq.heappop(self.__heap)
            min_node_2 = heapq.heappop(self.__heap)
            newfreq = min_node_1.freq + min_node_2.freq # newnode with frequency as the sum of two smnallest ones we got
            nn = BTnode(None, newfreq) # name it as None
            nn.left = min_node_1 # make the previous two nodes as the children of this newnode
            nn.right = min_node_2
            heapq.heappush(self.__heap, nn) # push the newnode back into the heap and it will go to its correct place
        return heapq.heappop(self.__heap) # return the only left node in the heap ((sum of previous two mins and with name None)) as the root of the tree
    
    def __getBinaryCode(self, root, code = '0'): # code is 0 for the root node        
        if root is None: 
            return 
        if root.left is None and root.right is None: # the nodes having the name, i.e the original ones are only present as leaf nodes, non-leaf ones are the sum of two nodes
            self.__Binarycode_dic[root.val] = code # stores the name of the charecter in a charecter along with the binary code, which is formed
            self.__reverseBinarycode_dic[code] = root.val # stores the code as the key and the charecter corresponding to it as value 
        self.__getBinaryCode(root.left, code + '0') # when we go left, we add 0 to the current code, which will be removed if we come back(return) because of recusion
        self.__getBinaryCode(root.right, code + '1') # when we go right, we add 1 to the current code, which will be removed if w come back(return) because of recursion
        
    def __convert_str_to_bin(self, text): # encoding text
        bin_text = ''
        for char in text:
            bin_text += self.__Binarycode_dic[char] #the binary value of all the charecters is in the dictionary
        return bin_text
        
    def __get_padded_text(self, bin_text):
        left_len = 8 - (len(bin_text) % 8) # tells us how short are we of to become a multiple of 8, we add the same number of zeros to the last
        binary_of_the_len = bin(left_len)[2 : ].zfill(8) #convert that "left_len" (no of zeros to bee added to the last) and also add the required number of zeros to the beginning for the length to become 8
        bin_text += ('0' * left_len)
        final_string = binary_of_the_len + bin_text
        return final_string
    
    def __conv_to_int(self, padded_bin_text): # length of padded_bin_text is in multiple of 8
        int_array = []
        for i in range(0, len(padded_bin_text), 8):
            ith_part = int(padded_bin_text[i : i + 8], 2) #convert every group of 8 binary digits into integer
            int_array.append(ith_part) # append them one by one into a new array
        return int_array # conatins the integer converted array
    
    def __conv_to_bytes(self, int_array):
        Bytes = bytes(int_array) # integer array can be converted into bytes by using bytes inbuilt bytes function
        return Bytes
    
    def compress(self): # compress the passed file
        file_name, file_extension = os.path.splitext(self.path) # os.path.splitext is used to split the path name from its extension name
        output_file_path = file_name + '.bin' # add .bin to the name of the file
        with open(self.path, 'r+') as input_file , open(output_file_path, 'wb') as output_file: #open both the files, [(open - opens the file, if no such file, create a file), ('r+' - opens the text file for read and write), ('wb' - opens the binary file for writing bianry stuff, if no such file, create one), ('with' - automatically closes the file, once we are doen with it)]
            text = input_file.read() #  read the file
            text = text.rstrip() # remove the trailing spaces
            freq_dic = self.__get_frequency(text) # it will get a dictionary of frequencies
            self.__BuildHeap(freq_dic) # using that dic, it will make nodes with value and frequency and put it in the heap we made
            root = self.__BuildTree() # next we build a tree using the nodes in the heap, and get the root node
            self.__getBinaryCode(root) # forms bianry code for each charecter and store them in a private dictionary (__Binarycode_dic)
            bin_text = self.__convert_str_to_bin(text) # gets encoded text(binary)
            padded_bin_text = self.__get_padded_text(bin_text) # now the length of our binary text is multiple of 8 and it has the (binary form of the number of zeros added to the last) at its beginning
            int_array = self.__conv_to_int(padded_bin_text) #convert the binary into int so that it can be converted into bytes
            Bytes = self.__conv_to_bytes(int_array) # convert the integer array into bytes
            output_file.write(Bytes) #write the bytes contents into the bianry file, which we created
        print('compressed')
        return output_file_path #returns the path of the '.bin' file we just made, so that we can use it during decompression 
        
    def __removePadding(self, bit_string):
        padded_info = bit_string[ : 8] # padded binary string
        padded_info = int(padded_info, 2) # convert it into int
        bit_string = bit_string[8 : ] # slice the rest of the string
        after_removing = bit_string[ : -padded_info] # remove the padding from the last
        return after_removing # return the string after the padding has been removed
    
    def __convert_to_text(self, binary_string): # return decompressed text
        text = ''
        bin_str = ''
        for bit in binary_string: # iterate through the binary string
            bin_str += bit # keep adding each bit to it
            if bin_str in self.__reverseBinarycode_dic: # if any code is matched, add the corresponding charecter to the text variable
                text += self.__reverseBinarycode_dic[bin_str]
                bin_str = '' # make it empty again for the next charecter 
        return text # return the decompressed text
    
    def decompress(self, file_path): #decompress the compressed file
        file_name, file_extension = os.path.splitext(file_path) #split it into teo part name and extension
        output_file_path = file_name + 'decompressed' + '.txt' #add the extension for output file
        with open(file_path, 'rb') as input_file , open(output_file_path, 'w') as output_file: # [(with - automatically closes the file once the work is done), (rb - read from a bianry file), (w - write to a text file)]
            bit_string = ''
            Byte = input_file.read(1) # read one byte from the file at a time
            while Byte: # while we don't get null
                byte = ord(Byte) # change the byte into its integer value
                bits = bin(byte)[2 : ].rjust(8, '0') #convert the integer value into its binary form and also add required zeros to make it of 8 digit
                bit_string += bits # add it to the bit_string
                Byte = input_file.read(1) # read the next byte
            # length of bit_string is in multiple of 8, where the first 8 digits represent the apdding info (i.e, how much padding is done at the last)
            bin_after_padding_removed = self.__removePadding(bit_string) # padding removed binary string
            decompressed_text = self.__convert_to_text(bin_after_padding_removed) # get the decompressed text
            output_file.write(decompressed_text) # write the contents to the output file
        print("decompressed")
        return
            
input_file_path = 'C:/Users/Yash/Desktop/sample.txt' # input file path
hc = HuffmanCoding(input_file_path) 
output_file_path = hc.compress() #get the path of the compressed file
hc.decompress(output_file_path) # decompresses the compressed file again

