#include <stdio.h>
#define pinMode(x,y) do { printf("pinMode(%d, %d)\n", (x), (y)); } while (0)
#define digitalWrite(p, v) do { printf("digital[%d]=%d\n", (p), (v)); } while (0)
#define delay(d) usleep((d)*1000)
#define OUTPUT 0
#define HIGH 1
#define LOW  0
#include "arduino.pde"
int main(void)
{
  setup();
  while(1) loop();
}
