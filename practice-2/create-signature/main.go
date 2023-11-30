package main

import (
    "encoding/json"
    "fmt"
    "math/big"
    "net/http"
    "crypto/sha256"
    "crypto/rand"
    "encoding/hex"
    "io/ioutil"
)

const (
    HostPort = ":8091"
)

// Simplified RSA structure
type RSAKey struct {
    // n = p * q
    // Part of both the public and private keys        
    n *big.Int    
    // Public exponent
    e *big.Int 
    // Private exponent
    d *big.Int 
}

func generateLargePrime(bits int) (*big.Int, error) {
    prime, err := rand.Prime(rand.Reader, bits)
    if err != nil {
        // Return the error to the caller
        return nil, err
    }
    return prime, nil
}

func generateRSAKeys(bitSize int) RSAKey {
    // Generate two large primes, p and q
    p, err := generateLargePrime(bitSize / 2)
    if err != nil {
        fmt.Println("Failed to generate a large prime:", err)
    }
    q, err := generateLargePrime(bitSize / 2 )
    if err != nil {
        fmt.Println("Failed to generate a large prime:", err)
    }

    // Calculate n = p * q
    n := new(big.Int).Mul(p, q)

    // Calculate phi(n) = (p-1) * (q-1)
    phi := new(big.Int).Mul(new(big.Int).Sub(p, big.NewInt(1)), new(big.Int).Sub(q, big.NewInt(1)))

    
    // Choose e, 65537 is commonly used as a public exponent in the RSA cryptosystem. 65537 is a Fermat prime.
    e := big.NewInt(65537)

    // Calculate d, the modular inverse of e mod phi(n)
    d := new(big.Int).ModInverse(e, phi)
    if d == nil {
        panic("ModInverse failed")
    }

    return RSAKey{n, e, d}
}


// hashFunction computes the SHA-256 hash of a message.
func hashFunction(message string) string {
    hasher := sha256.New()
    hasher.Write([]byte(message))
    return hex.EncodeToString(hasher.Sum(nil))
}

// Function to create a signature
func createSignature(message string, privateKey RSAKey) (*big.Int, *big.Int) {
    // Hash the message
    hashedMessage := hashFunction(message)

    // Convert the hashed message to a big integer
    messageInt := new(big.Int)

    // Assuming the hash is in hexadecimal
    messageInt.SetString(hashedMessage, 16) 

    // Encrypt the hash with the private key (signature = message^d mod n)
    signature := new(big.Int).Exp(messageInt, privateKey.d, privateKey.n)
    return signature, messageInt
}

// HTTP handler function
func handleSignature(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    // Read message from request body
    body, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error reading request body", http.StatusInternalServerError)
        return
    }
    message := string(body)

    // Generate keys and signature
    rsaKey := generateRSAKeys(2048)
    // If needed can be manually set.
    
    signature, messageInt := createSignature(message, rsaKey)

    // Create response object
    response := struct {
        N          string `json:"n"`
        E          string `json:"e"`
        MessageInt string `json:"messageInt"`
        Signature  string `json:"signature"`
    }{
        N:          rsaKey.n.String(),
        E:          rsaKey.e.String(),
        MessageInt: messageInt.String(),
        Signature:  signature.String(),
    }

    // Write JSON response
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    // Set up HTTP server
    http.HandleFunc("/signature", handleSignature)
    fmt.Printf("Server starting on %s\n", HostPort)
    err := http.ListenAndServe(HostPort, nil)
    if err != nil {
        fmt.Println("Error starting server:", err)
    }
}
