import re


class MWDict(object):
    """ Represents a Multi word dictionary """
    def __init__(self,data,types):
        self.data = data
        self.types = types
        self.resp = re.compile("\s+")

    def _lines(self):
        """ Reads Lines in the Dict """

        self.lines = [self.resp.split(line.strip("\n \t")) for line in self.data.split("\n") if line.strip("\n\t ") not in ["\n"," ", "\t",""]]

    def rules(self):
        """ Returns all rules """
        return self.lines

    @staticmethod
    def from_file (dictfile,types):
        d = open(dictfile).read()
        m = MWDict(d,types)
        m._lines()
        return m


class MWEDetect(object):
    """ Main Class For Detecting MWEs in a Sentence """
    def __init__(self,mdict):
        """ Takes a MW dictionary to initalize """
        self.mdict = mdict

    def detect_contiguous(self,sentence):
        """ Takes a SSFSentence, and detects contiguous potential MWs """
        ri = 0
        lines = sentence.lines()
        for rule in self.mdict.rules():
            for l in range(len(lines)):
                mybl = 0
                for p in range(len(rule)-1):
                    if lines[l+p].morph.root == rule[p]: # The contiguous part.
                        mybl += 1
                    else:
                        break
                if mybl == len(rule) -1:
                    nindex = l + len(rule) -2
                    new_lines = sentence.line_list
                    new_lines = new_lines[:l-1] + [SSFLine("\t((\tUNK\t<fs etype=mwe esubtype={rule_type}>".format(rule_type=rule[-1]))] + new_lines[l:nindex+1] + [SSFLine("\t))")]  + new_lines[nindex+1:]
                    new_sentence = SSFSentence.from_lines(new_lines)
                    return new_sentence
        return sentence

    def patch_test_trie(self,sentence,trie):
        lines = sentence.lines()
        line_pointer = 0
        while line_pointer < len(lines):
            possible_endings = trie.keys(lines[line_pointer].word.decode("UTF-8"))
            if len(possible_endings) != 0:
                print lines[line_pointer].word, possible_endings
            line_pointer += 1

    def detect_conjunct_verbs(self,sentence):
        """ Takes a SSFSentence, and detects contiguous potential Conjunct verbs """
        ri = 0
        lines = sentence.lines()
        for rule in self.mdict.rules():
          l = 0
          p = 0
          st = 0
          while l < len(lines):
                if lines[l].morph.root == rule[p]:
                    if (p == 0 and lines[l].tag.startswith("V")) or p <> 0:
                        if st == 0:
                            st = l
                        if p < len(rule):
                            p += 1
                        else:
                            return sentence

                if p == len(rule) - 1:
                    nindex = l
                    new_lines = sentence.line_list
                    if st > 1:
                        pre = new_lines[:st-1]
                    else :
                        pre  = []
                    new_lines = pre + [SSFLine("\t((\tetype=mwe\tesubtype= non-redup {rule_type}".format(rule_type=rule[-1]))] + new_lines[st:nindex+1] + [SSFLine("\t))")]  + new_lines[nindex:]
                    new_sentence = SSFSentence.from_lines(new_lines)
                    st = 0
                    return new_sentence

                l += 1

        #         if mybl == len(rule) -1:
        #

        return sentence


