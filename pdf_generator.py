#  MIT License
#
#  Copyright (c) 2021 Obaydah BOUIFADENE
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import json
import os
import re
import sys
import urllib.request
from urllib.error import HTTPError

from fpdf import FPDF


def network_logs_to_page_links(number_of_pages: int, json_path: str):
    pattern = r".*/page_[0-9]*/original.*"
    number_of_pages += 10
    a = 0
    with open("./log_entries.json", "r") as json_file:
        network = json.load(json_file)
        pages = [None] * number_of_pages
        my_dict = network
        for value in my_dict:
            if "params" in my_dict[value]:
                if "request" in my_dict[value]["params"]:
                    if ("url" in my_dict[value]["params"]["request"]) and bool(
                            re.match(pattern, my_dict[value]["params"]["request"]["url"])):
                        if my_dict[value]["params"]["request"]["url"] is not None and bool(
                                re.match(pattern, my_dict[value]["params"]["request"]["url"])):
                            page_url = my_dict[value]["params"]["request"]["url"]
                            page_number = (page_url.split('/')[7].split('_'))[1]
                            pages[int(page_number)] = page_url
                            a += 1

        for i in range(len(pages) - 1, -1, -1):
            if pages[i] is None:
                pages.pop()
            else:
                break
        for i in range(len(pages)):
            if i != 0 and pages[i] is None:  # what if the last page is needed
                print(f"error with page {i} not found, please check the json file")
        return pages


def pages_links_to_images(pages: list):
    if not os.path.exists('images'):
        os.makedirs('images')
    for i in range(len(pages)):
        if pages[i] is not None:
            try:
                urllib.request.urlretrieve(str(pages[i]), './images/page_' + str(i) + '.jpg')
            except HTTPError as e:
                print("you don't have permission to download those images")
                sys.exit(404)


def images_to_pdf():
    pdf = FPDF()
    images = list(os.listdir('images'))
    images.sort(key=lambda img: int(img[:-4].split("_")[1]))
    for image in images:
        pdf.add_page()
        pdf.image('./images/' + str(image), 0, 0, 210, 297)
    pdf.output("pdf_file.pdf", "F")


def generate_pdf():
    L = network_logs_to_page_links(30, "")
    pages_links_to_images(L)
    images_to_pdf()
    print(L, len(L), sep="\n")
    # images_to_pdf()
