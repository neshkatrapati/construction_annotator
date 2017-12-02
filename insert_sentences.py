from constructions.models import *
from tools.common import SSF, SSFSentence
import os

def insert(ssf_file, corpus_file):
	ssf = SSF.from_file(ssf_file)
	for index, sentence in enumerate(ssf):
		#print sentence.d()
		s = Sentence()
		s.treebank_id = sentence.id		
		s.plain_form = sentence.d(SSFSentence.display_mode_pos, ignore_chunks = True)
		s.treebank_form = sentence.d(SSFSentence.display_mode_full)
		s.corpus_file = corpus_file
		#print s.plain_form
		s.save()
	print corpus_file, "Inserted ", index, " Sentences"


def insert_from_fobj(ssf_file_obj, corpus_file):
	ssf =  SSF(ssf_file_obj.read())
        ssf._sentences()
	for index, sentence in enumerate(ssf):
		#print sentence.d()
		s = Sentence()
		s.treebank_id = sentence.id		
		s.plain_form = sentence.d(SSFSentence.display_mode_pos, ignore_chunks = True)
		s.treebank_form = sentence.d(SSFSentence.display_mode_full)
		s.corpus_file = corpus_file
		#print s.plain_form
		s.save()
	print corpus_file, "Inserted ", index, " Sentences"



def insert_plain(file_object, corpus_file):
	for i, line in enumerate(file_object):
		line = line.strip()
		if len(line) > 0:
			s = Sentence()
			s.treebank_id = str(i)
			s.plain_form = line
			s.treebank_form = ""
			s.corpus_file = corpus_file
			#print s.plain_form
			s.save()
	print corpus_file, "Inserted ", i, " Sentences"

def insertAllFiles(folder_path):
	for dirName, subdirList, fileList in os.walk(folder_path):
		
		for file_name in fileList:
			file_path = os.path.join(dirName, file_name)
			corpus_name = file_path[len(folder_path) + 1:]
			c = CorpusFile(name=corpus_name)	
			c.save()
			insert(file_path, c)
