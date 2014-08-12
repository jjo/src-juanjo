package main

import (
  "rpc"
  "net"
  "log"
  "http"
  "./server"
)

func main() {
  arith := new(server.Arith);
  rpc.Register(arith);
  rpc.HandleHTTP();
  l, e := net.Listen("tcp", ":1234");
  if e != nil {
          log.Exit("listen error:", e);
  }
  http.Serve(l, nil);
}

