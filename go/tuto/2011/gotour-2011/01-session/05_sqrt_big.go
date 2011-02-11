package main
import (
  "fmt"
  "big"
)

const (
  resol = 50
)

func Sqrt(x *big.Rat) *big.Rat {
  var prev_z, z, new_z big.Rat
  two := big.NewRat(2,1)
  z.Quo(x,two)
  for i:=0; i<10000;i++ {
    prev_z.Set(&z)
    new_z.Mul(&z, &z)
    new_z.Sub(&new_z, x)
    new_z.Quo(&new_z, two)
    new_z.Quo(&new_z, &z)
    z.Sub(&z, &new_z)
    if z.Cmp(&prev_z) == 0 {
      break
    }
    fmt.Println(z.FloatString(60))

     //z - (z*z - x)/2/x
  }
  return &z
}

func main() {
  v := big.NewRat(10000,1)
  fmt.Println(Sqrt(v).FloatString(10))
}
