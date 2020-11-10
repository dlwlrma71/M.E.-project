#include <stdio.h>
#include <wiringPi.h>
#include <softPwm.h>

#define ENCODERA 23
#define ENCODERB 24
#define ENC2REDGEAR 2165

#define MOTOR1 20
#define MOTOR2 21

#define PGAIN 1000
#define DGAIN 50
#define LOOPTIME 1

//* 초기값 설정
int encA;
int encB;
int encoderPosition = 0;
float redGearPosition = 0;
float input_value = 0;

int referencePosition;
float errorPosition;
float error_prev;

unsigned int startTime;
unsigned int checkTime;
unsigned int checkTimeBefore;

//*Interupt 되는 시점에 측정
void funcEncoderA()
{
    encA = digitalRead(ENCODERA);
    encB = digitalRead(ENCODERB);

if (encA == HIGH)
{
    if (encB == LOW)
        encoderPosition++;
    else
        encoderPosition++;
}
else
{
    if (encB == LOW)
        encoderPosition++;
    else
        encoderPosition++;
}
redGearPosition = (float)encoderPosition / ENC2REDGEAR;
errorPosition = referencePosition - redGearPosition;
}

void funcEncoderB()
{
    encA = digitalRead(ENCODERA);
    encB = digitalRead(ENCODERB);

    if (encB == HIGH)
    {
        if (encA == LOW)
            encoderPosition++;
        else
            encoderPosition++;
    }
    else
    {
        if (encA == LOW)
            encoderPosition++;
        else
            encoderPosition++;
    }
redGearPosition = (float)encoderPosition / ENC2REDGEAR;
errorPosition = referencePosition - redGearPosition;
}

//*모터 제어
int main()
{
printf("Write # of revolution: ");
scanf("%d", &referencePosition);

error_prev = referencePosition;
errorPosition = referencePosition;

wiringPiSetupGpio();
pinMode(ENCODERA, INPUT);
pinMode(ENCODERB, INPUT);

softPwmCreate(MOTOR1, 0, 100);
softPwmCreate(MOTOR2, 0, 100);

wiringPiISR(ENCODERA, INT_EDGE_BOTH, funcEncoderA);
wiringPiISR(ENCODERB, INT_EDGE_BOTH, funcEncoderB);


startTime = millis();
checkTimeBefore = millis();


//* PID Control
while(1)
{
checkTime = millis();

if (checkTime - checkTimeBefore >= LOOPTIME)
{
if (errorPosition < 0)
{
softPwmWrite(MOTOR1, (errorPosition * PGAIN + (errorPosition - error_prev) / LOOPTIME * 1000 * DGAIN));
softPwmWrite(MOTOR2, 0);
}

else

{
softPwmWrite(MOTOR1, 0);
softPwmWrite(MOTOR2, (errorPosition * PGAIN + (errorPosition - error_prev) / LOOPTIME * 1000 * DGAIN));
}


printf("error: %f, position: %f\n", errorPosition, redGearPosition);
error_prev = errorPosition;
checkTimeBefore = checkTime;
}

}

return 0;

}