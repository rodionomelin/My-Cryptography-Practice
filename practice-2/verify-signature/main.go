package main

import (
    "fmt"
    "math/big"
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "net/http"
)

const (
    HostPort = ":8092"
)

// hashFunction computes the SHA-256 hash of a message.
func hashFunction(message string) string {
    hasher := sha256.New()
    hasher.Write([]byte(message))
    return hex.EncodeToString(hasher.Sum(nil))
}

// Function to verify a signature
func verifySignature(hashedMessageInt *big.Int, signature *big.Int, e *big.Int, n *big.Int) bool {
    // Decrypt the signature with the public key (decryptedSignature = signature^e mod n)
    decryptedSignature := new(big.Int).Exp(signature, e, n)

    // Compare the decrypted signature with the hashed message
    return hashedMessageInt.Cmp(decryptedSignature) == 0
}

// HTTP handler function for signature verification
func handleVerifySignature(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var request struct {
        N          string `json:"n"`
        E          string `json:"e"`
        MessageInt string `json:"messageInt"`
        Signature  string `json:"signature"`
    }

    // Decode JSON body
    err := json.NewDecoder(r.Body).Decode(&request)
    if err != nil {
        http.Error(w, "Error parsing request body", http.StatusBadRequest)
        return
    }

    // Convert string values to *big.Int
    n := new(big.Int)
    n.SetString(request.N, 10)
    e := new(big.Int)
    e.SetString(request.E, 10)
    messageInt := new(big.Int)
    messageInt.SetString(request.MessageInt, 10)
    signature := new(big.Int)
    signature.SetString(request.Signature, 10)

    // Verify the signature
    isValid := verifySignature(messageInt, signature, e, n)

    // Create and send JSON response
    response := struct {
        Valid bool `json:"valid"`
    }{
        Valid: isValid,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/verify-signature", handleVerifySignature)
    fmt.Printf("Server starting on %s\n", HostPort)
    err := http.ListenAndServe(HostPort, nil)
    if err != nil {
        fmt.Println("Error starting server:", err)
    }
}