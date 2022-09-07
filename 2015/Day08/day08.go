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
	// \" \\ \x00
	result := 0

	splited := strings.Split(content, "\n")
	for _, str := range splited {
		if str == "" {
			continue
		}
		i := 0
		n := len(str)
		for i < n {
			if str[i] == '\\' {
				switch str[i+1] {
				case '"':
					result += 1
					i += 1
				case '\\':
					result += 1
					i += 1
				case 'x':
					result += 3
					i += 3
				}
			}
			i += 1
		}
		result += 2
	}

	fmt.Println(result)
}

func Part2(content string) {
	result := 0

	splited := strings.Split(content, "\n")
	for _, str := range splited {
		if str == "" {
			continue
		}
		i := 0
		n := len(str)
		for i < n {
			if str[i] == '\\' {
				switch str[i+1] {
				case '"':
					result += 2
					i += 1
				case '\\':
					result += 2
					i += 1
				case 'x':
					result += 1
					i += 3
				}
			}
			i += 1
		}
		result += 4
	}

	fmt.Println(result)
}

func main() {
	content, err := ioutil.ReadFile("input1.txt")
	if err != nil {
		log.Fatal(err)
	}
	Part1(string(content))
	Part2(string(content))
}
