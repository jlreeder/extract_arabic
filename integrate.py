from pprint import pprint
from collections import defaultdict

# Helper functions
def parse_decision(lines):
    """Returns a list of the information neede to add lang tags:
       the word, it's language tag, and the line"""

    cases = []
    word = ""
    decision = ""
    line = 0

    for i, l in enumerate(lines):
        if l.startswith("** "):
            cases.append((word, decision, int(line)))
            word = l[8:]
            decision = ""
            line = 0
        elif l.startswith("*** Decision"):
            decision = lines[i+1]
        elif l.startswith("*** Line"):
            line = lines[i+1]

    return cases[1:]

def add_tag(word, language, text):
    """Add a language tag around a word in a string"""

    tag_open = "<lang script=\"A\" lang=\"%s\">" % (language)
    tag_close = "</lang>"

    before, after = text.split(word)
    before += tag_open
    after = tag_close + after

    return before + word + after

# Run functions
def parse_decisions_doc():
    """Run function parse_decisions() on input file"""
    global decisions

    with open("cases.org", "r") as f:
        lines = f.read().splitlines()
        lines_cases = lines[19:]
    decisions = parse_decision(lines_cases)

def test_tags():
    """Make sure that all tags are acceptable"""

    acceptable_tags = ['Hindustani', 'Turkish', 'Arabic', 'Persian']
    unique_tags = set([d[1] for d in decisions])
    for u in unique_tags:
        if u not in acceptable_tags:
            print("Warning: the tag %s is unacceptable." % (u))

def create_complete_dictionary_file():
    """Add tags to a new copy of the dictionary
       This is very large and isn't a good way of testing"""
    # TODO: Refactor this to use the output of create_changes_file() below

    lines_to_change = [d[2] for d in decisions]
    with open("monier.xml", "r") as f:
        lines = f.read().splitlines()
        with open("monier_with_lang_tags.xml", "w") as w:
            for i, line in enumerate(lines):
                if i in lines_to_change:
                    w.write(add_tag(d[0], d[1], lines[d[2]]) + "\n")
                else:
                    w.write(line + "\n")

def create_changes_file():
    """Add tags to a special "changes" file"""

    changes = defaultdict(list)
    lines_to_change = [d[2] for d in decisions]
    doubles = set([l for l in lines_to_change if lines_to_change.count(l) > 1])
    decisions_with_doubles = [d for d in decisions if d[2] in doubles]
    decisions_without_doubles = [d for d in decisions if d[2] not in doubles]
    assert len(decisions) == len(decisions_with_doubles) + len(decisions_without_doubles)

    with open("monier.xml", "r") as f:
        lines = f.read().splitlines()
        for d in decisions:
            if d[2] in changes:
                changes[d[2]] = add_tag(d[0], d[1], changes[d[2]])
            else:
                changes[d[2]] = add_tag(d[0], d[1], lines[d[2]])
    # pprint(changes)

    with open("changes.xml", "w") as f:
        for k,v in sorted(changes.items()):
            f.write(str(k) + "\n")
            f.write("".join(v) + "\n\n")
        # f.write("\n".join(changes))

def run():
    parse_decisions_doc()
    test_tags()
    # create_complete_dictionary_file()
    create_changes_file()

run()