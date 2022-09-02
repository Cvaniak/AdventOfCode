package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"sort"
	"strconv"
	"strings"
	"math"
)

var _, _, _, _, _, _ = fmt.Print, ioutil.ReadFile, log.Print, strings.Trim, strconv.Atoi, sort.Ints

// toggle on off
func parse(line string) []int{
	splited := strings.Split(line, " ")
    values_ind := 1
    on_off := 0
    if splited[0] == "toggle" {
       
    } else {
        values_ind ++
        if splited[1] == "on" {
            on_off = 1
        } else {
            on_off = 2
        }

    }
    a := strings.Split(splited[values_ind], ",")
    b := strings.Split(splited[values_ind+2], ",")
    x1, _ := strconv.Atoi(a[0])
    y1, _ := strconv.Atoi(a[1])
    x2, _ := strconv.Atoi(b[0])
    y2, _ := strconv.Atoi(b[1])
 
    return []int{on_off, x1, y1, x2, y2}
}

func Part1(content string) {
	result := 0

	splited := strings.Split(content, "\n")
    var mat [1000000]bool

	
	for _, str := range splited {
        if str == "" {
            continue
        }
        list := parse(str)
		for i := list[1]; i <= list[3]; i++ {
            for j := list[2]; j <= list[4]; j++ {
                switch list[0] {
                case 0:
                    mat[i*1000 + j] = !mat[i*1000 + j] 
                case 1:
                    mat[i*1000 + j] = true
                case 2:
                    mat[i*1000 + j] = false
                }
            }
        }
    }
    for _, i := range mat {
        if i {
            result ++ 
        }
    }

	fmt.Println(result)
}

func Part2(content string) {
	result := 0.0

	splited := strings.Split(content, "\n")
    var mat [1000000]float64

	
	for _, str := range splited {
        if str == "" {
            continue
        }
        list := parse(str)
		for i := list[1]; i <= list[3]; i++ {
            for j := list[2]; j <= list[4]; j++ {
                switch list[0] {
                case 0:
                    mat[i*1000 + j] += 2  
                case 1:
                    mat[i*1000 + j] += 1
                case 2:
                    mat[i*1000 + j] = math.Max(0.0, mat[i*1000 + j] - 1)
                }
            }
        }
    }
    for _, i := range mat {
        result += i
    }

    fmt.Printf("%f\n", result)
}

func main() {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	Part1(string(content))
	Part2(string(content))
}
