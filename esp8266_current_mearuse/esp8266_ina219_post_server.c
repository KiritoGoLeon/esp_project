#include <Arduino.h>
#include <ArduinoJson.h>
// 8266
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

HTTPClient http_client;

const char *ssid = "LinuxRT";                      //wifi名
const char *password = "2267542848";              //wifi密码
const char *host = "http://192.168.31.127:5000"; 
const char *query_addr = "/esp_client/upload_data";

String req;
String rsp;

// lcd
#include <U8g2lib.h>
#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

U8G2_SSD1306_72X40_ER_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);   // EastRising 0.42" OLED

// ina
#include <INA.h>  // Zanshin INA Library
#if defined(_SAM3XA_) || defined(ARDUINO_ARCH_SAMD)
#endif
/**************************************************************************************************
** Declare program constants, global variables and instantiate INA class                         **
**************************************************************************************************/
const uint32_t SERIAL_SPEED{115200};     ///< Use fast serial speed
const uint32_t SHUNT_MICRO_OHM{100000};  ///< Shunt resistance in Micro-Ohm, e.g. 100000 is 0.1 Ohm
const uint16_t MAXIMUM_AMPS{1};          ///< Max expected amps, clamped from 1A to a max of 1022A
uint8_t        devicesFound{0};          ///< Number of INAs found
INA_Class      INA;                      ///< INA class instantiation to use EEPROM
// INA_Class      INA(0);                 ///< INA class instantiation to use EEPROM
// INA_Class      INA(5);                 ///< INA class instantiation to use dynamic memory rather
//   than EEPROM. Allocate storage for up to (n) devices


//Wifi连接
void setupWifi()
{
  delay(10);
  Serial.println("connecting WIFI");
  WiFi.begin(ssid, password);


  u8g2.clearBuffer();					// clear the internal memory
  u8g2.drawStr(0,40,"wifi ing");
  u8g2.sendBuffer();	


  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  u8g2.clearBuffer();					// clear the internal memory
  u8g2.drawStr(0,40,"wifi ok！");
  u8g2.sendBuffer();
}

void setupIna()
{
  // -- find ina
  devicesFound = INA.begin(MAXIMUM_AMPS, SHUNT_MICRO_OHM);  // Expected max Amp & shunt resistance
  while (devicesFound == 0) {
    Serial.println(F("No INA device found, retrying in 10 seconds..."));
    delay(1000);                                             // Wait 10 seconds before retrying
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

void setupHttp()
{
  req = (String)host + query_addr;
  Serial.println(req);
  http_client.begin(req);
}

void setup(void) {
  Serial.begin(115200);
  // lcd
  u8g2.begin();
  u8g2.setFont(u8g2_font_t0_15b_mr);	// choose a suitable font

  // ina
  setupIna();
  u8g2.clearBuffer();					// clear the internal memory
  u8g2.drawStr(0,20,"find ina!");
  u8g2.sendBuffer();	

  delay(1000);
  // wifi
  setupWifi();
  // http
   setupHttp();
}

char buff[50];



void loop(void) {

  u8g2.clearBuffer();					// clear the internal memory
  sprintf(buff,"ma:%d",abs(INA.getBusMicroAmps(0)/1000.0));
  u8g2.drawStr(0,20,buff);
  u8g2.drawStr(0,40,"wifi ok！");
  u8g2.sendBuffer();					// transfer internal memory to the display  
  printf("current:%d\r\n",abs(INA.getBusMicroAmps(0)/1000.0));


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
   Serial.println(http_code);
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