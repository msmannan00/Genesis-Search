# Local Imports
import mimetypes
import pathlib
import re
import validators

from abc import ABC
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from raven.transport import requests
from thefuzz import fuzz

# class to parse html raw duplicationHandlerService
from genesis_modules.user_data_parser.parse_instance.constants.constant import CRAWL_SETTINGS_CONSTANTS
from genesis_modules.user_data_parser.parse_instance.constants.strings import STRINGS
from genesis_modules.user_data_parser.parse_instance.i_crawl_crawler.i_crawl_enums import PARSE_TAGS
from genesis_modules.user_data_parser.parse_services.helper_services.helper_method import helper_method
from genesis_modules.user_data_parser.parse_services.helper_services.spell_check_handler import spell_checker_handler
from genesis_shared_directory.service_manager.topic_manager.topic_classifier_controller import \
    topic_classifier_controller
from genesis_shared_directory.service_manager.topic_manager.topic_classifier_enums import TOPIC_CLASSFIER_COMMANDS


class html_parse_manager(HTMLParser, ABC):

    def __init__(self, m_base_url, m_html):
        super().__init__()
        self.m_html = m_html
        self.m_base_url = m_base_url

        self.m_title = STRINGS.S_EMPTY
        self.m_meta_description = STRINGS.S_EMPTY
        self.m_important_content = STRINGS.S_EMPTY
        self.m_important_content_raw = []
        self.m_content = STRINGS.S_EMPTY
        self.m_meta_keyword = STRINGS.S_EMPTY
        self.m_content_type = CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_GENERAL
        self.m_sub_url = []
        self.m_image_url = []
        self.m_doc_url = []
        self.m_video_url = []

        self.m_paragraph_count = 0
        self.m_parsed_paragraph_count = 0
        self.m_query_url_count = 0
        self.m_non_important_text = STRINGS.S_EMPTY
        self.rec = PARSE_TAGS.S_NONE
        self.all_url_count = 0

    # find url type and populate the list respectively

    def __insert_external_url(self, p_url):
        self.all_url_count+=1
        if p_url is not None and not str(p_url).__contains__("#"):
            mime = mimetypes.MimeTypes().guess_type(p_url)[0]
            if 5 < len(p_url) <= CRAWL_SETTINGS_CONSTANTS.S_MAX_URL_SIZE:

                # Joining Relative URL
                if not p_url.startswith("https://") and not p_url.startswith("http://") and not p_url.startswith("ftp://"):
                    m_temp_base_url = self.m_base_url
                    p_url = requests.compat.urljoin(m_temp_base_url.m_url, p_url)
                    p_url = p_url.replace(" ", "%20")
                    p_url = helper_method.on_clean_url(helper_method.normalize_slashes(p_url))

                if validators.url(p_url):
                    suffix = ''.join(pathlib.Path(p_url).suffixes)
                    m_host_url = helper_method.get_host_url(p_url)
                    if mime is None:
                        mime = mimetypes.MimeTypes().guess_type(p_url)[0]
                    if mime is not None and mime != "text/html":
                        if suffix in CRAWL_SETTINGS_CONSTANTS.S_DOC_TYPES and len(self.m_doc_url) < 10:
                            self.m_doc_url.append(p_url)
                        elif str(mime).startswith("video") and len(self.m_video_url) < 10:
                            self.m_video_url.append(p_url)
                    elif m_host_url.__contains__(".onion"):
                        if m_host_url.__contains__("?"):
                            self.m_query_url_count+=1
                        if self.m_query_url_count < 5:
                            self.m_sub_url.append(p_url)


    def handle_starttag(self, p_tag, p_attrs):
        if p_tag == "a":
            for name, value in p_attrs:
                if name == "href":
                    self.__insert_external_url(value)

        if p_tag == 'img':
            for value in p_attrs:
                if value[0] == 'src' and not helper_method.is_url_base_64(value[1]) and len(self.m_image_url)<35:
                    # Joining Relative URL
                    m_temp_base_url = self.m_base_url
                    if not m_temp_base_url.m_url.endswith("/"):
                        m_temp_base_url.m_url = m_temp_base_url.m_url + "/"
                    m_url = requests.compat.urljoin(m_temp_base_url.m_url, value[1])
                    m_url = helper_method.on_clean_url(helper_method.normalize_slashes(m_url))
                    self.m_image_url.append(m_url)

        elif p_tag == 'title':
            self.rec = PARSE_TAGS.S_TITLE

        elif p_tag == 'h1' or p_tag == 'h2' or p_tag == 'h3' or p_tag == 'h4':
            self.rec = PARSE_TAGS.S_HEADER

        elif p_tag == 'span' and self.m_paragraph_count==0:
            self.rec = PARSE_TAGS.S_SPAN

        elif p_tag == 'div':
            self.rec = PARSE_TAGS.S_DIV

        elif p_tag == 'li':
            self.rec = PARSE_TAGS.S_PARAGRAPH

        elif p_tag == 'br':
            self.rec = PARSE_TAGS.S_BR

        elif p_tag == 'p':
            self.rec = PARSE_TAGS.S_PARAGRAPH
            self.m_paragraph_count+=1

        elif p_tag == 'meta':
            try:
                if p_attrs[0][1] == 'description':
                    if len(p_attrs) > 1 and len(p_attrs[1]) > 0 and p_attrs[1][0] == 'content' and p_attrs[1][1] is not None:
                        self.m_meta_description += p_attrs[1][1]
                elif p_attrs[0][1] == 'keywords':
                    if len(p_attrs) > 1 and len(p_attrs[1]) > 0 and p_attrs[1][0] == 'content' and p_attrs[1][1] is not None:
                        self.m_meta_keyword = p_attrs[1][1].replace(",", " ")
            except Exception:
                pass
        else:
            self.rec = PARSE_TAGS.S_NONE

    def handle_endtag(self, p_tag):
        if p_tag == 'p':
            self.m_paragraph_count -= 1
        if self.rec != PARSE_TAGS.S_BR:
            self.rec = PARSE_TAGS.S_NONE

    def handle_data(self, p_data):
        if self.rec == PARSE_TAGS.S_HEADER:
            self.__add_important_description(p_data)
        if self.rec == PARSE_TAGS.S_TITLE:
            self.m_title = p_data
        elif self.rec == PARSE_TAGS.S_META and len(self.m_title) > 0:
            self.m_title = p_data
        elif self.rec == PARSE_TAGS.S_PARAGRAPH or self.rec == PARSE_TAGS.S_BR:
            self.__add_important_description(p_data)
        elif self.rec == PARSE_TAGS.S_SPAN and p_data.count(' ')>5:
            self.__add_important_description(p_data)
        elif self.rec == PARSE_TAGS.S_DIV:
            if p_data.count(' ')>5 and p_data not in self.m_non_important_text:
                self.m_non_important_text += p_data
        elif self.rec == PARSE_TAGS.S_NONE:
            if self.m_paragraph_count > 0:
                self.__add_important_description(p_data)
        if self.rec == PARSE_TAGS.S_BR:
            self.rec = PARSE_TAGS.S_NONE

    # creating keyword request_manager1 for webpage representation
    def __add_important_description(self, p_data):
        if p_data.count(' ')>2 and p_data not in self.m_important_content:
            if self.m_parsed_paragraph_count<8:
                self.m_important_content_raw.append(p_data)
                self.m_parsed_paragraph_count += 1

                p_data = re.sub('[^A-Za-z0-9 ,;"\]\[/.+-;!\'@#$%^&*_+=]', '', p_data)
                p_data = re.sub(' +', ' ', p_data)
                p_data = re.sub(r'^\W*', '', p_data)


                if p_data.lower() in self.m_important_content.lower():
                    return
                if len(self.m_important_content)>2:
                    self.m_important_content = self.m_important_content + spell_checker_handler.get_instance().validate_sentence(p_data.lower())
                else:
                    self.m_important_content = self.m_important_content + spell_checker_handler.get_instance().validate_sentence(p_data.capitalize())
                if len(self.m_important_content)>250:
                    self.m_parsed_paragraph_count=9

                if len(self.m_important_content)>550:
                    self.m_important_content = self.m_important_content[0:550]

    def __clean_text(self, p_text):
        m_text = p_text

        for m_important_content_item in self.m_important_content_raw:
            m_text = m_text.replace(m_important_content_item, ' ')

        m_text = m_text.replace('\n', ' ')
        m_text = m_text.replace('\t', ' ')
        m_text = m_text.replace('\r', ' ')
        m_text = m_text.replace(' ', ' ')

        m_text = re.sub(' +', ' ', m_text)

        # Lower Case
        p_text = m_text.lower()

        # Tokenizer
        m_word_tokenized = p_text.split()

        # Word Checking
        m_content = STRINGS.S_EMPTY
        for m_token in m_word_tokenized:
            if helper_method.is_stop_word(m_token) is False and m_token.isnumeric() is False:
                m_valid_status = spell_checker_handler.get_instance().validate_word(m_token)
                if m_valid_status is True:
                    m_content += " " + spell_checker_handler.get_instance().stem_word(m_token)
                else:
                    m_content += " " + spell_checker_handler.get_instance().clean_invalid_token(m_token)

        m_content = ' '.join(m_content.split())
        return m_content


    def __generate_html(self):
        m_soup = BeautifulSoup(self.m_html, "html.parser")
        self.m_content = self.__clean_text(m_soup.get_text())

    # ----------------- Data Recievers -----------------

    def __get_title(self):
        return helper_method.strip_special_character(self.m_title).strip()

    def __get_meta_description(self):
        return helper_method.strip_special_character(self.m_important_content)

    def __get_title_hidden(self, p_title_hidden):
        return self.__clean_text(p_title_hidden)

    def __get_meta_description_hidden(self, p_description_hidden):
        return self.__clean_text(p_description_hidden)

    def __get_important_content(self):
        m_content = self.m_important_content
        if len(m_content)<150 and fuzz.ratio(m_content,self.m_meta_description)<85 and len(self.m_meta_description)>10:
            m_content+=self.m_meta_description
        if len(m_content)<150 and fuzz.ratio(m_content,self.m_non_important_text)<85 and len(self.m_non_important_text)>10:
            self.__add_important_description(self.m_non_important_text)
            m_content+=self.m_important_content
        if len(m_content)<50 and len(self.m_sub_url)>=3:
            m_content = "- No description found but contains some urls. This website is most probably a search engine or only contain references of other websites - " + self.m_title.lower()


        return helper_method.strip_special_character(m_content)[0:300]

    def __get_validity_score(self, p_important_content):
        m_rank = (((len(p_important_content) + len(self.m_title)) > 150) or len(self.m_sub_url) >= 3) * 10 + (len(self.m_sub_url) > 0 or self.all_url_count>5) * 5
        return m_rank

    def __get_content_type(self):
        if len(self.m_content)>0:
            self.m_content_type = topic_classifier_controller.get_instance().invoke_trigger(TOPIC_CLASSFIER_COMMANDS.S_PREDICT_CLASSIFIER, [self.m_title, self.m_important_content, self.m_content])
        return self.m_content_type

    def __get_static_file(self):
        return self.m_sub_url, self.m_image_url, self.m_doc_url, self.m_video_url

    def __get_content(self):
        return self.m_content

    def __get_meta_keywords(self):
        return self.m_meta_keyword

    def parse_html_files(self):
        self.__generate_html()

        m_content = self.__get_content()
        m_sub_url, m_images, m_document, m_video = self.__get_static_file()
        m_title = self.__get_title()
        m_meta_description = self.__get_meta_description()
        m_title_hidden = self.__get_title_hidden(m_title)
        m_important_content = self.__get_important_content()
        m_important_content_hidden = self.__get_meta_description_hidden(m_important_content)
        m_meta_keywords = self.__get_meta_keywords()
        m_content_type = self.__get_content_type()
        m_validity_score = self.__get_validity_score(m_important_content)

        return m_title, m_meta_description, m_title_hidden, m_important_content, m_important_content_hidden,m_meta_keywords, m_content, m_content_type, m_sub_url, m_images, m_document, m_video, m_validity_score
