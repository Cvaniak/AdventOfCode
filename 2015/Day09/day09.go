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

var _, _, _, _, _, _, _ = fmt.Print, ioutil.ReadFile, log.Print, strings.Trim, strconv.Atoi, sort.Ints, math.Max
type Pair struct {
    ci1 string
    ci2 string
}
var mapa = map[Pair]float64{}
var result []float64

func Foo(cityA string, value float64, been map[string]bool){
    any := true
    for cityB, elem := range been {
        if !elem{
            continue
        }
        any = false
        been[cityB] = false
        Foo(cityB, value+mapa[Pair{cityA, cityB}], been)
        been[cityB] = true
    }
    if any {
        result = append(result, value)
    }
}

func Part1And2(content string) {
 	// mapa := map[string]map[string]int{}
    been := map[string]bool{}

	splited := strings.Split(content, "\n")
	for _, str := range splited {
		if str == "" {
			continue
		}
		data := strings.Split(str, " = ")
        distance := data[1]
        cities := strings.Split(data[0], " to ")

        num, err := strconv.Atoi(distance)
        if err != nil {
            fmt.Println("Error")
        }
        been[cities[0]] = true
        been[cities[1]] = true
        mapa[Pair{cities[0], cities[1]}] = float64(num)
        mapa[Pair{cities[1], cities[0]}] = float64(num)
        // mapa[cities[1]][cities[0]] = num
	}

    for key, _ := range been {
        been[key] = false
        Foo(key, 0.0, been)
        been[key] = true
    }

    mn := result[0]
    mx := result[0]
	for _, value := range result{
		if value < mn {
			mn = value
		}
		if value > mx {
			mx = value
		}
	}

	fmt.Println(mn)
	fmt.Println(mx)
	// fmt.Println(result)
}

func main() {
	content, err := ioutil.ReadFile("input1.txt")
	if err != nil {
		log.Fatal(err)
	}
	Part1And2(string(content))
}
