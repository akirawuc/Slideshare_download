import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import argparse
import tqdm
from PIL import Image

# python3 initium_userAnalysis.py --noPic -c './config.json'
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--site', help='The url of the website.')
args = parser.parse_args()



class slide():
    def __init__(self, url, savePath):
        self.url = url
        self.savePath = savePath
        self.get_content_info()
        self.check_exist()
        self.image_urls = {}
    def get_content_info(self):
        self.context = requests.get(self.url)
        self.soup = BeautifulSoup(self.context.text, 'html.parser')
        self.title = self.soup.find('span', class_ = 'j-title-breadcrumb').text.strip()
    def check_exist(self):
        if not os.path.isdir(f'{self.savePath}/{self.title}'):
            os.mkdir(f'{self.savePath}/{self.title}')
    def get_image_url(self):
        for item in self.soup.find_all("section", class_ = 'slide'):
            page_num = item.get('data-index')
            img_url = item.find("img", class_ = 'slide_image')
            self.image_urls[page_num] = img_url.get('data-full')
    def save_pics(self):
        for slide_num, img in tqdm.tqdm(self.image_urls.items()):
            try:
                images = urlretrieve(img, f'{self.savePath}/{self.title}/{slide_num}.jpg')
            except:
                print(f'{self.savePath}/{self.title}/{slide_num}.jpg')
        with open(f'{self.savePath}/{self.title}/info.txt', 'w') as file:
            file.write(f'Source: {self.url}, Title: {self.title}')
    def save_pdf(self):
        def readImages(path):
            this_image = Image.open(path)
            return this_image.convert('RGB')
        imageList = [readImages(f'{self.savePath}/{self.title}/{i}.jpg') for i in self.image_urls.keys()]
        imageList[0].save(f'{self.savePath}/{self.title}.pdf', save_all=True, append_images=imageList[1:])
    def save_slide(self):
        self.get_image_url()
        self.save_pics()
        self.save_pdf()



if __name__ == '__main__':
    this_slide = slide(args.site, './slide')
    this_slide.save_slide()
