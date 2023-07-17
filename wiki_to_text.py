from dewiki_functions import *
import time

#wiki_xml_file = 'F:/simplewiki-20210401/simplewiki-20210401.xml'  # update this
wiki_xml_file = r'data\simplewiki-20230220-pages-articles-multistream.xml'  # update this
json_save_dir = r'processed_files/'

if __name__ == '__main__':
    start = time.time()
    process_file_text(wiki_xml_file, json_save_dir)
    print(f"Finished in {(time.time() - start)/60} minutes")

    start = time.time()
    concat_files(json_save_dir)
    print(f"Finished in {(time.time() - start)/60} minutes")
