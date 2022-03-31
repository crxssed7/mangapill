# Downloads mangas from mangapill.com

from bs4 import BeautifulSoup
import requests
import os

BASE_URL = 'https://mangapill.com'

def download(pages, chp_folder):
    for page in pages:
        # Download the page
        try:
            url = page['data-src']
            filenm = chp_folder + '/' + url.split('/')[-1]

            r = requests.get(url)

            open(filenm, 'wb').write(r.content)
            
            print(f"File has downloaded! Saved as {filenm}")
        except KeyboardInterrupt:
            exit()
        except:
            print("Couldn't download file")    
            print(f"Here's the download link: {url}")

def whole():
    print('Downloading all chapters of a manga!')
    query = input('Enter manga ID: ')

    response = requests.get(BASE_URL + '/manga/' + query)

    if response.status_code == requests.codes.ok:
        doc_response = response.text
        response_parser = BeautifulSoup(doc_response, 'html.parser')

        # Get the chapters
        chapters_div = response_parser.find('div', class_='my-3 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6')
        chapters = chapters_div.find_all('a')
        chapters.reverse()

        # Create the directory
        manga_name = response_parser.find('h1', class_='font-bold text-lg md:text-2xl').text
        try:
            os.mkdir(manga_name)
        except FileExistsError:
            pass

        # Loop and download the chapters
        for chapter in chapters:
            # Get the link for the chapter
            link = BASE_URL + chapter['href']

            chp_name = chapter.text

            # Load the chapter
            c = requests.get(link)
            
            if c.status_code == requests.codes.ok:
                c_detail = c.text
                chapter_parser = BeautifulSoup(c_detail, 'html.parser')

                # Create a folder for the chapter
                try:
                    os.mkdir(manga_name + '/' + chp_name)
                    chp_folder = manga_name + '/' + chp_name
                except FileExistsError:
                    os.mkdir(manga_name + '/' + chp_name + ' dup')
                    chp_folder = manga_name + '/' + chp_name + ' dup'

                pages = chapter_parser.find_all('img', attrs={'class': 'js-page'})

                download(pages, chp_folder)

def single():
    print('Downloading a single chapter of a manga!')
    query = input('Enter manga ID: ')

    response = requests.get(BASE_URL + '/manga/' + query)

    if response.status_code == requests.codes.ok:
        doc_response = response.text
        response_parser = BeautifulSoup(doc_response, 'html.parser')

        # Get the chapters
        chapters_div = response_parser.find('div', class_='my-3 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6')
        chapters = chapters_div.find_all('a')
        chapters.reverse()
    
        # Create the directory
        manga_name = response_parser.find('h1', class_='font-bold text-lg md:text-2xl').text
        try:
            os.mkdir(manga_name)
        except FileExistsError:
            pass

        for (index, chapter) in enumerate(chapters, start=1):
            # Get the link for the chapter
            link = BASE_URL + chapter['href']
            chp_name = chapter.text
            print(f'\x1b[1;33m· ({index}) - {chp_name}')

        c = int(input('Enter the chapter number: ')) - 1

        chapter  = chapters[c]
        # Get the link for the chapter
        link = BASE_URL + chapter['href']
        chp_name = chapter.text

        # Load the chapter
        c = requests.get(link)
        
        if c.status_code == requests.codes.ok:
            c_detail = c.text
            chapter_parser = BeautifulSoup(c_detail, 'html.parser')

            # Create a folder for the chapter
            try:
                os.mkdir(manga_name + '/' + chp_name)
                chp_folder = manga_name + '/' + chp_name
            except FileExistsError:
                os.mkdir(manga_name + '/' + chp_name + ' dup')
                chp_folder = manga_name + '/' + chp_name + ' dup'

            pages = chapter_parser.find_all('img', attrs={'class': 'js-page'})

            download(pages, chp_folder)


if __name__ == '__main__':
    choice = input("Do you want to download a single chapter? (y/N): ")
    if choice.lower() == 'y':
        single()
    else:
        whole()