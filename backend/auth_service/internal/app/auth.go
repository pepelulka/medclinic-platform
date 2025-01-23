package app

import (
	"auth_service/config"

	"github.com/gin-gonic/gin"
)

func AuthMiddleware(cfg config.Config) gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := c.Request.Cookie("jwt")
		var role string
		if err != nil || token == nil {
			role = "unauth"
		} else {
			parsed, err := readJwt(token.Value, cfg.JwtSecretKey)
			if err != nil {
				role = "unauth"
			} else {
				if parsed["role"] != nil {
					role = parsed["role"].(string)
				} else {
					role = "unauth"
				}
			}
		}

		c.Set("role", role)

		c.Next()
	}
}

func RequireAdminMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		if c.GetString("role") != "admin" {
			c.AbortWithStatusJSON(401, gin.H{"status": "error", "msg": "Permission denied"})
			return
		}
		c.Next()
	}
}
