/*
 * http_server, implemented w/channels for scheduling requests
 */
package main
import (
  //"fmt";
  "http";
  "io";
  "bufio";
  "os";
)

type CRequest struct {
  conn *http.Conn;
  req *http.Request;
  rwc io.ReadWriteCloser;
  buf *bufio.ReadWriter;
}
var req_channel chan CRequest;
func CHelloServer(c chan CRequest)
{
  for {
    creq := <-c;
    creq.buf.WriteString("HTTP/1.0 200 Ok\n\n");
    creq.buf.WriteString("hello, world!\n");
    creq.buf.Flush();
    creq.rwc.Close();
  }
}
// hello world, the web server
func HelloServer(c *http.Conn, req *http.Request)
{
  var creq CRequest;
  creq.conn = c;
  creq.req = req;
  //fmt.Printf("%s\n", creq.req);
  var e os.Error;
  creq.rwc, creq.buf, e = c.Hijack();
  if (e!=nil) {}
  req_channel <- creq;
}

func main() {
  req_channel = make(chan CRequest);
  go CHelloServer(req_channel);
  http.Handle("/hello", http.HandlerFunc(HelloServer));
  err := http.ListenAndServe(":12345", nil);
  if err != nil {
   panic("ListenAndServe: ", err.String())
  }
}
