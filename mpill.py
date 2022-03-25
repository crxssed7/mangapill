# Downloads mangas from mangapill.com

from bs4 import BeautifulSoup
import requests
import os

BASE_URL = 'https://mangapill.com'

def main():
    query = input('Enter manga url: ')

    response = requests.get(query)

    if response.status_code == requests.codes.ok:
        doc_response = response.text
        response_parser = BeautifulSoup(doc_response, 'html.parser')

        # Get the chapters
        chapters_div = response_parser.find('div', class_='my-3 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6')
        chapters = chapters_div.find_all('a')
        chapters.reverse()

        for c in chapters:
            print(c)

        # Create the directory
        manga_name = response_parser.find('h1', class_='font-bold text-lg md:text-2xl').text
        os.mkdir(manga_name)

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

                for page in pages:
                    # Download the page
                    try:
                        url = page['data-src']
                        filenm = chp_folder + '/' + url.split('/')[-1]

                        r = requests.get(url)

                        open(filenm, 'wb').write(r.content)
            
                        print(f"File has downloaded! Saved as {filenm}")
                    except:
                        print("Couldn't download file")    
                        print(f"Here's the download link: {url}")

if __name__ == '__main__':
    main()