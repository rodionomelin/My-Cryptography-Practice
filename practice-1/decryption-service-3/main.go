package main

import (
	"encoding/base64"
	"io/ioutil"
	"log"
	"net/http"
)

// Constant for hosting port
const HostPort = ":8093"

var key []byte

func decryptedHandler(w http.ResponseWriter, r *http.Request) {
    // Check if the key has been set
    if len(key) == 0 {
        log.Println("No key available for decryption")
        http.Error(w, "No key available", http.StatusInternalServerError)
        return
    }

    // Read the incoming encrypted message (base64 encoded)
    encryptedMsgBase64, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // Decode the message from base64
    encryptedMsg, err := base64.StdEncoding.DecodeString(string(encryptedMsgBase64))
    if err != nil {
        http.Error(w, "Failed to decode base64 message", http.StatusBadRequest)
        return
    }

    // Ensure the key and message lengths match
    if len(encryptedMsg) != len(key) {
        log.Println("Key and message length do not match")
        http.Error(w, "Invalid key length", http.StatusInternalServerError)
        return
    }

     // Decrypt the message using the XOR Cipher
	 decryptedBytes := xorDecrypt(encryptedMsg, key)
	 decryptedMsg := string(decryptedBytes)
    log.Printf("[+] Decrypted message: %s\n", decryptedMsg)
}


func publicKeyHandler(w http.ResponseWriter, r *http.Request) {
	// Read the incoming key
	keyBase64, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Decode the key from base64
	key, err = base64.StdEncoding.DecodeString(string(keyBase64))
	if err != nil {
		http.Error(w, "Failed to decode base64 key", http.StatusBadRequest)
		return
	}

	log.Printf("[+] Received key for decryption\n")
}

func xorDecrypt(encryptedBytes []byte, key []byte) []byte {
    decrypted := make([]byte, len(encryptedBytes))
    for i := range encryptedBytes {
        decrypted[i] = encryptedBytes[i] ^ key[i%len(key)]
    }
    return decrypted
}


func main() {
	http.HandleFunc("/decrypted", decryptedHandler)
	http.HandleFunc("/publickey", publicKeyHandler)
	log.Printf("[+] Service_3 is running on port %s...\n", HostPort)
	if err := http.ListenAndServe(HostPort, nil); err != nil {
		log.Fatal(err)
	}
}