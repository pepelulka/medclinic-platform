package main

import (
	"auth_service/config"
	"auth_service/internal/app"
	"auth_service/internal/db"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	conf, err := config.LoadConfig("config.json")

	if err != nil {
		panic(err)
	}

	userRepository, err := db.CreateUserRepository(conf)

	if err != nil {
		panic(err)
	}

	router.Use(app.AuthMiddleware(conf))

	router.GET("/ping", func(ctx *gin.Context) {
		ctx.JSON(200, gin.H{
			"message": "pong",
		})
	})
	router.POST("/internal/admin/create", func(ctx *gin.Context) {
		app.PostCreateAdmin(ctx, &userRepository)
	})
	router.POST("/api/admin/patient/create", app.RequireAdminMiddleware(), func(ctx *gin.Context) {
		app.PostCreatePatient(ctx, &userRepository)
	})
	router.POST("/api/admin/doctor/create", app.RequireAdminMiddleware(), func(ctx *gin.Context) {
		app.PostCreateDoctor(ctx, &userRepository)
	})
	router.POST("/api/login", func(ctx *gin.Context) {
		app.PostLogin(ctx, &userRepository, conf)
	})
	router.Run() // Listen and serve on 0.0.0.0:8080
}
