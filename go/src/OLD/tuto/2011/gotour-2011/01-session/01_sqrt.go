package main
import (
  "fmt"
)

func Sqrt(x float64) float64 {
  z:=x/2
  prev_z := z
  for i:=0; i<1000;i++ {
    prev_z, z = z, z - (z*z - x)/2/x
    if (prev_z == z ) { break }
  }
  return z
}

func main() {
  v := 10000.0
  fmt.Println(Sqrt(v))
}
