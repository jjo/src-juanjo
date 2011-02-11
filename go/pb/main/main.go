package main
import (
  "bytes"
  "log"
	"goprotobuf.googlecode.com/hg/proto"
  "prueba/pb/http"
)
func main() {
  request := &http.Request {
    Type: http.NewTYPE(http.TYPE_POST),
    Path: proto.String("hello"),
  }
  buf := new(bytes.Buffer)
  proto.CompactText(buf, request);
  log.Stdout(buf.String());
  log.Exit("Ouch");
}
