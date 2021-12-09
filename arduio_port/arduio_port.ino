int moc = 0;
int odczyt_potencjometru = 0;
float pomoc;

int grzalka=3;

int led_1=6;
int led_2=7;
int led_3=8;
int led_4=9;
int led_5=10;

int kom_pot=11;
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
    
  Serial.begin(9600);
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
   
//  odczytanaWartosc = map(odczytanaWartosc, 0, 1023, 1, 5);//Przeskalowanie wartości
  
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
