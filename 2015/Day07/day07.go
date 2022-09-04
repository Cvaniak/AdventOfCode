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

type Operation struct {
    Dest string
    What string
    V1 string
    V2 string
	Shift int
}


// AND, OR, LSHIFT, RHIFT, Not
func parse(line string) Operation{
	splited := strings.Split(line, " ")
    var result Operation
    if splited[0] == "NOT" {
       result = Operation{splited[3], "NOT", splited[1], "", 0}
       return result
    } 
    if len(splited) == 3 {
        x, err := strconv.Atoi(splited[0])
        if err != nil {
            
            result = Operation{splited[2], "MAP", splited[0], "", 0}
        } else{

            result = Operation{splited[2], "NUM", "", "", x}
        }
    }
    switch splited[1] {
    case "AND": 
        result = Operation{splited[4], splited[1], splited[0], splited[2], 0}
    case "OR":
        result = Operation{splited[4], splited[1], splited[0], splited[2], 0}
    case "LSHIFT":
        x, _ := strconv.Atoi(splited[2])
        result = Operation{splited[4], splited[1], splited[0], "", x}
    case "RSHIFT":
        x, _ := strconv.Atoi(splited[2])
        result = Operation{splited[4], splited[1], splited[0], "", x}
    }
 
    return result
}

func compute(value string, m map[string]Operation, cache map[string]int) int{
    if val, ok := cache[value]; ok {
        return val
    }

    what := m[value]
    x, err1 := strconv.Atoi(what.V1)
    if err1 != nil {
        x = compute(what.V1, m, cache)
    }
    result := -1
    switch what.What {
        case "MAP":
            result = compute(what.V1, m, cache)
        case "NUM":
            result = what.Shift
        case "NOT":
            result =  (math.MaxUint16)^x
        case "AND":
            y, err2 := strconv.Atoi(what.V2)
            if err2 != nil {
                y = compute(what.V2, m, cache)
            }
            result = x&y
        case "OR":
            y, err2 := strconv.Atoi(what.V2)
            if err2 != nil {
                y = compute(what.V2, m, cache)
            }
            result = x|y
        case "LSHIFT":
            result = x<<what.Shift
        case "RSHIFT":
            result = x>>what.Shift
    }
    cache[value] = result
    return result
}
    


func Part1(content string) {
	result := 0
	splited := strings.Split(content, "\n")
    mapa := map[string]Operation{}
    cache := map[string]int{}


	for _, str := range splited {
        if str == "" {
            continue
        }
        ope := parse(str)
        mapa[ope.Dest] = ope
    }

    result = compute("a", mapa, cache)
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
