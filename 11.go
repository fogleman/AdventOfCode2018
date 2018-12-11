package main

import (
	"fmt"
)

const S = 300

type Point struct {
	X, Y int
}

func summedAreaTable(serial int) []int {
	t := make([]int, (S+1)*(S+1))
	for y := 1; y <= S; y++ {
		for x := 1; x <= S; x++ {
			r := x + 10
			p := (((r*y+serial)*r)/100)%10 - 5
			i := y*S + x
			t[i] = p + t[i-1] + t[i-S] - t[i-S-1]
		}
	}
	return t
}

func regionSum(t []int, s, x, y int) int {
	x0, y0, x1, y1 := x-1, y-1, x+s-1, y+s-1
	return t[y0*S+x0] + t[y1*S+x1] - t[y0*S+x1] - t[y1*S+x0]
}

func best(t []int, s int) (int, Point) {
	var bestSum int
	var bestPoint Point
	for y := 1; y <= S-s+1; y++ {
		for x := 1; x <= S-s+1; x++ {
			r := regionSum(t, s, x, y)
			if r > bestSum {
				bestSum = r
				bestPoint = Point{x, y}
			}
		}
	}
	return bestSum, bestPoint
}

func bestAnySize(t []int) (int, int, Point) {
	var bestSum, bestSize int
	var bestPoint Point
	for s := 1; s <= S; s++ {
		sum, point := best(t, s)
		if sum > bestSum {
			bestSum = sum
			bestSize = s
			bestPoint = point
		}
	}
	return bestSize, bestSum, bestPoint
}

func main() {
	t := summedAreaTable(2694)

	_, p := best(t, 3)
	fmt.Printf("%d,%d\n", p.X, p.Y)

	s, _, p := bestAnySize(t)
	fmt.Printf("%d,%d,%d\n", p.X, p.Y, s)
}
