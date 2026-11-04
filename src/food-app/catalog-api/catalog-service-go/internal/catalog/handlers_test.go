package catalog_test

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"catalog-service-go/internal/catalog"
)

func newHandler(t *testing.T) http.Handler {
	t.Helper()
	store, err := catalog.OpenStore(":memory:")
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })
	return catalog.NewHandler(store, catalog.LoadConfig())
}

func send(t *testing.T, handler http.Handler, method, target, body string) *httptest.ResponseRecorder {
	t.Helper()
	req := httptest.NewRequest(method, target, strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	return rec
}

func decode[T any](t *testing.T, rec *httptest.ResponseRecorder) T {
	t.Helper()
	var value T
	if err := json.Unmarshal(rec.Body.Bytes(), &value); err != nil {
		t.Fatalf("decode %q: %v", rec.Body.String(), err)
	}
	return value
}

func expect(t *testing.T, rec *httptest.ResponseRecorder, status int, body string) {
	t.Helper()
	if rec.Code != status {
		t.Errorf("status = %d, want %d", rec.Code, status)
	}
	if got := strings.TrimSpace(rec.Body.String()); body != "" && got != body {
		t.Errorf("body = %s, want %s", got, body)
	}
}

func TestGetFoodReturnsSeededItems(t *testing.T) {
	rec := send(t, newHandler(t), http.MethodGet, "/food", "")

	expect(t, rec, http.StatusOK, "")
	items := decode[[]catalog.Item](t, rec)
	if len(items) != 5 || items[0].Name != "Hand pulled Noodles" || items[4].Name != "Pizza Tartufo" {
		t.Errorf("items = %+v", items)
	}
}

func TestGetFoodByIDReturnsItemWithJSONFieldNames(t *testing.T) {
	rec := send(t, newHandler(t), http.MethodGet, "/food/4", "")

	expect(t, rec, http.StatusOK, `{"id":4,"name":"Falafel Plate","price":12,"inStock":9,"pictureUrl":"falafel.jpg","description":"Falafel is a deep-fried ball, doughnut or patty made from ground chickpeas. Served with hummus, pita bread, and salad."}`)
}

func TestGetFoodByUnknownIDReturnsNull(t *testing.T) {
	rec := send(t, newHandler(t), http.MethodGet, "/food/99", "")

	expect(t, rec, http.StatusOK, "null")
}

func TestGetFoodByInvalidIDReturnsNotFound(t *testing.T) {
	rec := send(t, newHandler(t), http.MethodGet, "/food/abc", "")

	expect(t, rec, http.StatusNotFound, `{"error":"Not found"}`)
}

func TestCreateFoodReturnsCreatedItem(t *testing.T) {
	handler := newHandler(t)

	rec := send(t, handler, http.MethodPost, "/food", `{"id":0,"name":"Pizza","description":"Delicious cheese pizza","price":12.99}`)

	expect(t, rec, http.StatusCreated, `{"id":6,"name":"Pizza","price":12.99,"inStock":0,"pictureUrl":null,"description":"Delicious cheese pizza"}`)
	items := decode[[]catalog.Item](t, send(t, handler, http.MethodGet, "/food", ""))
	if len(items) != 6 {
		t.Errorf("len(items) = %d, want 6", len(items))
	}
}

func TestCreateFoodWithInvalidBodyReturnsBadRequest(t *testing.T) {
	rec := send(t, newHandler(t), http.MethodPost, "/food", "not json")

	expect(t, rec, http.StatusBadRequest, `{"error":"Bad request"}`)
}

func TestUpdateFoodKeepsFieldsMissingFromBody(t *testing.T) {
	handler := newHandler(t)

	rec := send(t, handler, http.MethodPut, "/food", `{"id":1,"name":"Margherita Pizza","description":"Classic Italian pizza with fresh mozzarella","price":14.99}`)

	want := `{"id":1,"name":"Margherita Pizza","price":14.99,"inStock":9,"pictureUrl":"hand-pulled-noodles.png","description":"Classic Italian pizza with fresh mozzarella"}`
	expect(t, rec, http.StatusOK, want)
	expect(t, send(t, handler, http.MethodGet, "/food/1", ""), http.StatusOK, want)
}

func TestUpdateUnknownFoodReturnsNull(t *testing.T) {
	rec := send(t, newHandler(t), http.MethodPut, "/food", `{"id":99,"name":"Ghost"}`)

	expect(t, rec, http.StatusOK, "null")
}

func TestDeleteFoodRemovesItem(t *testing.T) {
	handler := newHandler(t)

	rec := send(t, handler, http.MethodDelete, "/food/1", "")

	expect(t, rec, http.StatusOK, "{}")
	expect(t, send(t, handler, http.MethodGet, "/food/1", ""), http.StatusOK, "null")
	items := decode[[]catalog.Item](t, send(t, handler, http.MethodGet, "/food", ""))
	if len(items) != 4 {
		t.Errorf("len(items) = %d, want 4", len(items))
	}
}

func TestGetConfigReadsEnvironment(t *testing.T) {
	t.Setenv("AUTH_ENABLED", "True")
	t.Setenv("USE_SQLITE", "false")
	t.Setenv("DATABASE_URL", "./test.db")

	rec := send(t, newHandler(t), http.MethodGet, "/config", "")

	expect(t, rec, http.StatusOK, `{"title":"Catalog Service","app":{"authEnabled":true,"useAppConfig":false,"useSQLite":false,"connectionStrings":{"sqliteDbConnection":"Data Source=./test.db","sqlServerConnection":""}},"logging":{"logLevel":{"default":"Information","microsoft":"Warning"}}}`)
}

func TestGetEnvVarsReturnsEnvironment(t *testing.T) {
	t.Setenv("CATALOG_TEST_VAR", "42")

	rec := send(t, newHandler(t), http.MethodGet, "/config/getEnvVars", "")

	expect(t, rec, http.StatusOK, "")
	if vars := decode[map[string]string](t, rec); vars["CATALOG_TEST_VAR"] != "42" {
		t.Errorf("CATALOG_TEST_VAR = %q, want 42", vars["CATALOG_TEST_VAR"])
	}
}

func TestUnknownRouteReturnsNotFound(t *testing.T) {
	rec := send(t, newHandler(t), http.MethodGet, "/orders", "")

	expect(t, rec, http.StatusNotFound, `{"error":"Not found"}`)
}

func TestPreflightAllowsCrossOriginRequests(t *testing.T) {
	req := httptest.NewRequest(http.MethodOptions, "/food", nil)
	req.Header.Set("Origin", "http://localhost:4200")
	req.Header.Set("Access-Control-Request-Method", http.MethodPut)
	req.Header.Set("Access-Control-Request-Headers", "content-type")
	rec := httptest.NewRecorder()

	newHandler(t).ServeHTTP(rec, req)

	expect(t, rec, http.StatusOK, "")
	if got := rec.Header().Get("Access-Control-Allow-Origin"); got != "*" {
		t.Errorf("Access-Control-Allow-Origin = %q, want *", got)
	}
	if got := rec.Header().Get("Access-Control-Allow-Headers"); got != "content-type" {
		t.Errorf("Access-Control-Allow-Headers = %q, want content-type", got)
	}
}
