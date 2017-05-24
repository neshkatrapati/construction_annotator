
from tools import common
import sys
import collections
import re
import os
from django.conf import settings

def split_sentence(sentence):
	s = sentence.plain_form.split(' ')	
	return [(index, w) for index, w in enumerate(s)]


text_with_numbers = re.compile("(?P<text>[^0-9]+)(?P<number>[0-9]+)")

def extract_from_sentence(sentence):
  """  Extracts Dependency Information for `sentence` """
  drel_map = {} # Holds 'modified_name' -> ('relation' -> 'modifier_name') eg VGF1 -> (k1 -> NP2)
  names = {} # Holds 'name' (in SSF) -> token eg NP -> rAm
  for index, chunk in enumerate(sentence.chunks()): # Get Chunks from sentences

    drel_comps = None
    if chunk.name == None:
      chunk.name = chunk.pos + "0"

    if chunk.head != None:
      chunk.head = chunk.head.strip('" ')

    names[chunk.name] = chunk.d() # name -> token (~chunk.head)
    if chunk.drel:  # If chunk has drel info      
      drel_comps = chunk.drel.split(":") # Drel info in SSF is in the form 'relation:modified_name'
      if len(drel_comps) == 2: # Validate
        modified, relation = drel_comps[1], drel_comps[0]
        if modified not in drel_map: # If there is no entry in Drel_Map for the modified, create it
          drel_map[modified] = {}

        drel_map[modified][relation] = chunk.name # Link modified -> (rel -> modifier)
  return drel_map, names




def print_graph(ssf_string):
  #print ssf_string
  ssf = common.SSF(ssf_string)
  ssf._sentences()
  for sentence in ssf:
    
    drel_map, names = extract_from_sentence(sentence)
    #print drel_map, names    
    g = "digraph {\n"

    for node in drel_map:
      for label, connection in drel_map[node].items():
        g += '\t"' + names[node] + '" -> "' + names[connection] + '"[label="{label}"]'.format(**locals()) + ';\n'        
    g+= "}"

  return g


def get_graph(sentence):
	g = print_graph(sentence)
	dot_path = settings.STATIC_ROOT+"/test.dot"
	png_path = settings.BASE_DIR+"/constructions/static/constructions/test.png"
	print png_path
	if os.path.exists(dot_path):
		os.remove(dot_path)
	if os.path.exists(png_path):
		os.remove(png_path)

	with open(dot_path, 'w') as d:
		d.write(g.encode('utf-8'))

	os.system("dot -Tpng {dot_path} > {png_path}".format(**locals()))
	return png_path

#print_graph(filename)    

# def generate_flat(filename):
#   """  Generates Flat Dependency Information for `file_name` """
#   with common.SSFMMAP(filename) as ssf:
#     for sentence in ssf:
# #      print sentence.d()
#       drel_map, names = extract_from_sentence(sentence)
# #      print drel_map, names
#       generate_flat_from_deps(drel_map, names)

# generate_flat(filename)








