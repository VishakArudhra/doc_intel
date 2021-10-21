import fitz
from cleantext import clean
import re
import Levenshtein 
import math
import pandas as pd
from .despace import deSpace
import os

'''<-----------------------------------------  Header and Footer Removal Module  ------------------------------------------------------->'''
class head_foot:
    
    def __init__(self, path):
        
        self.doc = fitz.open(path)
        self.text = self.doc[2].get_text("block")
        self.text1 = self.doc[3].get_text("block")
        
    def epsilon(self):
        
        eps = 1.0
        while eps + 1 > 1:
            eps /= 2
        eps *= 2
        return eps
    
    def find_head_foot(self):
        
        
        lev_mat = []
        eps = self.epsilon()
        
        for i in self.text.split('\n'):
            for j in self.text1.split('\n'):
                lev_mat.append([i, j, Levenshtein.distance(i,j), (Levenshtein.distance(i,j)+eps)/(len(i)+len(j)+eps)])
                
        lev_dat = pd.DataFrame(lev_mat, columns = 'text text1 lev_dist lev_dist_norm'.split())
        
        potential_head_foot = lev_dat.sort_values(by = ['lev_dist_norm'],ascending = True ).head(8)
        
        pot_hf_list = list(potential_head_foot['text']) +  list(potential_head_foot['text1'])
        
        head_footer = [i.lstrip().rstrip() for i in pot_hf_list if not i.lstrip().rstrip().isdigit()]
        
        to_pop = []

        foot_head = {c:0 for c in head_footer}
        for page in self.doc:
            for line in head_footer:
        #         print(line)
                if line in page.get_text("text"):
                    foot_head[line] +=1
        for key, val in foot_head.items():
            if val == min(list(foot_head.values())):
                to_pop.append(key)
        for key in to_pop:
            foot_head.pop(key)

        to_remove = list(foot_head.keys())
        
        return to_remove
        
    def remove(self):
        
        texts = []
        for page in self.doc:
            texts.append(page.getText())
        
        texts = ''.join(texts)
        to_remove = self.find_head_foot()
        
        for rep in to_remove:            
            texts = texts.replace(rep,'').lstrip().rstrip()
        
        return texts.replace('\n',' ')

