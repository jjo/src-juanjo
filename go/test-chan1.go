package main

import "fmt"

func mostrar(c chan string, sig chan bool) {
  c <- "Hello world";
  c <- "\n";
  sig <- true;
}
func main() {
  canal := make(chan string);
  signalling := make(chan bool);
  var str string;
  go mostrar(canal, signalling);
  for {
    select {
    case str = <-canal:
      fmt.Printf(str)
    case <-signalling:
      goto out
    }
  }
out:
  ;
}
