# DeepInfra & DSGVO-Konformität (leaf of the `compliance` skill): Technical Brief

Leaf of the `compliance` master skill: a vendor-specific companion to the general [[dsgvo]] leaf
(`references/dsgvo.md`). When DeepInfra is the model host, run the general DSGVO check in the
`dsgvo` leaf and this vendor assessment together; if the DeepInfra model does AI work on personal
data, the [[eu-ai-act]] leaf is also in scope.

**Zweck:** Einschätzung, ob/wie DeepInfra-gehostete Modelle DSGVO-konform in einer Anwendung für
ein österreichisches KMU eingesetzt werden können. Kein Rechtsrat: vor Produktivbetrieb mit
personenbezogenen Daten juristisch absichern.

**Stand:** Juli 2026, basierend auf öffentlich zugänglichen DeepInfra-Dokumenten und Drittquellen.
Live-Angaben (DPF-Status, Rechenzentren, Retention) vor Verlass darauf neu verifizieren.

---

## TL;DR

DeepInfra ist ein reines US-Unternehmen ohne EU-Rechenzentren. Jede Anfrage mit personenbezogenen
Daten ist eine Drittlandübermittlung nach Art. 44 ff. DSGVO. Technisch nutzbar, aber **nicht
automatisch compliant**: erfordert AVV + Transfermechanismus (SCC), bevor personenbezogene Daten
in Prompts landen.

---

## 1. Infrastruktur-Fakten

| Punkt | Status |
|---|---|
| Unternehmenssitz | DeepInfra Inc., Palo Alto, CA, USA |
| Rechenzentren | Ausschließlich USA (mehrere Standorte); keine EU-Region |
| EU-Datenresidenz | Nicht verfügbar |
| Private VPC / On-Prem | Nicht angeboten |
| Zertifizierungen | SOC 2, ISO 27001 (laut Trust Center) |

## 2. Wie DeepInfra Daten verarbeitet

- **Standard-Inferenz:** Input/Output wird **nicht** auf Platte persistiert, nur im RAM während
  der Verarbeitung, danach gelöscht.
- **Bulk-Inference-API:** Kann Daten länger vorhalten, ggf. verschlüsselt auf Platte, mit kurzer
  Retention nach Abschluss.
- **Kein Training** auf Kundendaten. **Ausnahme:** Wird ein Google- oder Anthropic-Modell über
  DeepInfra angesprochen, greifen die Trainings-/Speicherrichtlinien des jeweiligen
  Upstream-Providers (Google Cloud Privacy Notice bzw. Anthropic Trust Center). Das ist relevant
  für die Sub-Processor-Kette im AVV.
- **Logging:** Grundsätzlich kein Content-Logging, nur Metadaten (Request-ID, Kosten,
  Sampling-Parameter). DeepInfra behält sich vor, bei Debugging/Security-Fällen Teile von Requests
  zu loggen.
- Bild-Generierungs-Outputs werden kurzzeitig gespeichert (Demo-Zugriff).

## 3. Offene Compliance-Punkte (vor Go-Live klären)

- [ ] **AVV/DPA nach Art. 28 DSGVO**: kein öffentliches Standarddokument gefunden. Aktiv anfragen:
      `policy@deepinfra.com`
- [ ] **Transfermechanismus**: Status EU-US Data Privacy Framework unklar; laut Drittquelle
      (Sub-Processor-Übersicht eines anderen Anbieters) wird DeepInfra dort über **SCC**
      abgesichert, nicht über DPF-Zertifizierung. Selbst verifizieren auf
      [dataprivacyframework.gov](https://www.dataprivacyframework.gov)
- [ ] **Transfer Impact Assessment (TIA)** bei SCC-Nutzung erforderlich (Schrems-II-Vorgabe)
- [ ] **Sub-Processor-Liste** anfordern, insbesondere falls Google-/Anthropic-Modelle über
      DeepInfra genutzt werden (zusätzliche Kette)
- [ ] **Verarbeitungsverzeichnis (Art. 30)** um DeepInfra als Processor ergänzen

## 4. Implementierungsempfehlungen für den Code

1. **PII-Minimierung an der Quelle:** Vor dem API-Call prüfen/maskieren, ob Prompts
   personenbezogene Daten enthalten (Namen, E-Mail, Kundennummern). Wo möglich pseudonymisieren,
   bevor der Request rausgeht.
2. **Modellauswahl bewusst treffen:** Reine Open-Weight-Modelle (Llama, Mixtral, Qwen etc.)
   bleiben in der DeepInfra-eigenen No-Storage/No-Training-Policy. Google-/Anthropic-Modelle über
   DeepInfra ziehen zusätzliche Datenschutzbedingungen des jeweiligen Herstellers nach sich,
   separat prüfen.
3. **Bulk-API mit Vorsicht:** Falls Bulk-Inference genutzt wird, Retention-Zeitraum und
   Verschlüsselung im AVV explizit festhalten lassen.
4. **Kein Fallback-Logging sensibler Prompts** in eigener Anwendung (Request/Response-Logs
   client-seitig ebenfalls DSGVO-relevant, unabhängig von DeepInfra).
5. **Kill-Switch/Alternative vorsehen:** Für Use Cases mit sensiblen Datenkategorien (Gesundheits-,
   Finanzdaten) einen EU-gehosteten Anbieter als Alternative einplanen (z. B. Anbieter mit
   EU-Rechenzentrum und garantierter Datenresidenz).

## 5. Fazit

DeepInfra ist technisch und vertraglich **nutzbar**, wenn:
- ein AVV mit SCC + TIA vorliegt, **und**
- personenbezogene Daten in Prompts minimiert/vermieden werden, **und**
- bei Nutzung von Google-/Anthropic-Modellen über DeepInfra die zusätzliche Sub-Processor-Kette im
  AVV abgebildet ist.

Ohne diese drei Punkte ist der Einsatz mit personenbezogenen Daten **nicht** DSGVO-konform.

---

## Quellen

- DeepInfra Privacy Policy: https://deepinfra.com/privacy
- DeepInfra Data Privacy Docs: https://docs.deepinfra.com/account/data-privacy
- DeepInfra Trust Center: https://trust.deepinfra.com/
- EU-US Data Privacy Framework Verzeichnis: https://www.dataprivacyframework.gov
