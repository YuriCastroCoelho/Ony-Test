#include "HX711.h"

float FATOR_CALIBRACAO = 420.0; 
// --------------------------------------------

String SERVER = "onussync-api.onrender.com"; 
String ENDPOINT = "/atualizar/";           
String PORTA = "443";                       

const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;

HX711 scale;

void setup() {
  Serial.begin(9600);
  

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(FATOR_CALIBRACAO); 
  scale.tare(); 
  

}

void loop() {

  float pesoLido = scale.get_units(5); 
  

  int porcentagem = (int)(pesoLido * 100);
  

  if (porcentagem > 100) porcentagem = 100;
  if (porcentagem < 0) porcentagem = 0;

  Serial.print("Porcentagem lida: ");
  Serial.println(porcentagem);



  enviarComandoAT("AT+CIPSTART=\"SSL\",\"" + SERVER + "\"," + PORTA, 4000, false);
  
  
  String pedido = "GET " + ENDPOINT + String(porcentagem) + " HTTP/1.1\r\n" +
                  "Host: " + SERVER + "\r\n" +
                  "Connection: close\r\n\r\n";
  
  enviarComandoAT("AT+CIPSEND=" + String(pedido.length()), 2000, false);
  enviarComandoAT(pedido, 2000, true);
  
  delay(5000); 
}


void enviarComandoAT(String comando, const int timeout, boolean debug) {
  
}