package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"sort"
	"strconv"
	"strings"
)

var _, _, _ = fmt.Print, ioutil.ReadFile, log.Print

func Part1(content string) {
	result := 0

	splited := strings.Split(content, "\n")
	ints := make([]int, 3)

	for _, char := range splited {
		if char == "" {
			continue
		}

		three := strings.Split(char, "x")
		for ind, str := range three {
			num, err := strconv.Atoi(str)
			if err != nil {
				continue
			}
			ints[ind] = num
		}

		ints[0], ints[1], ints[2] = ints[0]*ints[1], ints[1]*ints[2], ints[2]*ints[0]

		sort.Ints(ints)
		result += ints[0] + 2*(ints[0]+ints[1]+ints[2])
	}

	fmt.Println(result)
}

func Part2(content string) {
	result := 0

	splited := strings.Split(content, "\n")
	ints := make([]int, 3)

	for _, char := range splited {
		if char == "" {
			continue
		}

		three := strings.Split(char, "x")
		for ind, str := range three {

			num, err := strconv.Atoi(str)
			if err != nil {
				continue
			}

			ints[ind] = num
		}

		sort.Ints(ints)
		result += 2*(ints[0]+ints[1]) + ints[0]*ints[1]*ints[2]
	}

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
