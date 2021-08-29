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


## Feature instruction:

* remove header and footer terms in your document : 

```
from doc_intel import text_laundry

file_path = / your_path/ your_file.pdf

texts = text_laundry.head_foot(file_path).remove()
```

* scrub off textual noise from your texts:

###### Arguements : 

* **serial numerical noise** [bool]: noise like `some textual piece but then 101 234 384 927 so all these numbers will be removed if needed` will be removed. 

* **sentences or words interrupted with special characters** [bool] : All cohesive words and sentences interruptions like  `co -hesive` or `sol **utions` should be removed.
 
* **lower case** [bool] : toggle between bool values for lower or upper casing. 

* `s u b s t r i n g s w h i c h a r e a t t a c h e d w i l l b e s e p a r a t e d` will be separated to ``substrings which are attached will be separated`` based on the fequency of the constituent words in the document. 

```
text_object = text_laundry.load_text([input str], remove_serial, sents_or_word_breaks, lower)
cleaned_text = text_object.launder()
```


