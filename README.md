# Finnish Kanji
Or "Sinograms for Finnish".

This is a project to construct a hypothetical but authoritative set of borrowed Finnish *pronunciations* for Chinese characters.
This is intended as a Finnish counterpart to traditional Japanese on'yomi pronunciations of kanji, 
the pronunciations of Korean hanja, or the Vietnamese Han Nom.

The theory under which these borrowings are constructed is described in a PDF document in the folder docs/theory/, 
in a file called "Suomalaiset kanjit.pdf". The document is in Finnish. 
It is thoroughly researched and richly sourced in historical phonetics of both Finnish and Chinese circa 500 AD and 700 AD. 

There are many sub-projects within this project, many of which are underdeveloped. 
The principal functionality is the generation of Finnish readings for Chinese characters 
and the application of those pronunciations to test files in ReaderFiles/Input/. 
The contents of the test files are output to ReaderFiles/Output, into files with corresponding names. 

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
