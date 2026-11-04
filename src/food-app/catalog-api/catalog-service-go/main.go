package main

import (
	"log"
	"net/http"

	"catalog-service-go/internal/catalog"
)

func main() {
	store, err := catalog.OpenStore(catalog.DatabasePath())
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("Catalog service listening on port %s", catalog.Port())
	log.Fatal(http.ListenAndServe(":"+catalog.Port(), catalog.NewHandler(store, catalog.LoadConfig())))
}
