package com.example.catalog.config;

import com.example.catalog.model.CatalogItem;
import com.example.catalog.repository.CatalogItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {

  @Autowired
  private CatalogItemRepository repository;

  @Override
  public void run(String... args) throws Exception {
    if (repository.count() == 0) {
      List<CatalogItem> items = List.of(
        new CatalogItem("Hand pulled Noodles", 17.0, 9, "hand-pulled-noodles.png",
          "Hand pulled noodles made with love by our experienced cooks from Sichuan. Served with your choice of meat, vegetables, and smashed cucumber salad."),
        new CatalogItem("Pad Kra Pao", 16.0, 12, "pad-kra-pao.png",
          "Pad Kra Pao definitely one of the most popular spicy dishes in Thailand. Cooked with thai holy basil, long beans and chicken. Served with jasmine rice and fried egg."),
        new CatalogItem("Wiener Schnitzel", 18.0, 13, "schnitzel.jpg",
          "Wiener Schnitzel is a traditional Austrian dish consisting of a thin slice of veal coated in breadcrumbs and fried. Served with potato salad and lemon."),
        new CatalogItem("Falafel Plate", 12.0, 9, "falafel.jpg",
          "Falafel is a deep-fried ball, doughnut or patty made from ground chickpeas. Served with hummus, pita bread, and salad."),
        new CatalogItem("Pizza Tartufo", 24.0, 4, "pizza.jpg",
          "Pizza truffle is well tasting, exclusive joy for your taste bud. A delight of white pizza where the protagonist is our cheese with truffle flakes.")
      );
      repository.saveAll(items);
    }
  }
}
