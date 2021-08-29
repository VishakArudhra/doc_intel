from math import log
class deSpace:
    
    def __init__(self, texts):
        
        self.texts = texts
        
        # below derivations are entirely for cost based space inference using zipf's law cost allocation for every document word. 
        
        self.word_count = {c.lower() : self.texts.count(c) for c in self.texts.split()} # frequency of every word in the doc. 
        self.ranked_tuple = sorted(self.word_count.items(), key = lambda x : x[1], reverse = True) # sort by freq
        self.rankd = [item[0] for item in self.ranked_tuple] #just the words from the sorted dictionary
        self.words = [item[0] for item in self.word_count.items()]
        self.wordcost = dict((k, log((i+1)*log(len(self.rankd)))) for i,k in enumerate(self.rankd))
        self.maxlen = max(len(x) for x in self.rankd)
        
        # below list is for defining the class of characters to test for repeated singular occurence. 
        
        self.special_range = [chr(i) for i in range(32,48)] + [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 129)] + [chr(i) for i in range(58,65)]

    def infer_spaces(self,s):
        """Uses dynamic programming to infer the location of spaces in a string
        without spaces."""

        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i-self.maxlen):i]))
            return min((c + self.wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

        # Build the cost array.
        cost = [0]
        for i in range(1,len(s)+1):
            c,k = best_match(i)
            cost.append(c)

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i>0:
            c,k = best_match(i)
            assert c == cost[i]
            out.append(s[i-k:i])
            i -= k

        return " ".join(reversed(out))  


    def residue_space_fix(self, new_text):
        count = 0
        singles = []
        split = new_text.split()
        count_flag = False
        
        for idx, piece in enumerate(split):
            if ((len(piece) == 1)&(piece.isalpha()|(piece in self.special_range))):
                count+=1
                if count > 1:
                    count_flag = True
                    singles.append(idx)
            else:
                if count_flag == True:
                    count_flag = False
                    singles = [singles[0] - 1] + singles
                    split[singles[0]:singles[-1]+1] = ''
                    singles = []
                    count = 0
                elif count_flag == False:
                    count = 0
                    singles = []
                    continue
        return ' '.join(split)

    def space_in(self):
            
            split  = self.texts.split()

            count_flag = False
            singles = []
            final_idx = []
            count = 0
            for idx, piece in enumerate(split):
                if ((len(piece) in range(1,4))&(piece.isalpha()|(piece in self.special_range))):
                    count+=1
                    if count > 2:
                        count_flag = True
                        singles.append(idx)
            #             print(''.join([split[i] for i in singles])) # test point
                else:
                    if count_flag == True:
                        count_flag = False
                        singles = [singles[0] - i for i in range(2,0,-1)] + singles
                        intermediate = ''.join([split[i] for i in singles])
    #                     print(intermediate) #probing point
    #                     print(infer_spaces(intermediate.lower()))
    #                     print(residue_space_fix(infer_spaces(intermediate.lower())))
                        intermediate = self.residue_space_fix(self.infer_spaces(intermediate.lower()))
                        split[singles[0]] = intermediate
                        split[singles[1]:singles[-1]+1] = '' # test point 
                        singles = []
                        count = 0
                    else:
                        singles = []
                        count = 0
                        continue
            return ' '.join(split)