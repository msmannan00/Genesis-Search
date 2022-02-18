import difflib

def matches(large_string, query_string, threshold):
    words = large_string.split()
    for word in words:
        s = difflib.SequenceMatcher(None, word, query_string)
        match = ''.join(word[i:i+n] for i, j, n in s.get_matching_blocks() if n)
        if len(match) / float(len(query_string)) >= threshold:
            yield match

large_string = "thelargemanhatanproject is a great project in themanhattincity"
query_string = "manhattan"
print(list(matches(large_string, query_string, 0.8)))