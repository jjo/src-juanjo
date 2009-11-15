package main

import (
  "rpc";
  "log";
  "fmt";
  "server";
)

const serverAddress = "localhost"
func main() {
  client, err := rpc.DialHTTP("tcp", serverAddress + ":1234");
  if err != nil {
    log.Exit("dialing:", err);
  }
  // Synchronous call
  args := &server.Args{7, 8};
  reply := new(server.Reply);
  err = client.Call("Arith.Multiply", args, reply);
  if err != nil {
    log.Exit("arith error:", err)
  }
  fmt.Printf("Arith: %d*%d=%d", args.A, args.B, reply.C);
}


