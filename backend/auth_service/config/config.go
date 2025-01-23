package config

import (
	"encoding/json"
	"io"
	"os"
)

type Config struct {
	Database struct {
		Host     string `json:"host"`
		Port     int    `json:"port"`
		User     string `json:"user"`
		Password string `json:"password"`
		DbName   string `json:"dbName"`
	} `json:"database"`
	JwtSecretKey string `json:"jwtSecretKey"`
	Host         string `json:"host"`
}

func LoadConfig(filename string) (Config, error) {
	// Open our jsonFile
	jsonFile, err := os.Open(filename)
	// if we os.Open returns an error then handle it
	if err != nil {
		return Config{}, err
	}
	defer jsonFile.Close()

	byteValue, _ := io.ReadAll(jsonFile)
	var config Config
	json.Unmarshal(byteValue, &config)
	return config, nil
}
