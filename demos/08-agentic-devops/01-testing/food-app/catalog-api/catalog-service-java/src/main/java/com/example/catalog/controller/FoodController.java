package com.example.catalog.controller;

import com.example.catalog.model.CatalogItem;
import com.example.catalog.repository.CatalogItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/food")
public class FoodController {

  @Autowired
  private CatalogItemRepository repository;

  @GetMapping
  public ResponseEntity<List<CatalogItem>> getAllFood() {
    return ResponseEntity.ok(repository.findAll());
  }

  @GetMapping("/{id}")
  public ResponseEntity<CatalogItem> getFoodById(@PathVariable Long id) {
    Optional<CatalogItem> item = repository.findById(id);
    return ResponseEntity.ok(item.orElse(null));
  }

  @PostMapping
  public ResponseEntity<CatalogItem> createFood(@RequestBody CatalogItem item) {
    CatalogItem saved = repository.save(item);
    return ResponseEntity.status(HttpStatus.CREATED).body(saved);
  }

  @PutMapping
  public ResponseEntity<CatalogItem> updateFood(@RequestBody CatalogItem item) {
    if (item.getId() == null || !repository.existsById(item.getId())) {
      return ResponseEntity.ok(null);
    }
    CatalogItem updated = repository.save(item);
    return ResponseEntity.ok(updated);
  }

  @DeleteMapping("/{id}")
  public ResponseEntity<Void> deleteFood(@PathVariable Long id) {
    repository.deleteById(id);
    return ResponseEntity.ok().build();
  }
}
