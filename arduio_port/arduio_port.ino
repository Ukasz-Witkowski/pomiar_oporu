int moc = 0;
int odczyt_potencjometru = 0;
float pomoc;

const int grzalka=D1;

int led_1=D2;
int led_2=D3;
int led_3=D4;
int led_4=D5;
int led_5=D6;

int kom_pot=D6;
int potencjometr=A0;

void setup() {
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(grzalka, OUTPUT);
  
  pinMode(led_1, OUTPUT);
  pinMode(led_2, OUTPUT);
  pinMode(led_3, OUTPUT);
  pinMode(led_4, OUTPUT);
  pinMode(led_5, OUTPUT);
  pinMode(kom_pot, INPUT);
    
  Serial.begin(115200);
}

void loop() {
  
if(digitalRead(kom_pot)==LOW)
{
  if (Serial.available() > 0) 
    {
    String input = Serial.readStringUntil('\n');
    moc=input.toInt();
    Serial.println("zmiana na:");
    Serial.println(moc);
    Serial.flush();
    }
}
//print()
if(digitalRead(kom_pot)==HIGH)
{
  odczyt_potencjometru = analogRead(potencjometr);
  pomoc=round(100.0*odczyt_potencjometru/1023.0);
  moc=(int)pomoc;
  Serial.println("zmiana na:");
  Serial.println(moc);
}
   
  
  if (moc < 1) 
  {
      digitalWrite(led_1, LOW); 
      digitalWrite(led_2, LOW); 
      digitalWrite(led_3, LOW); 
      digitalWrite(led_4, LOW); 
      digitalWrite(led_5, LOW); 
  } 
  else if (moc>=1 and moc<20) 
  { 
      digitalWrite(led_1, HIGH); 
      digitalWrite(led_2, LOW); 
      digitalWrite(led_3, LOW); 
      digitalWrite(led_4, LOW); 
      digitalWrite(led_5, LOW);     
  } 
  else if (moc>=20 and moc<40) 
  {  
      digitalWrite(led_1, HIGH); 
      digitalWrite(led_2, HIGH); 
      digitalWrite(led_3, LOW); 
      digitalWrite(led_4, LOW); 
      digitalWrite(led_5, LOW);      
  }
  else if (moc>=40 and moc<60) 
  {
      digitalWrite(led_1, HIGH); 
      digitalWrite(led_2, HIGH); 
      digitalWrite(led_3, HIGH); 
      digitalWrite(led_4, LOW); 
      digitalWrite(led_5, LOW);     
  }
  else if (moc>=60 and moc<80) 
  {
      digitalWrite(led_1, HIGH); 
      digitalWrite(led_2, HIGH); 
      digitalWrite(led_3, HIGH); 
      digitalWrite(led_4, HIGH); 
      digitalWrite(led_5, LOW);     
  }  
  else 
  {
      digitalWrite(led_1, HIGH); 
      digitalWrite(led_2, HIGH); 
      digitalWrite(led_3, HIGH); 
      digitalWrite(led_4, HIGH); 
      digitalWrite(led_5, HIGH);   
  }

  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(grzalka, HIGH);
  delay(10*moc);                       
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(grzalka, LOW);
  delay(10*(100-moc));   
 
}
