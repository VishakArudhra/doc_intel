# doc_intel

`pip install doc-intel`


###### This package is subject to several potential fixes and until then any benefits derived by using this is very much intended. 

### doc_intel is your solution to a largely cleansed and intact text extract from a PDF. 


###### change 0.0.1 (8 / 23 / 2021) :
   * Line breaks lead to breakage of full words into smaller potentially non dictionary words and changes have been made to fix that. 
   * A dictionary has been used to identify how to reconstruct the broken words. 
###### change 0.0.2 (8 / 28 / 2021) :                         
   * Updated dictionary, maybe inverse document frequency will later be used instead to fix the line breaks. 
   * Inverse document frequency has been used to precisely split and reconstruct stitched or meaninglessly spaced words. 
###### change 0.0.3 (9 / 10 / 2021) :
   * added and removed words in word.txt, fixed dot spacing and conserved number word detachment post processing" 

###### change 0.0.4 (9 / 14 / 2021) :
   * added and removed words in word.txt, maintained the positions of apostrophes.
 
### Major Version Update 1.0.0 (10 / 19 / 2021) :
   * A new module has been added to serve requirements of deletion and addition of words in the words text file. 
   * Usage demonstration can be found under the feature instruction section. 

###### change 1.0.1 (10 / 21 / 2021) :
   * fixed issue by which decimal numbers were spaced from the decimal point.
   * closed the words text file in the main code block to prevent unclosed file issues. 


## Feature instruction:

#### REMOVE THE HEADER AND FOOTER TERMS FORM YOUR DOCUMENT: 

```
from doc_intel import text_laundry

file_path = / your_path/ your_file.pdf

texts = text_laundry.head_foot(file_path).remove()
```

#### SCRUB OFF TEXTUAL NOISE FROM YOUR TEXTS:

###### Arguments : 

* **serial numerical noise** [bool]: noise like `(text) + (random numbers, spaced or continous)` will be removed. 

* **sentences or words interrupted with special characters** [bool] : All cohesive words and sentences interruptions like  `co -hesive` or `sol **utions` should be removed.
 
* **lower case** [bool] : toggle between bool values for lower or upper casing. 

* `s u b s t r i n g s w h i c h a r e a t t a c h e d w i l l b e s e p a r a t e d` --> ``substrings which are attached will be separated`` (based on the fequency of the constituent words in the document). 

```
text_object = text_laundry.load_text([input str], remove_serial, sents_or_word_breaks, lower)
cleaned_text = text_object.launder()
```

#### **ADD** AND **DELETE** WORDS FROM IN-BUILT DICTIONARY:

* PDF documents are not purposely written to suite document extraction and therefore, a lot of discontinued words in the documents end up broken with ordinary text extraction. 
* doc-intel's in-built dictionary support identification of many 1000s of words which is now **editable**. Add and remove words as you require for your smooth text extraction. 
* `do-cument` --> `document`

```
from doc_intel import manage_diction

word_list = " your list of words to either add or delete "
manage_diction.register_words(word_list).Add()  #or
manage_diction.register_words(word_list).Delete()
```


###### **Authored & Maintained By** : Vishak Arudhra
