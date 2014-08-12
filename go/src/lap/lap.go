package main
import (
  "io/ioutil"
  "unicode"
  "log"
  "fmt"
  "flag"
  "regexp"
  "os/user"
)
var procDir = "/proc/"
// Format: 1 (init) S 0 1 1 0 -1 4219136 19614 33480686 ...
var restat = regexp.MustCompile(`(\d+) \((.+)\) (\w) (\d+) (\d+) (\d+) (\d+)`)
var restatus = regexp.MustCompile(`Uid:\s+(\d+)\s+(\d+)\s+(\d+)\s(\d+)`)

type ProcData struct {
        name string
        pid  string // using string to represent PID
        ppid string
        uid  string
        user string
}

func getPidEntries(procDir string) (pids []string, err error) {
        entries, err := ioutil.ReadDir(procDir)

        for _, proc := range entries {
                if unicode.IsDigit([]rune(proc.Name())[0]) {
pids = append (pids, proc.Name ())
                }
        }
        return pids, err
}

func getProcData(pid string) (procData ProcData, err error) {
        filename := procDir + pid + "/stat"
        stat, err := ioutil.ReadFile(filename)
        if err != nil {
                log.Fatal(err)
        }
        data := restat.FindStringSubmatch(string(stat))
        procData = ProcData{pid: data[1], name: data[2]}

        filename = procDir + pid + "/status"
        status, err := ioutil.ReadFile(filename)
        if err != nil {
                log.Fatal(err)
        }
        data = restatus.FindStringSubmatch(string(status))
        procData.uid = data[1]
        user, _ := user.LookupId(procData.uid)
        procData.user = user.Username

        return procData, nil
}

func main() {
        var realname = flag.Bool("r", false, "show real user name")
        flag.Parse()
        pids, err := getPidEntries(procDir)
        if err != nil {
                log.Fatal(err)
        }
        for _, pid := range pids {
                procData, _ := getProcData(pid)
                if *realname {
                        fmt.Printf("%s\t%s\t%s\n", procData.user, procData.pid, procData.name)
                } else {
                        fmt.Printf("%s\t%s\t%s\n", procData.uid, procData.pid, procData.name)
                }
        }
}
