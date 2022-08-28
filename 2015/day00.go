package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"sort"
	"strconv"
	"strings"
)

var _, _, _, _, _, _ = fmt.Print, ioutil.ReadFile, log.Print, strings.Trim, strconv.Atoi, sort.Ints

func Part1(content string) {
	result := 0
	fmt.Println(result)
}

func Part2(content string) {
	result := 0
	fmt.Println(result)
}

func main() {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	Part1(string(content))
	Part2(string(content))
}
