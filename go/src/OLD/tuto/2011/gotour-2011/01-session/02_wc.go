package main

import (
  //"fmt"
  "strings"
  "tour/wc"
)
func WordCount(s string) map[string]int {
  m:=make(map[string] int)
  for _,i:=range strings.Fields(s) {
    m[i]++
  }
  return m
}
func main() {
  wc.Serve(WordCount) // http://localhost:4000/
  //w := "foo bar foo foo baz"
  //fmt.Println(WordCount(w))
}
