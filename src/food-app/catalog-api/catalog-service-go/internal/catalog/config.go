package catalog

import (
	"os"
	"strings"
)

type Config struct {
	Title   string      `json:"title"`
	App     AppSettings `json:"app"`
	Logging Logging     `json:"logging"`
}

type AppSettings struct {
	AuthEnabled       bool              `json:"authEnabled"`
	UseAppConfig      bool              `json:"useAppConfig"`
	UseSQLite         bool              `json:"useSQLite"`
	ConnectionStrings ConnectionStrings `json:"connectionStrings"`
}

type ConnectionStrings struct {
	SQLiteDBConnection  string `json:"sqliteDbConnection"`
	SQLServerConnection string `json:"sqlServerConnection"`
}

type Logging struct {
	LogLevel LogLevel `json:"logLevel"`
}

type LogLevel struct {
	Default   string `json:"default"`
	Microsoft string `json:"microsoft"`
}

func LoadConfig() Config {
	return Config{
		Title: "Catalog Service",
		App: AppSettings{
			AuthEnabled: strings.EqualFold(env("AUTH_ENABLED", "false"), "true"),
			UseSQLite:   strings.EqualFold(env("USE_SQLITE", "true"), "true"),
			ConnectionStrings: ConnectionStrings{
				SQLiteDBConnection: "Data Source=" + DatabasePath(),
			},
		},
		Logging: Logging{
			LogLevel: LogLevel{Default: "Information", Microsoft: "Warning"},
		},
	}
}

func DatabasePath() string {
	return env("DATABASE_URL", "./food.db")
}

func Port() string {
	return env("PORT", "5000")
}

func env(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}
