package featurecounts

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

//
// Various utility functions
//

// UnmarshalJSONFile imports a string -> string map from a file.
func UnmarshalJSONFile(path string, target *map[string][]string) {
	fileReader, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer fileReader.Close()

	dataBytes, err := ioutil.ReadAll(fileReader)
	if err != nil {
		log.Fatal(err)
	}

	json.Unmarshal(dataBytes, target)
}

// InitialiseFeatures separates an array of +A, -B features into
// two string slices.
func InitialiseFeatures(rawFeatures []string, posFeatures *[]string, negFeatures *[]string) {
	for _, feature := range rawFeatures {
		trimmedFeature := strings.Trim(feature, "+-")
		if strings.HasPrefix(feature, "+") {
			*posFeatures = append(*posFeatures, trimmedFeature)
		} else {
			*negFeatures = append(*negFeatures, trimmedFeature)
		}
	}
}

// CheckDiff checks that the query condition
// holds for the inventory.
func CheckDiff(op string, diff int) bool {
	switch op {
	case "=":
		return diff == 0
	case "<":
		return diff < 0
	case "<=":
		return diff <= 0
	case ">":
		return diff > 0
	case ">=":
		return diff >= 0
	default:
		log.Fatal(fmt.Sprintf("Comparison operator not recognised: %s", op))
	}
	// Unreachable
	return false
}

// This will run in 0(1) since parses are always short
// and have a fixed maximum length.
func contains(slice []string, element string) bool {
	for _, s := range slice {
		if s == element {
			return true
		}
	}
	return false
}

// GetCountForFeatures returns the number of segments from
// a give inventory possessing all posFeatures and not
// possessing any negFeatures.
func GetCountForFeatures(
	posFeatures []string,
	negFeatues []string,
	inventory []string,
	parses map[string][]string) (result int) {
	result = 0
	parse := []string{}
	var skipThis bool
	var f string
	for _, segment := range inventory {
		parse = parses[segment]
		skipThis = false
		for _, f = range negFeatues {
			if contains(parse, f) {
				skipThis = true
				break
			}
		}
		if skipThis {
			continue
		}
		for _, f = range posFeatures {
			if !contains(parse, f) {
				skipThis = true
				break
			}
		}
		if skipThis {
			continue
		}
		result++
	}
	return
}
