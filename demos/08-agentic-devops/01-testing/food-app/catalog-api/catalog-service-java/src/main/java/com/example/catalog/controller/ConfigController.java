package com.example.catalog.controller;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/config")
public class ConfigController {

  @GetMapping
  public ResponseEntity<Map<String, Object>> getConfig() {
    boolean authEnabled = Boolean.parseBoolean(System.getenv().getOrDefault("AUTH_ENABLED", "false"));
    boolean useSqlite = Boolean.parseBoolean(System.getenv().getOrDefault("USE_SQLITE", "true"));

    Map<String, Object> config = new HashMap<>();
    config.put("title", "Catalog Service");

    Map<String, Object> app = new HashMap<>();
    app.put("authEnabled", authEnabled);
    app.put("useAppConfig", false);
    app.put("useSQLite", useSqlite);

    Map<String, Object> connectionStrings = new HashMap<>();
    connectionStrings.put("sqliteDbConnection", "Data Source=./food.db");
    connectionStrings.put("sqlServerConnection", "");
    app.put("connectionStrings", connectionStrings);

    config.put("app", app);

    Map<String, Object> logging = new HashMap<>();
    Map<String, String> logLevel = new HashMap<>();
    logLevel.put("default", "Information");
    logLevel.put("microsoft", "Warning");
    logging.put("logLevel", logLevel);
    config.put("logging", logging);

    return ResponseEntity.ok(config);
  }

  @GetMapping("/getEnvVars")
  public ResponseEntity<Map<String, String>> getEnvVars() {
    return ResponseEntity.ok(System.getenv());
  }
}
