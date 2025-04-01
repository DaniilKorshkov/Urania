/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/


const int AZERO = A0;
const int AONE = A1;
const int ATWO = A2;
const int ATHREE = A3;
const int AFOUR = A4;
const int AFIVE = A5;

const int RED_PIN = 3;
const int GREEN_PIN = 4;
const int BLUE_PIN = 5;


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  pinMode(AZERO,INPUT);
  pinMode(AONE,INPUT);
  pinMode(ATWO,INPUT);
  pinMode(ATHREE,INPUT);
  pinMode(AFOUR,INPUT);
  pinMode(AFIVE,INPUT);

  pinMode(RED_PIN,OUTPUT);
  pinMode(GREEN_PIN,OUTPUT);
  pinMode(BLUE_PIN,OUTPUT);
};

// the loop routine runs over and over again forever:
void loop() {

  
  if(Serial.available() > 0){

    String msg = Serial.readString();
    if(msg == "RV!"){

    int AZEROREAD = analogRead(AZERO);
    int AONEREAD = analogRead(AONE);
    int ATWOREAD = analogRead(ATWO);
    int ATHREEREAD = analogRead(ATHREE);
    int AFOURREAD = analogRead(AFOUR);
    int AFIVEREAD = analogRead(AFIVE);


    digitalWrite(GREEN_PIN,HIGH);

    //float amperage = voltage / resistance;

    // print out the value you read:
    Serial.print("CQ!AZEROVOLTAGE!");
    Serial.print(AZEROREAD);
    Serial.print("!AONEVOLTAGE!");
    Serial.print(AONEREAD);
    Serial.print("!ATWOVOLTAGE!");
    Serial.print(ATWOREAD);
    Serial.print("!ATHREEVOLTAGE!");
    Serial.print(ATHREEREAD);
    Serial.print("!AFOURVOLTAGE!");
    Serial.print(AFOURREAD);
    Serial.print("!AFIVEVOLTAGE!");
    Serial.print(AFIVEREAD);
    Serial.print("!QRT");
    
    delay(100);
    digitalWrite(GREEN_PIN,LOW);
    }
    else{
      digitalWrite(RED_PIN,HIGH);
      delay(100);
      digitalWrite(RED_PIN,LOW);

     


    };
    delay(1);

  };
}
