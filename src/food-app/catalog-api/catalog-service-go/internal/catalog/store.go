package catalog

import (
	"database/sql"
	"errors"

	_ "modernc.org/sqlite"
)

const createTable = `CREATE TABLE IF NOT EXISTS catalog_item (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	price REAL NOT NULL,
	in_stock INTEGER NOT NULL,
	picture_url TEXT,
	description TEXT
)`

const selectItems = "SELECT id, name, price, in_stock, picture_url, description FROM catalog_item"

type Store struct {
	db *sql.DB
}

type scanner interface {
	Scan(dest ...any) error
}

func OpenStore(path string) (*Store, error) {
	db, err := sql.Open("sqlite", path)
	if err != nil {
		return nil, err
	}
	db.SetMaxOpenConns(1)
	if _, err := db.Exec(createTable); err != nil {
		return nil, err
	}
	store := &Store{db: db}
	return store, store.seed()
}

func (s *Store) Close() error {
	return s.db.Close()
}

func (s *Store) seed() error {
	var count int
	if err := s.db.QueryRow("SELECT COUNT(*) FROM catalog_item").Scan(&count); err != nil || count > 0 {
		return err
	}
	for _, item := range seedItems {
		if _, err := s.db.Exec(
			"INSERT INTO catalog_item (id, name, price, in_stock, picture_url, description) VALUES (?, ?, ?, ?, ?, ?)",
			item.ID, item.Name, item.Price, item.InStock, item.PictureURL, item.Description,
		); err != nil {
			return err
		}
	}
	return nil
}

func scanItem(row scanner) (Item, error) {
	var item Item
	err := row.Scan(&item.ID, &item.Name, &item.Price, &item.InStock, &item.PictureURL, &item.Description)
	return item, err
}

func (s *Store) All() ([]Item, error) {
	rows, err := s.db.Query(selectItems)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	items := []Item{}
	for rows.Next() {
		item, err := scanItem(rows)
		if err != nil {
			return nil, err
		}
		items = append(items, item)
	}
	return items, rows.Err()
}

func (s *Store) Get(id int) (*Item, error) {
	item, err := scanItem(s.db.QueryRow(selectItems+" WHERE id = ?", id))
	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &item, nil
}

func (s *Store) Create(item Item) (Item, error) {
	result, err := s.db.Exec(
		"INSERT INTO catalog_item (name, price, in_stock, picture_url, description) VALUES (?, ?, ?, ?, ?)",
		item.Name, item.Price, item.InStock, item.PictureURL, item.Description,
	)
	if err != nil {
		return item, err
	}
	id, err := result.LastInsertId()
	item.ID = int(id)
	return item, err
}

func (s *Store) Update(item Item) error {
	_, err := s.db.Exec(
		"UPDATE catalog_item SET name = ?, price = ?, in_stock = ?, picture_url = ?, description = ? WHERE id = ?",
		item.Name, item.Price, item.InStock, item.PictureURL, item.Description, item.ID,
	)
	return err
}

func (s *Store) Delete(id int) error {
	_, err := s.db.Exec("DELETE FROM catalog_item WHERE id = ?", id)
	return err
}
