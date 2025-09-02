package main

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"math/big"
)

const HASHTABLEBUCKETS = 16 // The number of buckets for a hash table

type Node[V any] struct {
	key   []byte
	value V
}

type HashTable[V any] struct {
	buckets [HASHTABLEBUCKETS][]Node[V]
}

func (h *HashTable[V]) find(key []byte) (*V, bool) {
	// 1. Generate a hash of the key
	hash := sha256.Sum256(key) // The initial hash produced
	digestInt := new(big.Int).SetBytes(hash[:])

	// 2. Convert to an index by doing a modulo by 16
	searchIndex := int(new(big.Int).Mod(digestInt, big.NewInt(16)).Int64())

	// 3. Look through the bucket at the generated index
	if h.buckets[searchIndex] != nil {
		for _, n := range h.buckets[searchIndex] {
			// 4. If key matches the key we're looking for, return the value
			if bytes.Equal(n.key, key) {
				return &n.value, true
			}
		}
	}
	return nil, false
}

func (h *HashTable[V]) add(key []byte, value V) *error {
	// 1. Generate a hash of the key
	hash := sha256.Sum256(key)
	digestInt := new(big.Int).SetBytes(hash[:]) // Convert hash to big.Int

	// 2. Convert to an index by doing a modulo by 16
	insertIndex := int(new(big.Int).Mod(digestInt, big.NewInt(16)).Int64())

	// 3. Insert into specified bucket
	if h.buckets[insertIndex] == nil {
		// If no array exists at the bucket, initialize array, and push Node onto it
		h.buckets[insertIndex] = make([]Node[V], 0)
		h.buckets[insertIndex] = append(h.buckets[insertIndex], Node[V]{key: key, value: value})
	} else {
		// If array exists at the bucket
		// Start by looking if it's a duplicate, and overriding existing node if it is
		isDuplicate := false
		for keyIndex, n := range h.buckets[insertIndex] {
			if bytes.Equal(n.key, key) {
				isDuplicate = true
				h.buckets[insertIndex][keyIndex] = Node[V]{key: key, value: value}
			}
		}
		// If the Key is not in the current bucket, add a new Node of the key-value pair
		if !isDuplicate {
			h.buckets[insertIndex] = append(h.buckets[insertIndex], Node[V]{key: key, value: value})
		}
	}
	return nil
}

func main() {
	tes := HashTable[string]{}

	tes.add([]byte("key1"), "value 1")
	// fmt.Printf("%v\n", tes)
	tes.add([]byte("key2"), "value 2") // colides with 34
	// fmt.Printf("%v\n", tes)
	tes.add([]byte("key1"), "value 3")
	// fmt.Printf("%v\n", tes)
	tes.add([]byte("key10"), "value 10")
	tes.add([]byte("key20"), "value 20")
	tes.add([]byte("key30"), "value 30")
	tes.add([]byte("key11"), "value 11") // colides with 13
	tes.add([]byte("key21"), "value 21") // colides with 22 and 24
	tes.add([]byte("key31"), "value 31")
	tes.add([]byte("key12"), "value 12") // colides with 33
	tes.add([]byte("key22"), "value 22") // colides with 21 and 24
	tes.add([]byte("key32"), "value 32")
	tes.add([]byte("key13"), "value 13") // colides with 11
	tes.add([]byte("key23"), "value 23")
	tes.add([]byte("key33"), "value 33") // colides with 12
	tes.add([]byte("key14"), "value 14")
	tes.add([]byte("key24"), "value 24") // colides with 21 and 22
	tes.add([]byte("key34"), "value 34") // colides with 2
	fmt.Printf("%+v\n\n", tes)

	for index, val := range tes.buckets {
		fmt.Printf("Bucket #%d: %s\n", index, val)
	}

	for _, testCase := range [][]byte{[]byte("key1"), []byte("key2"), []byte("key3"), []byte("key11"), []byte("key13")} {
		v, isPresent := tes.find(testCase)
		if isPresent {
			fmt.Printf("%v\n", *v)
		} else {
			fmt.Printf("Test case %s is not present\n", testCase)
		}
	}

}
