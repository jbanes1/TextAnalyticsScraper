
# Text Analytics Comment Scraper

#### This project was created to fulfill three needs, in this order:

1. Easy use, with no coding knowledge, through a text-based GUI & basic error handling.

2. Enable the ability to scrape a vast amount of relevant data sources quickly through the use of a webpage link gatherer.

3. Mass input links into an appropriate Python comment scraping library.


## Features

- Facebook link scraping from a public profile with a /photos/ page
- YouTube link scraping from any page
- TikTok link scraping from any page
- Comment scraping from the above sources
- Automatic YouTube file naming using the video title
- Duplicate YouTube link check using ID of video 
- Error handling (that isn't a link, etc.)
- File already exists check (not for .txt files, only for XLSX files excluding TikTok)



## FAQ

#### How do I use this?

Go to the "Releases" section on the right hand side. Download the most recent release and either recompile the project using "PyInstaller" or run the pre-compiled Windows or Mac release. 

#### Facebook mode says "Unsupported Browser."

Wait a few seconds. Generally this is a warning and not an error.

If the program crashes or does not proceed, you may need to look into further help on why the program isn't working.

#### On Mac, I get “chromedriver cannot be opened" when starting the link scraping.

Click "cancel" and wait a few seconds. The program should proceed as intended. 

If the program crashes or does not proceed, you may need further help.

#### On Mac, I cannot find my .txt or .xlsx files!

1. Go to your applications and open "Terminal."
2. Type "open ." and press [ENTER]

Your files will likely be in this directory.

#### When I start scraping links, I get "StaleElementReferenceException."

This means the page did not finish loading before the [addLinksToList] function was called.

If this happens continuously, try closing some processes on your computer before the link scraping begins. After it starts scrolling, feel free to continue using your computer.

In the case the above "fix" does not work, try adding time.sleep(int) after the driver.get calls. Whatever interger you use as "int" will be the number of seconds until the next steps of the program can begin. This will require the program to be recompiled.

#### The TikTok scraper is broken!

Unfortunately, the API used for this scraper is not open source, so this part of the tool is unlikely to be maintained. However, the link scraper for TikTok should continue working.


## Authors

- [Jonas G. Banes](https://www.linkedin.com/in/jonasbanes)

- [Ignacio Luri, PhD](https://www.linkedin.com/in/iluri/)


## Acknowledgements

#### My professor in Text Analytics for Marketing:
- [Ignacio Luri, PhD](https://www.linkedin.com/in/iluri/)

#### VIPs
- [Alissa Coronna](https://www.linkedin.com/in/acoronna/)
- [Janaki Soni](https://www.linkedin.com/in/janaki-soni/)
- [Anika Vadlamani](https://www.linkedin.com/in/anika-vadlamani-84861b22a/)

#### My teammates in Professor Ignacio's Class:
- [Zurab Mikhelashvili](https://www.linkedin.com/in/zuka-mikhelashvili-34921a22b/) 
- [Santiago Garcia](https://www.linkedin.com/in/santiago-garcia-3a7157250/)

 

#### My classmates in the Fall 2023 class:
- [Amanda Phan](https://www.linkedin.com/in/amandaphan503/)
- [Hailey Mantooth](https://www.linkedin.com/in/hailey-mantooth-8210b01b3/)
- [Evelyn Janeczek](https://www.linkedin.com/in/evelyn-janeczek-a7675426b/)
- [Abigale Dore](https://www.linkedin.com/in/abigail-dore-a96bb8222/)
- [Jack Loizza](https://www.linkedin.com/in/jack-loizzo-469254292/)
- [Victoria Morales](https://www.linkedin.com/in/victoria-morales-16b004291/)
- [Tania Garcia](https://www.linkedin.com/in/tania-garcia-loza-680b26177/)
- [Defne Ergin](https://www.linkedin.com/in/defne-ergin/)
- Juliet Citron
- [Jeet Gujarathi](https://www.linkedin.com/in/jeet-gujarathi-73311b268/)
- [Mohsin Zaman](https://www.linkedin.com/in/mohsin-khan-89222858/)
- [Ritika Marwah](https://www.linkedin.com/in/ritika-marwah-22ba3a166/)
- [Mounica Nakka](https://www.linkedin.com/in/mounica-nakka-461506144/)
- [Jada Stewart](https://www.linkedin.com/in/jada-stewart-a9374023a/)
- [Özlem Elgün](https://www.linkedin.com/in/%C3%B6zlem-elg%C3%BCn-044b131b2/)
- [Xuyang Ji](https://www.linkedin.com/in/xuyang-j-a34a1a93/)
- Aaron Lint
- [Pornnapa Musittimanee](https://www.linkedin.com/in/pornnapa-musittimanee/)
- [Michelle Bank](https://www.linkedin.com/in/michellefbank/)
- [Sakshi Jaiswal](https://www.linkedin.com/in/sakshijaiswaldepaul/)
- Alvaro Leal Puyol
- Khaja Musharaf Mohammad





## Python Packages

#### Facebook Comments Scraper: 

Kevin Zúñiga

#### YouTube Comments Scraper: 

Egbert Bouman

#### Slugify: 

The Django Project

#### Read & Write TXT Files: 

Pythontutorial.net

#### Selenium: 

Thoughtworks

#### Pyfiglet: 

Peter Waller

#### Beautiful Soup: 

Leonard Richardson

#### XLSX Writer: 

John McNamara

#### Requests: 

Kenneth Reitz

#### NLTK: 

Steven Bird, Edward Loper, Ewan Klein
## License

MIT License

Copyright (c) 2023 Jonas Gideon Banes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

