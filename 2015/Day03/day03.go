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

type Vector struct {
	X, Y float64
}

func (a Vector) Add(b Vector) Vector {
	a.X += b.X
	a.Y += b.Y
	return a
}

func (a *Vector) AddP(b Vector) *Vector {
	a.X += b.X
	a.Y += b.Y
	return a
}

func Part1(content string) {
	s, n, w, e := Vector{0, -1}, Vector{0, 1}, Vector{-1, 0}, Vector{1, 0}
	start := Vector{0, 0}
	set := map[Vector]bool{start: true}
	for _, str := range content {
		switch str {
		case '^':
			start = start.Add(n)
		case 'v':
			start = start.Add(s)
		case '>':
			start = start.Add(e)
		case '<':
			start = start.Add(w)
		}
		set[start] = true
	}

	fmt.Println(len(set))
}

func Part2(content string) {
	s, n, w, e := Vector{0, -1}, Vector{0, 1}, Vector{-1, 0}, Vector{1, 0}
	santa := Vector{0, 0}
	robot := Vector{0, 0}
	set := map[Vector]bool{santa: true}
	for ind, str := range content {
		start := &santa
		if ind%2 == 1 {
			start = &robot
		}
		switch str {
		case '^':
			start = start.AddP(n)
		case 'v':
			start = start.AddP(s)
		case '>':
			start = start.AddP(e)
		case '<':
			start = start.AddP(w)
		}
		set[*start] = true
	}

	fmt.Println(len(set))
}

func main() {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	Part1(string(content))
	Part2(string(content))
}
