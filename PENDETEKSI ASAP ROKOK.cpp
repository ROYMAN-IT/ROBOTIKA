#include <Wire.h>

#include <LiquidCrystal_I2C.h>


const int led_aman = 13;
const int led_bahaya = 12;
const int buzzer = 7;
const int gas = A0;

const int batas_aman = 717;

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup(){
  pinMode(led_aman, OUTPUT);
  pinMode(led_bahaya, OUTPUT);
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  
}

void loop(){
  int nilai_gas = analogRead(gas);
  Serial.print("gas sensor : ");
  Serial.println(nilai_gas);
  
  if(nilai_gas > batas_aman){
    digitalWrite(led_bahaya, HIGH);
    
    digitalWrite(led_aman, LOW);
    analogWrite(buzzer, 250);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("ASAP ROKOK");
    lcd.setCursor(0, 1);
    lcd.print("TERDETEKSI !!!");
    
  }
  else{
    digitalWrite(led_bahaya, LOW);
    digitalWrite(led_aman, HIGH);
    analogWrite(buzzer, 0);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("AMAN");
    
  }
  delay(300);
               
}