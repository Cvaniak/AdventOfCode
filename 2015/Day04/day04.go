package main

import (
	"crypto/md5"
	"fmt"
	"io/ioutil"
	"log"
	"sort"
	"strconv"
	"strings"
)

var _, _, _, _, _, _ = fmt.Print, ioutil.ReadFile, log.Print, strings.Trim, strconv.Atoi, sort.Ints

func Part1(content string) {
	content = strings.TrimSpace(content)
	i := 0
	for {
		hash := md5.Sum([]byte(fmt.Sprintf("%s%d", content, i)))
		if strings.HasPrefix(fmt.Sprintf("%x", hash), "00000") {
			fmt.Printf("%d\n", i)
			break
		}
		i += 1
	}
}

func Part2(content string) {
	content = strings.TrimSpace(content)
	i := 0
	for {
		hash := md5.Sum([]byte(fmt.Sprintf("%s%d", content, i)))
		if strings.HasPrefix(fmt.Sprintf("%x", hash), "000000") {
			fmt.Printf("%d\n", i)
			break
		}
		i += 1
	}
}

func main() {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	Part1(string(content))
	Part2(string(content))
}
