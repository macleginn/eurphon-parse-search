package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"

	fc "macleginn/featurecounts"
)

func main() {
	// Initialise data caches
	inventories := make(map[string][]string)
	fc.UnmarshalJSONFile("inventories.json", &inventories)
	parses := make(map[string][]string)
	fc.UnmarshalJSONFile("parses_cache.json", &parses)

	// Read the input
	var op string
	fmt.Scanf("%s\n", &op)

	var target int
	fmt.Scanf("%d\n", &target)

	reader := bufio.NewReader(os.Stdin)
	inputBytes, err := reader.ReadBytes('\n')
	if err != nil {
		log.Fatal(err)
	}
	rawFeatures := []string{}
	json.Unmarshal(inputBytes, &rawFeatures)
	posFeatures := make([]string, 0)
	negFeatures := make([]string, 0)
	fc.InitialiseFeatures(rawFeatures, &posFeatures, &negFeatures)

	// Iterate over inventories and get counts
	result := []int{}
	var diff int
	for languageID, inventory := range inventories {
		count := fc.GetCountForFeatures(posFeatures, negFeatures, inventory, parses)
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
