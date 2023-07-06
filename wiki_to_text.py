from dewiki_functions import *

#wiki_xml_file = 'F:/simplewiki-20210401/simplewiki-20210401.xml'  # update this
wiki_xml_file = r'C:\Users\larisa\Documents\Github\PlainTextWikipedia\data\simplewiki-20230220-pages-articles-multistream.xml'  # update this
json_save_dir = r'C:\Users\larisa\Documents\Github\PlainTextWikipedia\processed_files\ '

if __name__ == '__main__':
    process_file_text(wiki_xml_file, json_save_dir)