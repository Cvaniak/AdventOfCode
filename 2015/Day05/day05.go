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

var naughty_strings = []string{"ab", "cd", "pq", "xy"}
var vowels = []string{"a", "e", "i", "o", "u"}

func check_double(content string) bool {
	last := '0'
	for _, str := range content {
		if str == last {
			return true
		}
		last = str
	}
	return false
}

func Part1(content string) {
	result := 0
	splited := strings.Split(content, "\n")
	for _, str := range splited {
		c := 0
		for _, vowel := range vowels {
			counted := strings.Count(str, vowel)
			if counted > 0 {
				c += counted
			}
		}
		if c < 3 {
			continue
		}
		if check_double(str) == false {
			continue
		}

		is_naughty := false
		for _, substring := range naughty_strings {
			if strings.Contains(str, substring) {
				is_naughty = true
				break
			}
		}
		if is_naughty {
			continue
		}

		result++

	}

	fmt.Println(result)
}

func Part2(content string) {
	result := 0
	splited := strings.Split(content, "\n")
	for _, str := range splited {
		is_r := false
		for i := 0; i < len(str)-2; i++ {
			if str[i] == str[i+2] {
				is_r = true
				break
			}
		}
		if is_r == false {
			continue
		}

		m := map[string]int{}
		has_rep := false
		for i := 0; i < len(str)-1; i++ {
			s := fmt.Sprintf("%c%c", str[i], str[i+1])
			if val, ok := m[s]; ok {
				if val+1 != i {
					has_rep = true
					break
				}
			}
			m[s] = i
		}
		if has_rep == false {
			continue
		}
		result++
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
