from PyPDF2 import PdfReader


#https://pypi.org/project/pdfminer.six/
archivo=PdfReader(r"H:\Mi unidad\TRABAJO\MINERÍA DE DATOS\EJEMPLOS\EJEMPLO MINERIA DE DATOS\CVS\CV_NATHAN.pdf")

number_of_pages = len(archivo.pages)
page = archivo.pages[0]
text = page.extract_text()

print (text)
if "data" in text:
    print("Es el candidato")
#for i in listadoDirectorio:
#    text = extract_text(r"H:\Mi unidad\TRABAJO\ORANGE\EJEMPLO MINERIA DE DATOS\CVS"+i)
#    if "data" in text:
#        print("El archivo que contiene BDNS es: ",i)
#        print("------------------------------------")