#	Author:		Gehrig Keane
#	Purpose:	Change the file extension .htm or .html to .tk
#	Description:Python execerpt to rename files, namely, file extensions

import os, sys

htm_files = [file for file in os.listdir(".") if file.endswith(".htm") or file.endswith(".html")]

for filename in htm_files:
	os.rename(filename, filename+".tk")