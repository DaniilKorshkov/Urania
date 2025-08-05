


const int AZERO = A0;
const int AONE = A1;
const int ATWO = A2;
const int ATHREE = A3;
const int AFOUR = A4;
const int AFIVE = A5;


const int ACTUATOR_WRITE_ONE = 3;
const int ACTUATOR_WRITE_TWO = 5;



int WRITE_ONE_STATUS = LOW;
int WRITE_TWO_STATUS = LOW;
  


// https://stackoverflow.com/questions/9072320/split-string-into-string-array
String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if( data.charAt(i) == separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
  }}

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}










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


  pinMode(ACTUATOR_WRITE_ONE,OUTPUT);
  pinMode(ACTUATOR_WRITE_TWO,OUTPUT);
 



};

// the loop routine runs over and over again forever:
void loop() {

  
  if(Serial.available() > 0){

    String raw_msg = Serial.readString();
    char delimiter = '!';
    String msg = getValue(raw_msg, delimiter, 0);
    



    if(msg == "RV"){ //RV command is an inquiry for raw readings from A0-A5 ports

    int amount_of_scans = (getValue( raw_msg, delimiter, 1 )).toInt();
    


    

    // Output starts from START and ends with END. Statements are separated with "!" sign
    Serial.print("START!AZEROVOLTAGE!");
    for(int i=0; i < amount_of_scans; i++){
      int READ = analogRead(AZERO);
      Serial.print(READ);
      if ( i<(amount_of_scans-1) ){ Serial.print("+"); };

    
    };
    Serial.print("!AONEVOLTAGE!");
    for(int i=0; i < amount_of_scans; i++){
      int READ = analogRead(AONE);
      Serial.print(READ);
      if ( i<(amount_of_scans-1) ){ Serial.print("+"); };

    
    };
    Serial.print("!ATWOVOLTAGE!");
    for(int i=0; i < amount_of_scans; i++){
      int READ = analogRead(ATWO);
      Serial.print(READ);
      if ( i<(amount_of_scans-1) ){ Serial.print("+"); };

    
    };
    Serial.print("!ATHREEVOLTAGE!");
    for(int i=0; i < amount_of_scans; i++){
      int READ = analogRead(ATHREE);
      Serial.print(READ);
      if ( i<(amount_of_scans-1) ){ Serial.print("+"); };

    
    };
    Serial.print("!AFOURVOLTAGE!");
    for(int i=0; i < amount_of_scans; i++){
      int READ = analogRead(AFOUR);
      Serial.print(READ);
      if ( i<(amount_of_scans-1) ){ Serial.print("+"); };

    
    };
    Serial.print("!AFIVEVOLTAGE!");
    for(int i=0; i < amount_of_scans; i++){
      int READ = analogRead(AFIVE);
      Serial.print(READ);
      if ( i<(amount_of_scans-1) ){ Serial.print("+"); };

    
    };
  

    Serial.print("!WRITE_ONE_VOLTAGE!");
    Serial.print(WRITE_ONE_STATUS);
    Serial.print("!WRITE_TWO_VOLTAGE!");
    Serial.print(WRITE_TWO_STATUS);
    

    Serial.print("!END");
  }
    
   
    

  else if(msg == "ACT_ONE_ON"){

    WRITE_ONE_STATUS = HIGH;
    

    digitalWrite(ACTUATOR_WRITE_ONE,WRITE_ONE_STATUS);
    Serial.print("START!ACT_ONE_ONED!END");
    
    
  }

   else if(msg == "ACT_ONE_OFF"){

    WRITE_ONE_STATUS = LOW;
    
    
    digitalWrite(ACTUATOR_WRITE_ONE,WRITE_ONE_STATUS);
    Serial.print("START!ACT_ONE_OFFED!END");
   
   }


   else if(msg == "ACT_TWO_ON"){

    WRITE_TWO_STATUS = HIGH;
    

    digitalWrite(ACTUATOR_WRITE_TWO,WRITE_TWO_STATUS);
    Serial.print("START!ACT_TWO_ONED!END");
    
    
  }

   else if(msg == "ACT_TWO_OFF"){

    WRITE_TWO_STATUS = LOW;
    
    
    digitalWrite(ACTUATOR_WRITE_TWO,WRITE_TWO_STATUS);
    Serial.print("START!ACT_TWO_OFFED!END");
   
   }

   else if(msg == "PING"){
    Serial.print("START!THIS_IS_ARDUINO!END");
   }

  
    else{
      Serial.print("START!MESSAGE_NOT_RECOGNIZED!END");
    };






    
    delay(1);

  };
};


