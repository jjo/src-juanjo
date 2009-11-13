// LED connected to digital pin 13

#define I_DPIN01 0x0001
#define I_DPIN02 0x0002
#define I_DPIN03 0x0003

#define I_APIN00 0x0010

#define SCHED_ENTRY_RUN  0x00
#define SCHED_ENTRY_INIT 0x01

#define SCHED_ENTRY_C_DATA_SIZE 16
#define SCHED_ENTRY_I_DATA_SIZE (SCHED_ENTRY_C_DATA_SIZE/sizeof(int))
#define SCHED_ENTRY_P_DATA_SIZE (SCHED_ENTRY_C_DATA_SIZE/sizeof(void*))

#define SOS_PERIOD 200
struct sched_entry {
    int period_ms;
    int event;
    void(*func)(struct sched_entry *);
    union {
      int i[SCHED_ENTRY_I_DATA_SIZE];
      void *p[SCHED_ENTRY_P_DATA_SIZE];
      char c[SCHED_ENTRY_C_DATA_SIZE];
    } data;
    int flags_;
    int t_rem_;
};


void test(struct sched_entry *e)
{
    if (e->flags_ == SCHED_ENTRY_INIT)
      goto setup;
    e->data.i[1] = e->data.i[1] == LOW? HIGH : LOW;
    digitalWrite(e->data.i[0], e->data.i[1]);
    return;
setup:
    // sets the digital pin as output 
    pinMode(e->data.i[0], OUTPUT); 
    e->data.i[1] = LOW;
}
struct sched_entry sched_table[] = {
      { 1000, 0, test, {13,0,}},
      { 200, 0, test, {14,0,}},
      //{ 100, 0, test, {2}},
};
#ifndef ASSERT
#define ASSERT(cond) do { if(!(cond)) panic(); } while(0)
#endif
void panic()
{
  /* SOS in pin 13 ;) */
  int n;
  for( n = 0 ; ; n = (++n)%9 ) {
    digitalWrite(13, HIGH);
    // double the 3 in the middle
    delay(n/3==1? 2*SOS_PERIOD : SOS_PERIOD);
    digitalWrite(13, LOW);
    // further "silence" at last step
    delay(n==8? 4*SOS_PERIOD : SOS_PERIOD);
  }
}
void sched_setup()
{
    int i;
    for(i = 0; i < sizeof(sched_table)/sizeof(*sched_table); i++) {
	sched_table[i].flags_ = SCHED_ENTRY_INIT;
	sched_table[i].func(sched_table+i);
	sched_table[i].flags_ = SCHED_ENTRY_RUN;
    }
}
void sched_run(int tic_period_ms)
{
  int i;
  for(i = 0; i < sizeof(sched_table)/sizeof(*sched_table); i++) {
      if (sched_table[i].t_rem_ <= 0) {
	sched_table[i].func(sched_table+i);
	sched_table[i].t_rem_ += (sched_table[i].period_ms > tic_period_ms)?
	  sched_table[i].period_ms : tic_period_ms;
      }
      sched_table[i].t_rem_ -= tic_period_ms;
  }
  delay(tic_period_ms);
}


void setup() {
  sched_setup();
} 

void loop() { 
  sched_run(100);
}
