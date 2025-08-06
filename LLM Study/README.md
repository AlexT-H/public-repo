
# LLM Study
### *Language Generation*

-----

## A. Overview
This program takes an input file and generates an output file with text based on the given data.  
Customizations that effect character randomization are prompted let the user manipulate the output. 

*This is a proof of concept design that could scale with increased resources + additional refinements.* 

---

## B. Program Instructions 
```
1. Run main.py with preprocess.py in the same folder
2. Enter chosen n value
    - 2a. (n is the number of character sequences studied for generation)
3. Enter input file with text to generate from
4. Enter desired output document name
    - 4a. (or leave blank for default naming)
5. Enter amount of characters desired in outcome document
6. Enter randomization seed for generation
    - 6a. (or leave blank for random seed to be applied)
7. Observe outcome document in the folder running main.py
```

---

## C. Brief Analysis 
```
- With the lowest possible n scores, the output is illegible as it does not formulate words properly.
- At approximately n = 5, words are visible but not conceptually fluid.
- With 10 and 20 n values respectively, the output becomes more understandable, but still lacks full congruency.
- At approximately n = 30, this model reaches its current limits. The output starts to become overfit and simply replicates sections of the input text.
```
**Outcome:** *Words and sentences are able to be generated with varying degrees of sensibility  
and are heavily dependent on the selected n value and input text.*

---

## D. Possible Improvements

**To further enhance this generation model, more finite grammar abidance and contextualization tools can be deployed.**  

*While the current version does estimate these concepts by merit of it word proximity based design, implementing these specific  
technics could help  assure better, more accurate syntax for the resulting output.*

#### Possible grammatical filters could include:
```
- Noun and Verb Agreement (checking/correcting)
- Sentence Structure (checking/correcting)
- Word Gendering (checking/correcting)
```

#### Possible Contextualization methods could include:
```
- Synonym Considering (changing words with synonyms for more differentiation)
- Noun/Verb Recognition (for keeping a 'train of thought' within the program for greater sensibility) 
```


