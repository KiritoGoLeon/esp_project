#include <Arduino.h>
#include "HTTPClient.h"
#include <ArduinoJson.h>



// -- ina
#if ARDUINO >= 100  // Arduino IDE versions before 100 need to use the older library
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include <INA.h>  // Zanshin INA Library

#if defined(_SAM3XA_) || defined(ARDUINO_ARCH_SAMD)
// The SAM3XA architecture needs to include this library, it is already included automatically on
// other platforms //
#include <avr/dtostrf.h>  // Needed for the SAM3XA (Arduino Zero)
#endif

/**************************************************************************************************
** Declare program constants, global variables and instantiate INA class                         **
**************************************************************************************************/
const uint32_t SERIAL_SPEED{115200};     ///< Use fast serial speed
const uint32_t SHUNT_MICRO_OHM{100000};  ///< Shunt resistance in Micro-Ohm, e.g. 100000 is 0.1 Ohm
const uint16_t MAXIMUM_AMPS{1};          ///< Max expected amps, clamped from 1A to a max of 1022A
uint8_t        devicesFound{0};          ///< Number of INAs found
INA_Class      INA;                      ///< INA class instantiation to use EEPROM


const char *ssid = "LinuxRT";                      //wifi名
const char *password = "2267542848";              //wifi密码
const char *host = "http://192.168.31.221:5000"; 
const char *query_addr = "/esp_client/upload_data";

WiFiClient wifi_Client;
HTTPClient http_client;
String req;
String rsp;
 

//Wifi连接
void setupWifi()
{
  delay(10);
  Serial.println("connecting WIFI");
  WiFi.begin(ssid, password);
  while (!WiFi.isConnected())
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println("Wifi connected ok!");

  // -- find ina
  devicesFound = INA.begin(MAXIMUM_AMPS, SHUNT_MICRO_OHM);  // Expected max Amp & shunt resistance
  while (devicesFound == 0) {
    Serial.println(F("No INA device found, retrying in 10 seconds..."));
    delay(10000);                                             // Wait 10 seconds before retrying
    devicesFound = INA.begin(MAXIMUM_AMPS, SHUNT_MICRO_OHM);  // Expected max Amp & shunt resistance
  }                                                           // while no devices detected
  Serial.print(F(" - Detected "));
  Serial.print(devicesFound);
  Serial.println(F(" INA devices on the I2C bus"));
  INA.setBusConversion(8500);             // Maximum conversion time 8.244ms
  INA.setShuntConversion(8500);           // Maximum conversion time 8.244ms
  INA.setAveraging(128);                  // Average each reading n-times
  INA.setMode(INA_MODE_CONTINUOUS_BOTH);  // Bus/shunt measured continuously
  INA.alertOnBusOverVoltage(true, 5000);  // Trigger alert if over 5V on bus

}
 
void setUpHttpClient()
{
  req = (String)host + query_addr;
  Serial.println(req);
  if (http_client.begin(req))
  {
    Serial.println("HTTPclient setUp done!");
  }
}
 
void setup()
{
  Serial.begin(115200);
  delay(3000);
  setupWifi();
  setUpHttpClient();
}
 
void loop()
{

  // - get current 
  static uint16_t loopCounter = 0;     // Count the number of iterations
  static char     sprintfBuffer[100];  // Buffer to format output
  static char     busChar[8], shuntChar[10], busMAChar[10], busMWChar[10];  // Output buffers

  Serial.print(F("Nr Adr Type   Bus      Shunt       Bus         Bus\n"));
  Serial.print(F("== === ====== ======== =========== =========== ===========\n"));

    dtostrf(INA.getBusMilliVolts(0) / 1000.0, 7, 4, busChar);      // Convert floating point to char
    dtostrf(INA.getShuntMicroVolts(0) / 1000.0, 9, 4, shuntChar);  // Convert floating point to char
    dtostrf(INA.getBusMicroAmps(0) / 1000.0, 9, 4, busMAChar);     // Convert floating point to char
    dtostrf(INA.getBusMicroWatts(0) / 1000.0, 9, 4, busMWChar);    // Convert floating point to char
    sprintf(sprintfBuffer, "%2d %3d %s %sV %smV %smA %smW\n", 1, INA.getDeviceAddress(0),
            INA.getDeviceName(0), busChar, shuntChar, busMAChar, busMWChar);
    Serial.print(sprintfBuffer);

  Serial.println();
  delay(100);  // Wait 10 seconds before next reading
  Serial.print(F("Loop iteration "));
  Serial.print(++loopCounter);
  Serial.print(F("\n\n"));



  // 转换为json
  StaticJsonDocument<200> doc;
  doc["current"] = (int)(INA.getBusMicroAmps(0)/1000.0);
  doc["wa"] = INA.getBusMicroWatts(0) / 1000.0;

  String ouput;
  // 序列化
  serializeJsonPretty(doc, ouput);

  // 添加http头
  http_client.addHeader("Content-Type","application/json");
  // 发送请求
  int http_code = http_client.POST((uint8_t*)ouput.c_str(),ouput.length());
  if(http_code == 200)
  {
      rsp = http_client.getString();


      DynamicJsonDocument doc(1024);
      // json反序列化
      deserializeJson(doc, rsp);
      JsonObject obj = doc.as<JsonObject>();
      // 获得key
      String state = obj["state"];
      Serial.println(state);
  }
  delay(1000);
}