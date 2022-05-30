
import re

textfile = open("3-FA-2121_COSTADO_TAMPOS.TXT", 'r')
filetext = textfile.read()
textfile.close()
matches = re.findall("(<(\d{4,5})>)?", filetext)

print(matches)