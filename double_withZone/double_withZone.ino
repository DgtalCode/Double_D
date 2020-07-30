#include <iarduino_HC_SR04.h>
#include <DcMotor.h>

#define ARRAY_LEN 5

int arr[ARRAY_LEN];

bool flag = false;

DcMotor m1, m2;

iarduino_HC_SR04 lhc(37, 38);

iarduino_HC_SR04 rhc(33, 34);

iarduino_HC_SR04 thc(35, 36);

volatile int counter = 0;

int oldCounter = 0;

void encTick() {
  counter++;
}

float d = 7, r = 8.2, pi = 3.14, full_rot = 1200, v2 = 90;

/////////////////////////////////////////////////////////////////////////////////////////////////////////// SIGN OF THE NUMBER //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
static inline int8_t sign(int val) {
  if (val < 0) return -1;
  if (val == 0) return 0;
  return 1;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////// GO FORWARD //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void go(int cm) {
  int counter_local = counter;
  float x = (1200 * abs(cm)) / (d * pi);
  while ((counter - counter_local) < x) {
    m1.move(v2 * sign(cm));
    m2.move(v2 * sign(cm));
  }
  m1.stop();
  m2.stop();
  delay(100);
}

void go(int cm, int t) {
  int counter_local = counter;
  float x = (1200 * abs(cm)) / (d * pi);
  while ((counter - counter_local) < x) {
    m1.move(v2 * sign(cm));
    m2.move(v2 * sign(cm));
  }
  m1.stop();
  m2.stop();
  delay(t);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////// ROTATE TO ANGLE (NO) ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void rotate(int a) {
  int counter_local = counter;
  float cm = (pi * r * abs(a)) / 180;
  float x = (2800 * cm) / (7.8 * pi);
  while ((counter - counter_local) < x) {
    m1.move(v2 * sign(a));
    m2.move(-v2 * sign(a));
  }
  m1.stop();
  m2.stop();
  delay(100);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////// MOTOR STOP //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void mstop(int t){
  m1.stop();
  m2.stop();
  delay(t);
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////// GREEN MARKS /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void do_smthng(int todo) {
  switch (todo) {
    case 0:
      go(7);
      rotate(-55);
      go(-5);
      break;
    case 1:
      go(7);
      rotate(55);
      go(-5);
      break;
    case 2:
      go(5);
      rotate(155);
      go(-5);
      break;
  }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////// UART RECEIVE ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void receive2() {
  String st = "";
  int incByte = 0;
  int counter = 0;
  while (true) {
    if (Serial2.available() > 0) {

      incByte = Serial2.read();

      //Serial.println(incByte);

      if (incByte == 58) {
        //Serial.println("Start");
        continue;
      }

      if (incByte == 59) {
        //Serial.println("Stop");
        break;
      }

      if (incByte != 47)
        st += (char)incByte;
      else {
        //Serial.println(st);
        arr[counter] = st.toInt();
        st = "";
        counter++;
      }

    }
  }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////// WALL FOLLOWING //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int l = 9;
float kk1 = 40, kk2 = 1, u_w, v3 = 90, err_w, errold_w = 0;

void wall(){
  err_w = l - rhc.distance();
  u_w = kk1 * err_w - kk2 * (err_w - errold_w);
  errold_w = err_w;
  m1.move(v3 - u_w);
  m2.move(v3 + u_w);
  delay(1);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////// OBJEZD PREPYATSTVIY /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void objezd(){
  rotate(65);
  mstop(100);
  go(17);
  mstop(100);
  rotate(-70);
  mstop(100);
  go(25);
  mstop(100);
  rotate(-65);
  mstop(100);
  go(17);
  mstop(100);
  rotate(85);
  mstop(100);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////// MAIN FUNCTIONS //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

float k1 = 1.8, k2 = 1, ka = 1.3, v = 100, err, errold;
float u;
int cnt = 0, cnt1 = 0, dist_cnt = 0;

void setup() {
  pinMode(24, INPUT); 
  pinMode(25, INPUT); //gray
  
  attachInterrupt(0, encTick, FALLING);
  //attachInterrupt(0, flagEdit, FALLING);

  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial2.begin(9600);

  m1.begin(6, 5);
  m2.begin(8, 7);

  m1.stop();
  m2.stop();

  delay(1000);
}


void loop() {
  while (digitalRead(25) == 0) {
    arr[0] = 0;
    arr[1] = 0;
    arr[2] = 0;
    arr[3] = 3;
    arr[4] = 0;

    receive2();

    /*Serial.print(arr[0]);
    Serial.print(" ");
    Serial.print(arr[1]);
    Serial.print(" ");
    Serial.print(arr[2]);
    Serial.print(" ");
    Serial.print(arr[3]);
    Serial.println("");
    Serial.println("");*/

    err = (arr[0] + arr[1] + arr[2] * ka) / 3;
    u = k1 * err + k2 * (err - errold);
    errold = err;

    m1.move(v - u);
    m2.move(v + u);

    cnt++;
    if (arr[3] != 3 and cnt > 10) {
      m1.stop();
      m2.stop();
      delay(1000);
      do_smthng(arr[3]);
      m1.stop();
      m2.stop();
      delay(100);
      arr[3] = 3;
      cnt = 0;
      //Serial2.flush();
    }
  }
}
