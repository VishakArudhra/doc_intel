import os
class register_words:

        def __init__(self, input_words):

            self.input_words = input_words
            self.list_assert = False

            try: 
                assert isinstance(self.input_words, list)
                try:
                    text_bool  = all([isinstance(x,str) for x in self.input_words])
                    assert text_bool == True
                except:
                    print('please pass in a list of strings')
                    self.list_assert = True
                    return
            except:
                print('please pass in a list')
                self.list_assert = True
                return

            self.input_words = [x.lower() + '\n' for x in self.input_words]

        #this function deletes words from the list
        def Delete(self):
                '''
                input: list of words to add
                output : input words deleted from vocabulary
                '''
                try: 
                    assert self.list_assert == False
                except:
                    print('check your input')
                    return

                try:
                    #check the presence of the input word(s) in the file                    
                    fin =  open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words.txt'), 'r+')
                    words = fin.readlines()
                    exist_bool = [x in words for x in self.input_words]

                    if all(exist_bool) == False:
                        print("word(s) don't exist!")
                        return
                    else:
                        #only the word(s) which exist in the file. 
                        words = [x for x in words if x not in self.input_words]
                        
                        #'w' to freshly write a new list of words.
                        fout = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words.txt'), 'w')      
                        fout.writelines(words)
                        print('word(s) deleted!')
                finally:
                    fin.close()
                    try:
                        fout.close()                               
                    except:
                        return

                return 


        #this function adds words to the list
        def Add(self):

            '''
            input: list of words to add
            output : input words added to vocabulary
            '''
            try: 
                    assert self.list_assert == False
            except:
                    print('check your input')
                    return

            try: 
                fin =  open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words.txt'), 'r+') #file opened to read words. 
                words = fin.readlines()
                fout = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words.txt'), 'a+') #file opened to append word(s). 
                
                #word presence check through boolean list.
                exist_bool = [x in words for x in self.input_words]
                self.input_words = [x for x,y in zip(self.input_words, exist_bool) if y != True]

                if self.input_words != []:                                                               #incase the 'to add' word list is not empty. 
                    fout.writelines(self.input_words)
                    print('new word(s) have been added!')       
                else:                                                                                    #otherwise
                    print('word(s) already exist!')
            finally:
                fin.close()
                fout.close()
            return

if __name__ == '__main__':
    
    register_words(['implementation']).Add()
    register_words(['implementation']).Delete()