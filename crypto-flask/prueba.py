from algorithms.goodies import processInput

text = "['41976', '90343', '99287', '6042', '7439', '72893', '4341', '6042', '72893', '76303', '21075', '26862', '6042', '21075']"
text = [int(binario[1:-1]) for binario in text[1:-1].replace(" ","").split(',')]

print(text)