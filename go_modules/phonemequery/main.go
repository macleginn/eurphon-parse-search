package main

import (
	"encoding/json"
	"fmt"
	"log"
	"strconv"

	fc "macleginn/featurecounts"
)

// Returns 1 if the phoneme is found in the inventory and 0 otherwise.
func getCountForPhoneme(phoneme string, inventory []string) (result int) {
	result = 0
	for _, segment := range inventory {
		if segment == phoneme {
			result = 1
			break // We do not expect to meet a phoneme twice in an inventory.
		}
	}
	return
}

func main() {
	inventories := make(map[string][]string)
	fc.UnmarshalJSONFile("inventories.json", &inventories)

	// Read the input
	var op string
	fmt.Scanf("%s\n", &op)

	var target int
	fmt.Scanf("%d\n", &target)

	var phoneme string
	fmt.Scanf("%s\n", &phoneme)

	// Iterate over inventories
	result := []int{}
	var diff int
	for languageID, inventory := range inventories {
		count := getCountForPhoneme(phoneme, inventory)
		diff = count - target
		if fc.CheckDiff(op, diff) {
			intID, err := strconv.Atoi(languageID)
			if err != nil {
				log.Fatal(err)
			}
			result = append(result, intID)
		}
	}
	output, err := json.Marshal(result)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(output))
}
