from threading import Thread
import json
import re
from html2text import html2text as htt
import wikitextparser as wtp
import os
from smart_open import open
import boto3

def dewiki(text):
    text = wtp.parse(text).plain_text()  # wiki to plaintext
    text = htt(text)  # remove any HTML
    text = text.replace('\\n',' ')  # replace newlines
    text = re.sub('\s+', ' ', text)  # replace excess whitespace
    return text


def analyze_chunk(text):
    try:
        if '<redirect title="' in text:  # this is not the main article
            return None
        if '(disambiguation)' in text:  # this is not an article
            return None
        else:
            title = text.split('<title>')[1].split('</title>')[0]
            title = htt(title)
            if ':' in title:  # most articles with : in them are not articles we care about
                return None
        serial = text.split('<id>')[1].split('</id>')[0]
        content = text.split('</text')[0].split('<text')[1].split('>', maxsplit=1)[1]
        content = dewiki(content)
        return {'title': title.strip(), 'text': content.strip(), 'id': serial.strip()}
    except Exception as oops:
        print(oops)
        return None


def save_article(article, savedir):
    try:
        s3 = boto3.client('s3')
        bucket_name = ('upcars-wikipedia-embeddings')
        doc = analyze_chunk(article)
        if doc:
            filename = savedir + doc['id'] + '.txt'
            s3.put_object(Body=bytes(doc['text'].encode('utf-8')), Bucket=bucket_name, Key=filename)

        print('DONE')

    except Exception as oops:
        print(f"exception at save_article: {oops}")


def process_file_text(filename, savedir, no_articles=2):
    article = ''
    articles_count = 0
    with open(filename, 'r') as infile:
        for line in infile:
            if articles_count < no_articles:
                if '<page>' in line:
                    article = ''
                elif '</page>' in line:  # end of article
                    articles_count += 1
                    Thread(target=save_article, args=(article, savedir)).start()
                else:
                    article += line
            else:
                break


def concat_files(path_folder):
    # print(f"Files names: {os.listdir(path_folder)}")
    print(f"Files count: {len(os.listdir(path_folder))}")

    file_names = os.listdir(path_folder)
    with open("wikipedia.txt", 'w') as outfile:
        for fname in file_names:
            try:
                print(fname)
                with open(path_folder + fname, 'r') as infile:
                    outfile.write(infile.read())
                infile.close()
            except Exception as oops:
                print(oops)
                continue
    outfile.close()