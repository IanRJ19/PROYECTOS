from pdfminer.high_level import extract_text

#https://pypi.org/project/pdfminer.six/
archivo=(r"H:\Mi unidad\TRABAJO\MINERÍA DE DATOS\EJEMPLOS\EJEMPLO MINERIA DE DATOS\CVS\CV_NATHAN.pdf")

text = extract_text(archivo)
print(text)
if "data" in text:
    print("Es el candidato")
