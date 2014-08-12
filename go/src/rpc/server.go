package server

import "os"

type Args struct {
  A, B int
}

type Reply struct {
  C int
}

type Arith int

func (t *Arith) Multiply(args *Args, reply *Reply) os.Error {
  reply.C = args.A * args.B;
  return nil
}

func (t *Arith) Divide(args *Args, reply *Reply) os.Error {
  if args.B == 0 {
    return os.ErrorString("divide by zero");
  }
  reply.C = args.A / args.B;
  return nil
}

