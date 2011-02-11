package main

import "fmt"

type NameAge struct {
  Name string
  Age int
}


func (p *NameAge) Get() (string, int) {
  return p.Name, p.Age
}
func (p *NameAge) Set(name string, age int) {
  p.Name, p.Age = name, age
}

type GSeter interface {
  Get()(string, int)
  Set(string, int)()
}

type GenteDb struct {
  d map[string]*NameAge
}

func NewGenteDb () (db *GenteDb) {
  db = new(GenteDb)
  db.d = make(map[string]*NameAge)
  return
}
func (p *GenteDb) AddEntry(e *NameAge)() {
  p.d[e.Name]=e
}

func (p *GenteDb) GetEntry(q *NameAge)(e *NameAge) {
  return p.d[q.Name]
}
func (p *GenteDb) Dump() () {
  for _,e:=range p.d {
    fmt.Println(*e)
  }
}

type DbManager interface {
  AddEntry(*NameAge)()
  GetEntry()(*NameAge)
  Dump()
}

func main() {
  jjo :=NameAge{"jjo", 43 }
  clau :=NameAge{"clau", 44 }
  paio :=&NameAge{"pablo", 14}
  db := NewGenteDb()
  db.AddEntry(&jjo)
  db.AddEntry(&clau)
  db.AddEntry(paio)
  db.Dump()
  return
}
