package main

import (
  "fmt"
  "strings" // Fields(s string) []string
  "os"
)


func WordCount(s string) map[string] int {
  ret := make(map[string] int)
  str_array := strings.Fields(s)
  for _,word:= range(str_array) {
    ret[word]++
  }
  return ret
}

func main() {
  buf := make([]byte, 1024)
  os.Stdin.Read(buf)
  fmt.Printf("%v\n", WordCount(string(buf)))
}
