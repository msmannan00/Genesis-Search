import difflib


def ireplace(old, repl, text):
    m_tokenize_description = text.split(" ")
    m_description = ""

    for m_token in m_tokenize_description:
        if old in m_token:
            m_description += repl + " "
        else:
            m_description += m_token + " "
    return m_description

print(ireplace("hello","world","hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello "))