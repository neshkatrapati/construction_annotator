from constructions.models import Sentence
from tools.common import SSF, SSFSentence

def insert(ssf_file):
	ssf = SSF.from_file(ssf_file)
	for index, sentence in enumerate(ssf):
		#print sentence.d()
		s = Sentence()
		s.treebank_id = sentence.id		
		s.plain_form = sentence.d(SSFSentence.display_mode_pos, ignore_chunks = True)
		s.treebank_form = sentence.d(SSFSentence.display_mode_full)
		#print s.plain_form
		s.save()
	print "Inserted ", index, " Sentences"