'''<-----------------------------------------------------  Text Clean Up Module  ------------------------------------------------------->'''    
class load_text:
    
    def __init__(self, texts:str, remove_serial: bool, sents_or_word_breaks:bool, lower: bool):
        try:
            dict_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words.txt'), 'rt')
            eng_dic = dict_file.read()
            
        finally:
            dict_file.close()
        
        dictionary = set(eng_dic.lower().split())
        
        self.sents_or_word_breaks = sents_or_word_breaks
        
        self.remov_serial = remove_serial
        
        self.lower = lower
        
        if self.lower == None:
            self.lower = True
         
        
        self.texts = [clean(text,
                    fix_unicode=True,               # fix various unicode errors
                    to_ascii=True,                  # transliterate to closest ASCII representation
                    lower=self.lower,               # lowercase text
                    no_line_breaks=True,           # fully strip line breaks as opposed to only normalizing them
                    no_urls=True,                  # replace all URLs with a special token
                    no_emails=True,                # replace all email addresses with a special token
                    no_phone_numbers=True,         # replace all phone numbers with a special token
                    no_numbers=False,               # replace all numbers with a special token
                    no_digits=False,                # replace all digits with a special token
                    no_currency_symbols=True,      # replace all currency symbols with a special token
                    no_punct=False,                 # remove punctuations
                    replace_with_punct="",          # instead of removing punctuations you may replace them
                    replace_with_url="",
                    replace_with_email="",
                    replace_with_phone_number="",
                    replace_with_number="",
                    replace_with_digit="",
                    replace_with_currency_symbol="",
                    lang="en"                       # set to 'de' for German special handling
                ) for text in texts.split()]
        self.texts = ' '.join(self.texts)
        
        hif  = '-'.join([i.lstrip().rstrip() for i in self.texts.split('-')])
        words = hif.split()

        for idx,word in enumerate(words):
            if (words[idx].find('-') > 0):
        #         print(word.split('-'))
                dic_bool = sum([(piece.lstrip().rstrip().lower() in dictionary) for piece in word.split('-')])
                num_bool = any([piece.lstrip().rstrip().isdigit() for piece in word.split('-')])
                
                if dic_bool > 1:
                    words[idx] = words[idx].replace('-',' ')
                if num_bool:
                    words[idx]  = words[idx].replace('-',' - ')              
                else:
                    words[idx] = words[idx].replace('-','')

        self.texts =  ' '.join(words)
        
    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False 

    def num_dot_correct(self, document):

        dot_split = document.split('.')

        for idx, line in enumerate(dot_split):
            if idx == (len(dot_split) - 1):
                print('(dot digit) - last line reached!\ncleansing done. ')
                break
            else:
                cond_1 = line[-1].isdigit()
                cond_2 = dot_split[idx + 1][1].isdigit()

                if ((cond_1)&(cond_2)):
                    dot_split[idx + 1] = dot_split[idx + 1].replace(' ','',1)

        return '.'.join(dot_split)
        
    def remove_serial(self, texts): # to remove a series of numbers separated by spaces
        
        text_split = texts.split(' ')
        
        for k,ele in enumerate(text_split):
        #     print(k)
            int_bool_list =  [(i.isdigit() or self.isfloat(i)) for i in [text_split[j] for j in range(k,k+3) if ((k+3) < len(text_split))]]
            
            #the below boolean mask is so that that number of figures with percentages are removed. 
            
            int_junk_list = [bool(i.find('%')>0) for i in [text_split[j] for j in range(k,k+3) if ((k+3) < len(text_split))]]
            try: 
                if (sum(int_bool_list)/len(int_bool_list))>0.67:
        #             print([text_split[j] for j in range(k,k+16)])
                  if (k+10)<len(text_split):
                    for j in range(k,k+10):
                        if (text_split[j].isdigit() or self.isfloat(text_split[j])):
                            text_split[j] = ''
            except ZeroDivisionError:
                pass


            try: 
                if (sum(int_junk_list)/len(int_junk_list))>0.67:
                       if (k+10)<len(text_split):
                        for j in range(k,k+10):
                            if bool(text_split[j].find('%')>0):
                                     text_split[j] = ''
            except ZeroDivisionError:
                pass
            
        texts = repr(' '.join(text_split))
            
        return texts.replace('|','').replace('\'','').replace('\\','"').replace('"',"'")
    
    def launder(self):
        
        if self.sents_or_word_breaks == None:
            self.sents_or_word_breaks = False 

        if self.sents_or_word_breaks:

            for ind, sym in enumerate('* .'.split()):

                if(sym=='.'):       
                    self.texts = '. '.join([piece.rstrip().lstrip() for piece in self.texts.split(sym) if len(piece.split()) > 1])
                else:
                    self.texts = ' '.join([piece.rstrip().lstrip() for piece in self.texts.split(sym) if len(piece.split()) > 1])
        if self.remov_serial:

            self.texts = self.remove_serial(self.texts)
            
        interext = deSpace(self.texts).space_in()
        self.texts = deSpace(interext).space_in()        
        self.texts = ' '.join(self.texts.split())

        return self.num_dot_correct(self.texts)

if __name__ == '__main__':
    
    file_path =  r"C:\Users\Vishak\Downloads\deeplearningbook.pdf"
    texts = head_foot(file_path).remove()
    trues = [True]*3
    texts = load_text(texts, *trues).launder()
    saved_txt = open('text_extract.txt','w')
    saved_txt.write(texts)
    saved_txt.close()

    




    
          

                
            


        
        




    
    
