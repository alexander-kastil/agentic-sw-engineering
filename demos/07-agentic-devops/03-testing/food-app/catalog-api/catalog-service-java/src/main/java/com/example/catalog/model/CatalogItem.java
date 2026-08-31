package com.example.catalog.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "catalog_item")
public class CatalogItem {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false)
  private Double price;

  @Column(nullable = false, name = "in_stock")
  private Integer inStock;

  @Column(name = "picture_url")
  private String pictureUrl;

  @Column
  private String description;

  public CatalogItem() {
  }

  public CatalogItem(String name, Double price, Integer inStock, String pictureUrl, String description) {
    this.name = name;
    this.price = price;
    this.inStock = inStock;
    this.pictureUrl = pictureUrl;
    this.description = description;
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public Double getPrice() {
    return price;
  }

  public void setPrice(Double price) {
    this.price = price;
  }

  public Integer getInStock() {
    return inStock;
  }

  public void setInStock(Integer inStock) {
    this.inStock = inStock;
  }

  public String getPictureUrl() {
    return pictureUrl;
  }

  public void setPictureUrl(String pictureUrl) {
    this.pictureUrl = pictureUrl;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }
}
