#	Author:		Gehrig Keane
#	Purpose:	Remove .tk from file extenstion
#	Description:Python execerpt to rename files, namely, file extensions

import os, sys

htm_files = [file for file in os.listdir(".") if file.endswith(".tk")]

for filename in htm_files:
	os.rename(filename, filename[:-3])