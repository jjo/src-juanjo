/*
 * create 100000 channels, pass 1char around
 */
package main

import "fmt"

func tubito(entrada, salida chan int) { salida <- 1+<-entrada }
func main() {
  var izq, der chan int;
  izq_1 := make(chan int);
  der = izq_1;
  for i := 0; i < 100000; i++ {
    izq, der = der, make(chan int);
    go tubito(izq, der);
  }
  izq_1 <- 0;
  fmt.Printf("val=%d\n", <-der);
}
