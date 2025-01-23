package app

import (
	"encoding/base64"

	"golang.org/x/crypto/bcrypt"
)

func hashPassword(password string) (string, error) {
	bytePassword := []byte(password)

	hashedBytePassword, err := bcrypt.GenerateFromPassword(bytePassword, bcrypt.DefaultCost)
	if err != nil {
		return "", err
	}
	hashedPasswordBase64 := base64.StdEncoding.EncodeToString(hashedBytePassword)
	return hashedPasswordBase64, nil
}

func checkPasswords(passwordHash string, password string) (bool, error) {
	bytePassword := []byte(password)
	byteHash, err := base64.StdEncoding.DecodeString(passwordHash)
	if err != nil {
		return false, err
	}
	err = bcrypt.CompareHashAndPassword(byteHash, bytePassword)
	return err == nil, nil
}
