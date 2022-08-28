package main

import (
	"fmt"
	"io/ioutil"
	"log"
)

func check(char rune) int {
	if char == '(' {
		return 1
	} else if char == ')' {
		return -1
	}
	return 0
}

func Part1() {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	a := 0
	for _, char := range string(content) {
		a += check(char)
	}
	fmt.Printf("%d", a)
}

func Part2() {
	content, err := ioutil.ReadFile("input.txt")

	if err != nil {
		log.Fatal(err)
	}
	a := 0
	for pos, char := range string(content) {
		a += check(char)
		if a < 0 {
			fmt.Printf("%d", pos)
			break
		}
	}
}

func main() {
	Part1()
	Part2()
}
