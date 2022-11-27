function enviarcorreo(enviado) {
  const info=enviado.namedValues
  const area=info['ÁREA'][0];
  const tema=info['TIPO'][0];
  const detalles=info['REQUERIMIENTO'][0];
  const usuario=info['Dirección de correo electrónico'][0];
  const hora=info['Marca temporal'][0];
  const archivo=info['¿DESEAS INCLUIR UN ARCHIVO?'][0];
  var hoja=SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Respuestas de formulario 1");
  var ultimafila=hoja.getLastRow();
  var idConsecutivo=ultimafila-1;
  //colocamos el valor
  hoja.getRange(ultimafila,1).setValue(idConsecutivo);
  ticket=hoja.getRange(ultimafila,1).getValue()
const mensaje=+usuario+hora+detalles+archivo
const asunto=" "+"Ticket N°"+ticket+" "+"-"+" "+area+" "+"-"+" "+tema
const correos="irumiche@globokas.com"+","+","+usuario
var textohtml=HtmlService.createHtmlOutputFromFile("diseño").getContent();
  textohtml=textohtml.replace("{{AREA}}",area)
  textohtml=textohtml.replace("{{TEMA}}",tema)
  textohtml=textohtml.replace("{{DETALLES}}",detalles)
  textohtml=textohtml.replace("{{USUARIO}}",usuario)
  textohtml=textohtml.replace("{{HORA}}",hora)
  textohtml=textohtml.replace("{{ARCHIVO}}",archivo)
  textohtml=textohtml.replace("{{TICKET}}",ticket)
  if (archivo.length>0){
        textohtml=textohtml.replace("{{TEXTO}}","Este es el archivo adjuntado:");
  } else {
        textohtml=textohtml.replace("{{TEXTO}}", " ");
  }  
  
GmailApp.sendEmail(correos,asunto,mensaje,{htmlBody:textohtml}) 
}

/*ACÁ USAREMOS UNA FUNCION PARA ENVIAR UN EMAIL DE PRUEBA Y SE ACTIVEN LOS PERMISOS */

function permisos(){
  GmailApp.sendEmail("irumiche@globokas.com","Mail de prueba","Prueba");
  FormApp.getActiveForm();
}

function ticket(valor1){
  resultado=Date.parse(valor1)
  return resultado
}


