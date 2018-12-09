package main

import "fmt"

type Node struct {
	Value      int
	Prev, Next *Node
}

func (prev *Node) Insert(value int) *Node {
	next := prev.Next
	node := &Node{value, prev, next}
	prev.Next, next.Prev = node, node
	return node
}

func (n *Node) Remove() *Node {
	next, prev := n.Next, n.Prev
	prev.Next, next.Prev = next, prev
	return next
}

func run(numPlayers, numMarbles int) int {
	node := &Node{}
	node.Prev, node.Next = node, node
	players := make([]int, numPlayers)
	for i := 1; i <= numMarbles; i++ {
		if i%23 == 0 {
			for j := 0; j < 7; j++ {
				node = node.Prev
			}
			players[i%numPlayers] += i + node.Value
			node = node.Remove()
		} else {
			node = node.Next.Insert(i)
		}
	}
	max := players[0]
	for _, p := range players {
		if p > max {
			max = p
		}
	}
	return max
}

func main() {
	fmt.Println(run(419, 71052))
	fmt.Println(run(419, 71052*100))
}
