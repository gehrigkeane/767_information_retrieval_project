#	Author:		Gehrig Keane
#	Purpose:	Validate token formatting
#	Description:Verify that no punctuation or uppercase letters exist within the preprocessed documents.
#				Uses sets and examines every character of the file.

import sys, tempfile, os
from subprocess import call

# List and open every file in current dir
tk_files = [file for file in os.listdir(".") if file.endswith(".tk")]
lower_case_char = range(97, 123)
lower_case_char.append(32)
out = ""

for x,y in enumerate(tk_files):
	map_char = [0] * 256
	pass_flag = True
	#	Populate character map with characters in a document
	with open(y,'r') as f:
		#	Iterates through each character of the file at hand
		for ch in iter(lambda: f.read(1), ''):
			#	ACSII mapping of file characters
			map_char[ord(ch)] += 1

	#	Iterate through character map
	out += "-" * 50 + "\n"
	out += y + ": Token Verification" + "\n"
	for x,y in enumerate(map_char):
		if x not in lower_case_char and y != 0:
			pass_flag = False
			out += (str(y).ljust(5) + " - Occurrences of ASCII [" + str(x) + "] -> [" + chr(x) + "]\n") 

	out += "Test Results: PASS\n" if pass_flag else "Test Results: FAIL\n"
	out += ("-" * 50) + "\n"

EDITOR = os.environ.get('EDITOR','vim')
initial_message = "Hello world"

with tempfile.NamedTemporaryFile(suffix=".tmp") as tempfile:
  tempfile.write(out)
  tempfile.flush()
  call([EDITOR, tempfile.name])