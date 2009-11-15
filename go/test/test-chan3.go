/*
 * producers-workers-consumer(s) test
 */
package main

import (
  "fmt";
  "flag";
)

const W = 2
const P = 100
const N_total_req = 1000000

var wFlag = flag.Int("w", W, `number of workers`)
var pFlag = flag.Int("p", P, `number of producers`)
var nFlag = flag.Int("n", N_total_req, `number of total requests`)

type Item struct {
  data, control int;
}

func worker(entrada chan Item, salida chan Item) {
  var data Item;
  for {
    data = <-entrada;
    data.data++;
    salida <- data;
  }
}
func producer(salida chan Item) {
  for i := 0; i < *nFlag/(*pFlag); i++ {
    data := new(Item);
    data.data = i;
    salida <- *data;
  }
  var data_end Item;
  data_end.control = 1;
  salida <- data_end;
}
func consumer(entrada chan Item) int {
  num_done := 0;
  num_reqs := 0;
  for {
    data := <-entrada;
    if data.control == 0 {
      num_reqs++
    } else {
      num_done++;
      if num_done == *pFlag {
        break
      }
    }
  }
  return num_reqs;
}
func main() {
  flag.Parse();
  prod_c := make(chan Item);
  cons_c := make(chan Item);
  for i := 0; i < *wFlag; i++ {
    go worker(prod_c, cons_c)
  }
  for i := 0; i < *pFlag; i++ {
    go producer(prod_c)
  }
  total_reqs := consumer(cons_c);
  fmt.Printf("total_reqs=%d\n", total_reqs);
}
