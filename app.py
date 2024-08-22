import html


m_file = "yd3fwwVsdm-B-19kg-FzSdbVyRNCKEQL.txt"
m_json = open(m_file, 'r', encoding='unicode_escape').read()
murl = m_json.split("\",")[0][10:]
mhtml = m_json.split("\",")[1][10:-2]
