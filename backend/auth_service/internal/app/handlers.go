package app

import (
	"auth_service/config"
	"auth_service/internal/db"
	"auth_service/internal/models"
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
)

// Utils:
func makeError(ctx *gin.Context, err error) {
	ctx.JSON(http.StatusBadRequest, gin.H{"status": "error", "msg": err.Error()})
}

func makeSuccess(ctx *gin.Context) {
	ctx.JSON(200, gin.H{"status": "ok"})
}

// Internal API:

// POST /internal/admin/create
func PostCreateAdmin(ctx *gin.Context, repo *db.UserRepository) {
	var createInfo models.AdminCreate

	if err := ctx.ShouldBindJSON(&createInfo); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	passwordHash, err := hashPassword(createInfo.Credentials.Password)
	if err != nil {
		makeError(ctx, err)
		return
	}
	adminCreateHashed := models.AdminCreateHashed{
		Login:        createInfo.Credentials.Login,
		PasswordHash: passwordHash,
	}
	err = repo.CreateAdmin(adminCreateHashed)
	if err != nil {
		makeError(ctx, err)
		return
	}
	makeSuccess(ctx)
}

// POST /api/admin/patient/create
func PostCreatePatient(ctx *gin.Context, repo *db.UserRepository) {
	var createInfo models.PatientCreate

	if err := ctx.ShouldBindJSON(&createInfo); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	passwordHash, err := hashPassword(createInfo.Credentials.Password)
	if err != nil {
		makeError(ctx, err)
		return
	}
	patientCreateHashed := models.PatientCreateHashed{
		Login:        createInfo.Credentials.Login,
		PasswordHash: passwordHash,
		PatientId:    createInfo.PatientId,
	}
	err = repo.CreatePatient(patientCreateHashed)
	if err != nil {
		makeError(ctx, err)
		return
	}
	makeSuccess(ctx)
}

// POST /api/admin/doctor/create
func PostCreateDoctor(ctx *gin.Context, repo *db.UserRepository) {
	var createInfo models.DoctorCreate

	if err := ctx.ShouldBindJSON(&createInfo); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	passwordHash, err := hashPassword(createInfo.Credentials.Password)
	if err != nil {
		makeError(ctx, err)
		return
	}
	doctorCreateHashed := models.DoctorCreateHashed{
		Login:        createInfo.Credentials.Login,
		PasswordHash: passwordHash,
		DoctorId:     createInfo.DoctorId,
	}
	err = repo.CreateDoctor(doctorCreateHashed)
	if err != nil {
		makeError(ctx, err)
		return
	}
	makeSuccess(ctx)
}

// POST /api/login
func PostLogin(ctx *gin.Context, repo *db.UserRepository, cfg config.Config) {
	var loginInfo models.UserLogin

	if err := ctx.ShouldBindJSON(&loginInfo); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	passwordHashForUser, err := repo.GetPasswordHashByLogin(loginInfo.Login)
	if err != nil {
		print(1)
		makeError(ctx, err)
		return
	}

	checkResult, err := checkPasswords(passwordHashForUser, loginInfo.Password)
	if err != nil {
		print(2)
		makeError(ctx, err)
		return
	}
	if !checkResult {
		print(3)
		makeError(ctx, errors.New("wrong credentials"))
		return
	}

	userInfo, err := repo.GetInfoByLogin(loginInfo.Login)
	if err != nil {
		print(4)
		makeError(ctx, err)
		return
	}

	jwtToken, err := createJwt(userInfo, cfg.JwtSecretKey)
	if err != nil {
		print(5)
		makeError(ctx, err)
		return
	}

	ctx.SetCookie("jwt", jwtToken, 360000, "/", cfg.Host, false, true)
	makeSuccess(ctx)
}
