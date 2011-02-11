package main
import (
  "fmt"
)

func Cubert(x complex128) complex128 {
  z:=x/3
  prev_z := z
  for i:=0; i<1000;i++ {
    prev_z, z = z, z - (z*z*z - x)/2/z/z
    if (prev_z == z ) { break }
  }
  return z
}

func main() {
  v := (1+1i)
  fmt.Println(Cubert(v))
}
