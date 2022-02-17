import json

from django.utils.text import unescape_entities

from modules.user_data_parser.parse_instance.i_crawl_crawler.static_parse_controller import static_parse_controller
from modules.user_data_parser.parse_instance.local_shared_model.url_model import url_model


''' m_html = "&lt;head&gt;   &lt;title&gt;Ahmia - Redirect&lt;/title&gt;   &lt;meta charset=&quot;UTF-8&quot;&gt;   &lt;meta http-equiv=&quot;Refresh&quot; content=&quot;0; url=http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page&quot;&gt; &lt;/head&gt;  &lt;body&gt;   &lt;h2&gt;Redirecting to hidden service.&lt;/h2&gt;   &lt;p&gt;You are being redirected to &lt;a href=&quot;http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page&quot;&gt;http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page&lt;/a&gt;.&lt;/p&gt;   &lt;p&gt;If you are not redirected after a few seconds, please click on the link above!&lt;/p&gt;    &lt;/body&gt;"
m_html = unescape_entities(m_html)
p_request_model = url_model("https://bbc.com", 10,"general")
m_html_parser = static_parse_controller()
m_status, m_parsed_model = m_html_parser.on_parse_html(m_html, p_request_model) '''


xx = json.dumps(json.loads('{"match_all": {}}'))
print(xx)

