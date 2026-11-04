package catalog

import (
	"encoding/json"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"
)

type api struct {
	store  *Store
	config Config
}

type apiError struct {
	Error string `json:"error"`
}

func NewHandler(store *Store, config Config) http.Handler {
	a := &api{store: store, config: config}
	mux := http.NewServeMux()
	mux.HandleFunc("GET /food", a.getFood)
	mux.HandleFunc("GET /food/{id}", a.getFoodByID)
	mux.HandleFunc("POST /food", a.createFood)
	mux.HandleFunc("PUT /food", a.updateFood)
	mux.HandleFunc("DELETE /food/{id}", a.deleteFood)
	mux.HandleFunc("GET /config", a.getConfig)
	mux.HandleFunc("GET /config/getEnvVars", a.getEnvVars)
	mux.HandleFunc("/", notFound)
	return cors(mux)
}

func (a *api) getFood(w http.ResponseWriter, r *http.Request) {
	items, err := a.store.All()
	respond(w, http.StatusOK, items, err)
}

func (a *api) getFoodByID(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		notFound(w, r)
		return
	}
	item, err := a.store.Get(id)
	respond(w, http.StatusOK, item, err)
}

func (a *api) createFood(w http.ResponseWriter, r *http.Request) {
	var item Item
	if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
		badRequest(w)
		return
	}
	created, err := a.store.Create(item)
	respond(w, http.StatusCreated, created, err)
}

func (a *api) updateFood(w http.ResponseWriter, r *http.Request) {
	var target struct {
		ID int `json:"id"`
	}
	body, err := io.ReadAll(r.Body)
	if err != nil || json.Unmarshal(body, &target) != nil {
		badRequest(w)
		return
	}
	item, err := a.store.Get(target.ID)
	if err != nil || item == nil {
		respond(w, http.StatusOK, item, err)
		return
	}
	if err := json.Unmarshal(body, item); err != nil {
		badRequest(w)
		return
	}
	respond(w, http.StatusOK, item, a.store.Update(*item))
}

func (a *api) deleteFood(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		notFound(w, r)
		return
	}
	respond(w, http.StatusOK, struct{}{}, a.store.Delete(id))
}

func (a *api) getConfig(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, a.config)
}

func (a *api) getEnvVars(w http.ResponseWriter, r *http.Request) {
	vars := map[string]string{}
	for _, entry := range os.Environ() {
		if key, value, _ := strings.Cut(entry, "="); key != "" {
			vars[key] = value
		}
	}
	writeJSON(w, http.StatusOK, vars)
}

func notFound(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusNotFound, apiError{Error: "Not found"})
}

func badRequest(w http.ResponseWriter) {
	writeJSON(w, http.StatusBadRequest, apiError{Error: "Bad request"})
}

func respond(w http.ResponseWriter, status int, body any, err error) {
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, apiError{Error: "Internal server error"})
		return
	}
	writeJSON(w, status, body)
}

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(body)
}

func cors(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		if r.Method == http.MethodOptions {
			w.Header().Set("Access-Control-Allow-Methods", "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT")
			w.Header().Set("Access-Control-Allow-Headers", r.Header.Get("Access-Control-Request-Headers"))
			w.WriteHeader(http.StatusOK)
			return
		}
		next.ServeHTTP(w, r)
	})
}
