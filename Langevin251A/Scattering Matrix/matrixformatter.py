import os
path = '/Users/sofiavallejo/Documents/UPF/Music Tech Lab/Langevin251A/Scattering Matrix'
os.chdir(path)

# Open the file in read mode
file_path = 'langevin251.txt'
file = open(file_path, 'r')

# Read the contents into a variable
txt = file.read()

# Close the file
file.close()

txt = txt.replace('{','[').replace('}',']').replace(' ','').replace('==', '=')

# Open the file in write mode
file_path = 'langevin251.txt'
file = open(file_path, 'w')

# Write the string to the file
file.write(txt)

# Close the file
file.close()

