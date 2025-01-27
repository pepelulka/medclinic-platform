package app

import (
	"auth_service/internal/models"
	"errors"
	"time"

	"github.com/golang-jwt/jwt"
)

func createJwt(userInfo models.UserInfo, jwtSecret string, daysToExpire int) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"login":      userInfo.Login,
		"role":       userInfo.Role,
		"patient_id": userInfo.PatientId,
		"doctor_id":  userInfo.DoctorId,
		"expires":    time.Now().AddDate(0, 0, daysToExpire).Format(time.RFC3339),
	})

	// Sign and get the complete encoded token as a string using the secret
	return token.SignedString([]byte(jwtSecret))
}

func readJwt(token string, jwtSecret string) (jwt.MapClaims, error) {
	tokenParsed, err := jwt.Parse(token, func(token *jwt.Token) (interface{}, error) {
		// since we only use the one private key to sign the tokens,
		// we also only use its public counter part to verify
		return []byte(jwtSecret), nil
	})
	if err != nil {
		return nil, err
	}
	if claims, ok := tokenParsed.Claims.(jwt.MapClaims); ok {
		return claims, nil
	} else {
		return jwt.MapClaims{}, errors.New("can't parse jwt")
	}
}
