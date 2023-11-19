package main

import (
	"bytes"
	"log"
	"io/ioutil"
	"net/http"
)

// Constants for service endpoint and hosting port
const (
	Service3URL = "http://localhost:8093/decrypted"
	HostPort    = ":8092"
)

func encryptedHandler(w http.ResponseWriter, r *http.Request) {
	// Read the incoming encrypted message
	encryptedMsg, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Log the encrypted message
	log.Printf("[+] Received encrypted message: %s\n", string(encryptedMsg))

	// Forward the encrypted message to Service_3
	sendToService(Service3URL, encryptedMsg)
	log.Printf("[+] Encrypted message sent to Service_3...")
}

func sendToService(url string, data []byte) {
	_, err := http.Post(url, "application/octet-stream", ioutil.NopCloser(bytes.NewReader(data)))
	if err != nil {
		log.Printf("Failed to send data to %s: %v\n", url, err)
	}
}

func main() {
	http.HandleFunc("/encrypted", encryptedHandler)
	log.Printf("Service_2 is running on port %s...\n", HostPort)
	http.ListenAndServe(HostPort, nil)
}