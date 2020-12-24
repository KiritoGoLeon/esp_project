# esp32 INA219 current measure with python flask server

平台: esp32 + vscode + platformio + arduino + ina219

服务器: python3 flask + mysql

GPIO:

```
/** PIN **
 * OLED:VCC  --- ESP32:3.3V
 * OLED:GND  --- ESP32:GND
 * OLED:SCL  --- ESP32:D22
 * OLED:SDA  --- ESP32:D21
 * * 
 * */

```



传输协议: http post

功能:  能采集ina219的电流和功率数据, 传输到flask服务器, 并且图像显示出来

效果:

![image-20201215221140808](README.assets/image-20201215221140808.png)