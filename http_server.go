package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"
)

const INFO_FILE = "/tmp/aws_stats.py"
const RDS_INFO_FILE = "/tmp/rds_stats.py"
const EC2_INFO_FILE = "/tmp/ec2_stats.py"

func getInfo(filename string) string {
	s, _ := ioutil.ReadFile(filename)
	return string(s)
}

func printEC2info(w http.ResponseWriter, r *http.Request) {
	cmd := exec.Command("/usr/bin/python", "/usr/local/bin/aws_stats.py")
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		log.Fatal(err)
	}

	err = ioutil.WriteFile(INFO_FILE, []byte(out.String()), 0644)
	if err != nil {
		log.Fatal(err)
	}

	// read file
	fmt.Fprintf(w, getInfo(INFO_FILE))
}

func printRDSstat(w http.ResponseWriter, r *http.Request) {
        cmd := exec.Command("/usr/bin/python", "/usr/local/bin/rds_stats.py")
        var out bytes.Buffer
        cmd.Stdout = &out
        err := cmd.Run()
        if err != nil {
                log.Fatal(err)
        }

        err = ioutil.WriteFile(RDS_INFO_FILE, []byte(out.String()), 0644)
        if err != nil {
                log.Fatal(err)
        }

        // read file
        fmt.Fprintf(w, getInfo(RDS_INFO_FILE))
}

func printEC2stat(w http.ResponseWriter, r *http.Request) {
        cmd := exec.Command("/usr/bin/python", "/usr/local/bin/ec2_stats.py")
        var out bytes.Buffer
        cmd.Stdout = &out
        err := cmd.Run()
        if err != nil {
                log.Fatal(err)
        }

        err = ioutil.WriteFile(EC2_INFO_FILE, []byte(out.String()), 0644)
        if err != nil {
                log.Fatal(err)
        }

        // read file
        fmt.Fprintf(w, getInfo(EC2_INFO_FILE))
}
func main() {

	http.HandleFunc("/", printEC2info)
	http.HandleFunc("/rds", printRDSstat)
	http.HandleFunc("/ec2", printEC2stat)
	err := http.ListenAndServe(":80", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
