package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"sort"
	"strconv"
	"strings"
)

var _, _, _, _, _, _ = fmt.Print, ioutil.ReadFile, log.Print, strings.Trim, strconv.Atoi, sort.Ints

// AND, OR, LSHIFT, RHIFT, Not
func compute(value string, m map[string]string, cache map[string]int) int {
	if val, ok := cache[value]; ok {
		return val
	}

	num, err := strconv.Atoi(value)
	if err == nil {
		return num
	}

	var result int
	data := strings.Split(m[value], " ")
	switch {
	case len(data) == 1:
		result = compute(data[0], m, cache)
	case data[0] == "NOT":
		result = (math.MaxUint16) ^ compute(data[1], m, cache)
	case data[1] == "AND":
		result = compute(data[0], m, cache) & compute(data[2], m, cache)
	case data[1] == "OR":
		result = compute(data[0], m, cache) | compute(data[2], m, cache)
	case data[1] == "LSHIFT":
		result = compute(data[0], m, cache) << compute(data[2], m, cache)
	case data[1] == "RSHIFT":
		result = compute(data[0], m, cache) >> compute(data[2], m, cache)
	}
	cache[value] = result
	return result
}

func Part1(content string) {
	result := 0
	mapa := map[string]string{}
	cache := map[string]int{}

	splited := strings.Split(content, "\n")
	for _, str := range splited {
		if str == "" {
			continue
		}
		ope := strings.Split(str, " -> ")
		mapa[ope[1]] = ope[0]
	}

	result = compute("a", mapa, cache)
	fmt.Println(result)

	var resultPart2 int
	cache = map[string]int{}
	mapa["b"] = strconv.Itoa(result)
	resultPart2 = compute("a", mapa, cache)
	fmt.Println(resultPart2)
}

func main() {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	Part1(string(content))
}
