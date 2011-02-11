package main

import (
	"os"
	"strconv"
	"fmt"
	"math"
)

// z=z-(x*x-2)/2z
func Sqrt(x float64) float64 {
  if (x<0.0) {
    panic("negative x")
  }
  z:=x
  for prev_z:=z/2; math.Fabs((prev_z-z)/z)>1E-9; {
    prev_z, z=z,z-(z*z-x)/(2*z)
    fmt.Printf("%e\r", z)
  }
  return z
}


func main() {
  f,_:=strconv.Atof64(os.Args[1])
  ret := Sqrt(f)
  fmt.Printf ("%e %e\n",f, ret);
}
