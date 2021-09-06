
#include <MPU6050_tockn.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>

MPU6050 mpu6050(Wire);

long timer = 0;
String data;
void setup() {
  Serial.begin(9600);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  SD.begin(4);
  Wire.begin();
  mpu6050.begin();
  digitalWrite(6, HIGH);
  mpu6050.calcGyroOffsets(true);
  digitalWrite(6, LOW);
  File dataFile = SD.open("data.csv", FILE_WRITE);
  dataFile.println("ACCX;ACCY;ACCZ;GYROX;GYROY;GYROZ;ANGLX;ANGLY;ANGLZ");
  dataFile.close();
}

void loop() {
  mpu6050.update(); //complementary filter
  int valPotenziometro = analogRead(1);
  if(valPotenziometro > 500) {
    digitalWrite(5, HIGH);
    File dataFile = SD.open("data.csv", FILE_WRITE);
    dataFile.seek(EOF);
  
    if(millis() - timer > 10){
      dataFile.print(mpu6050.getAccX());
      dataFile.print(";");
      dataFile.print(mpu6050.getAccY());
      dataFile.print(";");
      dataFile.print(mpu6050.getAccZ());
      dataFile.print(";");
      dataFile.print(mpu6050.getGyroX());
      dataFile.print(";");
      dataFile.print(mpu6050.getGyroY());
      dataFile.print(";");
      dataFile.print(mpu6050.getGyroZ());
      dataFile.print(";");
      dataFile.print(mpu6050.getAngleX());
      dataFile.print(";");
      dataFile.print(mpu6050.getAngleY());
      dataFile.print(";");
      dataFile.println(mpu6050.getAngleZ());
      timer = millis();
      
    }
  
    dataFile.close();
  }
  else {
    digitalWrite(5, LOW);
  }
}
