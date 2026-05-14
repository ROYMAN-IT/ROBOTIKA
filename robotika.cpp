#include <NewPing.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>


int hijau = 11;
int kuning = 12;
int merah = 13;
int buzer = 5;
int trig = 7;
int echo = 6;

LiquidCrystal_I2C lcd(0x27, 16, 2);
NewPing sonar(trig, echo, 400);

int distance;

void setup(){ 
pinMode(hijau, OUTPUT);
pinMode(kuning, OUTPUT);
pinMode(merah, OUTPUT);
Serial.begin(9600);
lcd.init();
lcd.backlight();
}

void loop(){
  distance = sonar.ping_cm();
  Serial.print("jarak :");
  Serial.println(distance);

  if(distance >= 0 && distance < 20){
    digitalWrite(hijau, LOW);
    digitalWrite(kuning, LOW);
    digitalWrite(merah, HIGH);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("STOP");
      analogWrite(5, 250);
  }
 

  else if(distance >= 20 && distance < 50 ) {
    digitalWrite(hijau, LOW);
    digitalWrite(kuning, HIGH);
    digitalWrite(merah, LOW);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("PELAN-PELAN");
    analogWrite(5, 0);

  }
  

 else if(distance >= 50) {
    digitalWrite(hijau, HIGH);
    digitalWrite(kuning, LOW);
    digitalWrite(merah, LOW);
    analogWrite(5, 0);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("AMAN");
  }
  delay(200);
}