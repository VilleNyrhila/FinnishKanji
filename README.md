
# Finnish Kanji
Or _"Sinographs for Finnish"_

This is a project to construct a hypothetical but authoritative set of borrowed Finnish *pronunciations* for Chinese characters.
This is intended as a Finnish counterpart to traditional Japanese on'yomi pronunciations of kanji, 
the pronunciations of Korean hanja, or the Vietnamese Han Nom.  
  
The idea and essence of this project could be crystallized in the question: _"What if Finnish had kanji?"_

The theory under which these borrowings are constructed is described in a PDF document in the folder docs/theory/, 
in a file called _"Suomalaiset kanjit.pdf"_. The document is in Finnish. 
It is thoroughly researched and richly sourced in historical phonetics of both Finnish and Chinese circa 500 AD and 700 AD.

To generate the Finnish reading of Chinese characters, run **main.py**. The pronunciations are compiled into **product/FinnicKanji.yaml**.
So long as the pronunciations exist, it is possible to try them out using **ReadingGenerator.py**. 
It takes as its input files from **ReaderFiles/Input**.
The products of the ReadingGenerator are output to **ReaderFiles/Output**, into files with corresponding names. 

There are many sub-projects within this project, many of which are underdeveloped. 
The principal functionality is the generation of Finnish readings for Chinese characters 
and the application of those pronunciations to test files in ReaderFiles/Input/.  
 
### Format for the ReadingGenerator input files
The ReadingGenerator takes input files in a very simple plaintext format. 
The format is admittedly rather ad hoc, but convenient enough.
    
The ReadingGenerator takes each individual line in an input file, 
and outputs Middle Chinese, North Finnic, and Finnish readings for the 
Chinese characters on that line to a corresponding line in the output file. 
  
'#' as the first character in a line designates the line as a comment 
and will not be appended to the output file.
However, if '#' comes after a character entry, 
the comment will be appended to the corresponding line in the output file.  
  
';' as the first character of a line designates it as a header. 
This is useful for delineating vocabulary and phrases by theme.

Other than these, there are no special characters. 
ReadingGenerator is intended only for demonstrating the aforementioned 
readings of Chinese characters. 
 
 
### Questions and clarifications
#### Why was this made?  
To break into personal anecdotes briefly, I've always been fascinated by the Chinese writing characters. 
I've always admired their ability to capture complicated ideas into just a few syllables. 
I wanted for the Finnish language to also have something like it.

#### What this is not?   
Strictly speaking, **this project is not a dictionary.** 
Although there are plans in place to include a dictionary of the meanings of Chinese characters into Finnish,
this feature is not yet complete. 
This project is most importantly about constructing a set of borrowed _pronunciations_ of Chinese characters for Finnish 
in a way that is plausible _within the frames of the historical phonetics_ of these two languages and 
would be adjacent in terms of the time period to the Japanese on'yomi and Korean pronunciations.  
  
**Neither is this a translation machine.** 
This project does not take text in Chinese or other language and output a translation into Finnish or other language.
That sort of a program is fundamentally different to what is provided here. 
No, what this project and enclosed program does is provide a hypothetical _"traditional Finnish pronunciation"_ 
of Chinese characters in a way that is fundamentally equivalent to the very real traditional borrowed pronunciations 
of Chinese characters in Japanese and Korean.
  
No claim is asserted here about any actual historical contact having taken place between Iron Age Finns 
and their contemporary China.
It is difficult to conceive a set of circumstances,
where Dark Age or Viking Age Finns might have come under a strong enough Chinese cultural influence 
that they would've adopted the Chinese writing system like the Koreans and the Japanese did. 
It would certainly have to be a fantasy scenario.

#### What is the use of this?
To be frank, I myself have no idea. This project was created out of a personal passion for the goal of this project. 
I wanted it to exist, so I created it.  

That said, it is not like some potential use for these could never exist. 
Just because I or most people can't conceive of it, doesn't mean someone out there could not.
That is to say, perhaps someone else out there might find these interesting or useful somehow.

#### Can I use these Finnish pronunciations?
I grant full permission without asking to anyone who wants to use my generated set of Finnish pronunciations
for Chinese characters, whether for commercial or non-commercial uses. I ask not for any royalties.
Please think kindly of me when you use them.

## Notes about licences
The Baxter-Sagart data on the pronunciation of 9 000 characters is **licenced under CC BY 4.0**
It is available at: http://ocbaxtersagart.lsait.lsa.umich.edu

The Songben Guangyun data on 19 000+ characters is distributed under **GPL License**. 
It is available at: http://kanji-database.sourceforge.net/dict/sbgy/index.html?lang=en

Mapping of Kyuujitai characters to Shinjitai is based on material that is copyrighted by Dylan W.H. Sung.
It is available at: https://web.archive.org/web/20081218203648/http://www.sungwh.freeserve.co.uk/hanzi/j-s.htm 

Mapping of Simplified Chinese to Traditional Chinese is from the website SayJack.com.
It is available at: https://www.sayjack.com/chinese/simplified-to-traditional-chinese-conversion-table/

The Unihan database provides its data under the Unicode, Inc. License Agreement.
It is available at: https://www.unicode.org/license.txt 

The manual mapping of Chinese characters is specifically made for this project, and is made with reference to the Unihan database.

The Chinese definitions of Chinese characters are derived from the Unihan database, kDefinitions dataset.

The Japanese definitions of Chinese characters are derived from KANJIDIC2, 
which is released under a Creative Commons Attribution-ShareAlike Licence (V3.0).   
