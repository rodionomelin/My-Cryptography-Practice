package main

import (
	"bytes"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
)

// Constants for service endpoints and hosting port
const (
	Service2URL = "http://localhost:8092/encrypted"
	Service3URL = "http://localhost:8093/publickey"
	HostPort    = ":8091"
)

// Message represents a simple text message
type Message struct {
	Text string `json:"text"`
}

func encryptHandler(w http.ResponseWriter, r *http.Request) {
	// Read the incoming message
	var msg Message
	err := json.NewDecoder(r.Body).Decode(&msg)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	log.Printf("[+] Received a new message...")

	// Generate a random key with length matching the number of runes
	key := make([]byte, len(msg.Text))
	_, err = rand.Read(key)
	if err != nil {
		http.Error(w, "Failed to generate key", http.StatusInternalServerError)
		return
	}
    log.Printf("[+] Generating a new key...")

    // Get byte representation of the message
    messageBytes := []byte(msg.Text)

	 // Encrypt the message using XOR Cipher
	encryptedMsg := xorEncrypt(messageBytes, key)
	
	// Encode the key in base64
	keyBase64 := base64.StdEncoding.EncodeToString(key)

    // Send key to Service_3
	sendToService(Service3URL, []byte(keyBase64))
    log.Printf("[+] Public key sent to Service_3...")

    // Encode the encrypted message in base64
    encryptedMsgBase64 := base64.StdEncoding.EncodeToString(encryptedMsg)
	
	// Send encrypted message to Service_2
	sendToService(Service2URL, []byte(encryptedMsgBase64))
    log.Printf("[+] Encrypted message sent to Service_2...")
}

func xorEncrypt(data []byte, key []byte) []byte {
    encrypted := make([]byte, len(data))
    for i := range data {
        encrypted[i] = data[i] ^ key[i%len(key)]
    }
    return encrypted
}


func sendToService(url string, data []byte) {
	_, err := http.Post(url, "application/octet-stream", ioutil.NopCloser(bytes.NewReader(data)))
	if err != nil {
		log.Printf("Failed to send data to %s: %v\n", url, err)
	}
}

func main() {
	http.HandleFunc("/encrypt", encryptHandler)
	log.Printf("[+] Service_1 is running on port %s...\n", HostPort)
	if err := http.ListenAndServe(HostPort, nil); err != nil {
		log.Fatal(err)
	}
}