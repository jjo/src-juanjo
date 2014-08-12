package main

import (
  "fmt"
  "tour/pic"
)

func Pic(dx, dy int) [][]uint8 {
  ret := make([][]uint8, dy)
  for i:=0; i<dy; i++ {
    ret[i] = make([]uint8, dx)
    for j:=0; j<dx; j++ {
      //ret[i][j] = uint8((i*j))
      ret[i][j] = uint8((i^j))
    }
  }
  return ret
}


func main() {
  fmt.Println(Pic(4,5))
  pic.Serve(Pic)
}
